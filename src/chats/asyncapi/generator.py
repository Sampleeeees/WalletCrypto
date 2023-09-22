import datetime
import json
from typing import Optional
from uuid import UUID

from asyncapi_schema_pydantic import (  # noqa
    AsyncAPI,
    Info,
    ChannelItem,
    Operation,
    Message,
    ChannelBindings,
    AmqpChannelBinding,
    AmqpQueue,
    Components,
    Tag, WebSocketsChannelBinding
)

from pydantic import BaseModel, EmailStr

class AsyncSchema:

    @classmethod
    def async_schema(cls, **kwargs):
        """
        Return async schema.
        """
        schema = cls.schema()
        schema.pop("definitions", None)
        schema_str = json.dumps(schema)
        schema_str = schema_str.replace("#/definitions/", "#/components/schemas/")
        return json.loads(schema_str)


class User(BaseModel, AsyncSchema):
    id: UUID
    username: str
    email: EmailStr
    avatar: Optional[str] = None

class Disconnect(BaseModel, AsyncSchema):
    detail: str


class ChatMessage(BaseModel, AsyncSchema):
    message: str
    image: Optional[str] = None
    date: Optional[datetime.datetime]
    user_id: UUID
    username: str
    avatar: Optional[str] = None


# Construct AsyncAPI by pydantic objects
async_api = AsyncAPI(
    info=Info(
        title="Socket.IO Chat service",
        version="1.0.0",
        description="AsyncAPI documentation for description socket events",
    ),
    servers={
        "socketio": {
            "url": "http://127.0.0.1:8001/ws/socket.io",
            "protocol": "wss",
            "protocolVersion": "5",
            "description": "Socketio development server",
        },
        "rabbitmq": {
            "url": "amqp://localhost:5672",
            "protocol": "amqp",
            "protocolVersion": "0.9.1",
            "description": "RabbitMQ development server",
        },
    },
    channels={
        "connect": ChannelItem(
            description="This channel is used for connecting users",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="User connecting.",
                message={
                    "$ref": "#/components/messages/UserData",
                },
            ),
            subscribe=Operation(
                summary="New connection for server.",
                message={
                    "$ref": "#/components/messages/UserData",
                },
            ),
        ),
        "get_history": ChannelItem(
            description="This channel is used for get chat history",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="Server emit chat history.",
                message={
                    "$ref": "#/components/messages/ChatHistory",
                },
            ),
            subscribe=Operation(
                summary="Get chat history.",
                message={
                    "$ref": "#/components/messages/ChatHistory",
                },
            ),
        ),
        "new_message": ChannelItem(
            description="This channel is used for exchange of new messages between users",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="User send new message.",
                message={
                    "$ref": "#/components/messages/NewMessage",
                },
            ),
            subscribe=Operation(
                summary="User get new messages.",
                message={
                    "$ref": "#/components/messages/NewMessage",
                },
            ),
        ),
        "user_detail": ChannelItem(
            description="This channel is used for get additional info about online user",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="Server emit additional info about user.",
                message={
                    "$ref": "#/components/messages/UserInfo",
                },
            ),
            subscribe=Operation(
                summary="User get additional info about another user.",
                message={
                    "$ref": "#/components/messages/UserInfo",
                },
            ),
        ),
        "disconnect": ChannelItem(
            description="This channel is used for disconnecting users",
            bindings=ChannelBindings(
                ws=WebSocketsChannelBinding(),
            ),
            publish=Operation(
                summary="User disconnect from chat.",
                message={
                    "$ref": "#/components/messages/DisconnectData",
                },
            ),
        ),
    },
    components=Components(
        messages={
            "UserData": Message(
                name="User",
                title="User Data",
                summary="Action to connect to server.",
                description="Get user data after success connection",
                contentType="application/json",
                tags=[
                    Tag(name="User connect"),
                    Tag(name="User data"),
                ],
                payload={
                    "$ref": "#/components/schemas/User",
                },
            ),
            "ChatHistory": Message(
                name="ChatHistory",
                title="Chat History",
                summary="Action to got chat history.",
                description="Get chat history after success connection",
                contentType="application/json",
                tags=[
                    Tag(name="Chat History"),
                ],
                payload={
                    "$ref": "#/components/schemas/ChatMessage",
                },
            ),
            "NewMessage": Message(
                name="NewMessage",
                title="New Message",
                summary="Action to got new messages.",
                description="Get new messages in chat",
                contentType="application/json",
                tags=[
                    Tag(name="New Message"),
                ],
                payload={
                    "$ref": "#/components/schemas/ChatMessage",
                },
            ),
            "UserInfo": Message(
                name="UserInfo",
                title="User Info",
                summary="Action to got user info.",
                description="Get additional info about another user",
                contentType="application/json",
                tags=[
                    Tag(name="User"),
                    Tag(name="Additional Info"),
                ],
                payload={
                    "$ref": "#/components/schemas/User",
                },
            ),
            "DisconnectData": Message(
                name="DisconnectData",
                title="Disconnect user",
                summary="Action for disconnect user from server",
                description="Disconnect user from server and print success disconnect",
                contentType="application/json",
                tags=[
                    Tag(name="Disconnect User")
                ],
                payload={
                    "$ref": "#/components/schemas/Disconnect",
                },
            )
        },
        schemas={
            "User": User.async_schema(),
            "ChatMessage": ChatMessage.async_schema(),
            "Disconnect": Disconnect.async_schema(),
        },
    ),
)


if __name__ == "__main__":
    json_data = async_api.json(by_alias=True, exclude_none=True, indent=2)

    # recursively delete "oneOf", "anyOf", "allOf", "enum" keys if they are []
    for_delete = ['"oneOf": [],\n', '"anyOf": [],\n', '"allOf": [],\n', '"enum": [],\n']
    for key in for_delete:
        json_data = json_data.replace(key, "")

    # dump to file sample.yaml
    with open("asyncapi_docs.yaml", "w") as f:
        f.write(json_data)