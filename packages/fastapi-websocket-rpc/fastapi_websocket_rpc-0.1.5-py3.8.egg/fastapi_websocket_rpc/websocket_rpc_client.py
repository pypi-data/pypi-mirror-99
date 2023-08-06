import asyncio
from fastapi_websocket_rpc.rpc_methods import RpcMethodsBase
from typing import Dict
from tenacity import retry, wait
from tenacity.retry import retry_if_exception

import websockets
from websockets.exceptions import InvalidStatusCode

from .rpc_channel import RpcChannel
from .logger import get_logger

logger = get_logger("RPC_CLIENT")


def isNotInvalidStatusCode(value):
    return not isinstance(value, InvalidStatusCode)


class WebSocketRpcClient:
    """
    RPC-client to connect to an WebsocketRPCEndpoint
    Can call methodes exposed by server
    Exposes methods that the server can call
    """

    def __init__(self, uri, methods=None, retry_config=None, default_response_timeout=None, **kwargs):
        """
        Args:
            uri (str): server uri to connect to (e.g. 'http://localhost/ws/client1')
            methods (RpcMethodsBase): RPC methods to expose to the server
            retry_config (dict): Tenacity.retry config (@see https://tenacity.readthedocs.io/en/latest/api.html#retry-main-api) 
            default_response_timeout (float): default time in seconds
            **kwargs: Additional args passed to connect (@see class Connect at websockets/client.py)
                      https://websockets.readthedocs.io/en/stable/api.html#websockets.client.connect


            usage:
                async with  WebSocketRpcClient(uri, RpcUtilityMethods()) as client:
                response = await client.call("echo", {'text': "Hello World!"})
                print (response)
        """
        self.methods = methods or RpcMethodsBase()
        self.connect_kwargs = kwargs
        # Websocket connection
        self.conn = None
        # Websocket object
        self.ws = None
        # URI to connect on
        self.uri = uri
        # Pending requests - id mapped to async-event
        self.requests: Dict[str, asyncio.Event] = {}
        # Received responses
        self.responses = {}
        # Read worker
        self._read_task = None
        # defaults
        self.default_response_timeout = default_response_timeout
        # RPC channel
        self.channel = None
        self.retry_config = retry_config if retry_config is not None else {
            'wait': wait.wait_exponential(),
            'retry': retry_if_exception(isNotInvalidStatusCode),
            'reraise': True
        }

    async def __connect__(self):
        logger.info("Trying server", uri=self.uri)
        # Start connection
        self.conn = websockets.connect(self.uri, **self.connect_kwargs)
        # Get socket
        self.ws = await self.conn.__aenter__()
        # Init an RPC channel to work on-top of the connection
        self.channel = RpcChannel(self.methods, self.ws, default_response_timeout=self.default_response_timeout)
        # Start reading incoming RPC calls
        self._read_task = asyncio.create_task(self.reader())
        return self

    async def __aenter__(self):
        if self.retry_config is False:
            return await self.__connect__()
        else:
            return await retry(**self.retry_config)(self.__connect__)()

    async def __aexit__(self, *args, **kwargs):
        # Stop reader - if created
        if self._read_task:
            self._read_task.cancel()
        # Stop socket
        if (hasattr(self.conn, "ws_client")):
            await self.conn.__aexit__(*args, **kwargs)

    async def reader(self):
        """
        Read responses from socket worker
        """
        while True:
            raw_message = await self.ws.recv()
            await self.channel.on_message(raw_message)

    async def wait_on_reader(self):
        """
        Join on the internal reader task
        """
        await self._read_task

    async def call(self, name, args={}, timeout=None):
        """
        Call a method and wait for a response to be received
         Args: 
            name (str): name of the method to call on the other side (As defined on the otherside's RpcMethods object)
            args (dict): keyword arguments to be passeds to otherside method
        """
        return await self.channel.call(name, args, timeout=timeout)

    @property
    def other(self):
        """
        Proxy object to call methods on the other side
        """
        return self.channel.other
