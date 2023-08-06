""" Internal session package. """

import asyncio
from typing import Dict, Hashable, Optional

import structlog

from diffusion.handlers import HandlersMapping, SimpleHandler, UnknownHandlerError
from diffusion.internal import utils
from diffusion.internal.protocol.conversations import (
    Conversation,
    ConversationID,
    ConversationSet,
)
from diffusion.internal.services import Service, ServiceLocator
from .connection import Connection, State
from .credentials import Credentials

LOG = structlog.get_logger()


class InternalSession:
    """Internal session implementation.

    Args:
        connection: The connection to a Diffusion server.

    Attributes:
        conversations: A `ConversationSet` instance managing active conversations.
        handlers: A mapping of callables that can be called to handle various events.
    """

    def __init__(self, connection: Connection):
        self.connection = connection
        self.conversations = ConversationSet()
        self.handlers: HandlersMapping = {
            Service.get_by_name("SYSTEM_PING"): _system_ping_default_handler,
        }
        self.data: dict = utils.nested_dict()
        self.services = ServiceLocator()
        self._read_task: Optional[asyncio.Task] = None

    async def send_request(self, service: Service, conversation: Optional[Conversation] = None):
        """ Send a request to the server. """
        if conversation is None:
            conversation = await self.conversations.new_conversation(service)
        LOG.debug(
            "Sending request.",
            cid=conversation.cid,
            service=service,
            request=service.request,
        )
        request_message = await self.protocol.prepare_request(conversation)
        await self.connection.send(request_message)
        return await conversation.get_value()

    async def close(self):
        """ Close the session and the underlying connection. """
        await self.connection.close()

    def get_conversation(self, cid: ConversationID) -> Conversation:
        """ Retrieve a conversation from the set based on its ID. """
        return self.conversations.get_by_cid(cid)

    async def connect(self, properties: Optional[Dict[str, str]] = None) -> None:
        """ Establish or re-establish a connection with the server. """
        await self.connection.connect(properties)
        self._read_task = asyncio.create_task(self.connection.read_loop(self))

    @property
    def protocol(self):
        """ Gets the underlying protocol used by the session. """
        return self.connection.protocol

    @property
    def session_id(self):
        """ Session ID of the current session. """
        if self.connection.response is None:
            return None
        return self.connection.response.session_id

    @property
    def protocol_version(self) -> int:
        """ Client protocol version. """
        return self.connection.protocol.VERSION

    @property
    def state(self) -> State:
        """ Get current connection state. """
        return self.connection.state

    @property
    def principal(self) -> str:
        """ The security principal currently associated with the session. """
        return self.connection.principal

    async def handle(self, handler_key: Hashable, **kwargs):
        """Invoke the handler registered for the given key.

        A typical usage is for a service instance to call this method when handling
        a received message (either a request or a response to a request). The key
        will then generally be a tuple consisting of the service's class and a textual
        key (e.g. a topic selector or a message path), and sometimes additional values
        for further specialisation (e.g. event type like "error" or "subscribed").

        Args:
            handler_key: Any hashable (immutable) object.
            *args, **kwargs: Any arguments passed directly to the handler function.

        Raises:
            UnknownHandlerError: If there is no handler registered for the given key.
        """
        LOG.debug("Handling event.", handler_key=handler_key, kwargs=kwargs)
        try:
            handler = self.handlers[handler_key]
        except KeyError:
            raise UnknownHandlerError(f"A handler was not registered for key '{handler_key}'.")
        else:
            return await handler.handle(**kwargs)


@SimpleHandler
async def _system_ping_default_handler():
    message = "System ping received."
    LOG.debug(message)
    return message
