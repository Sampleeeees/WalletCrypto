from asyncapi_schema_pydantic import ( # noqa
    AsyncAPI,
    Info,
    ChannelItem,
    Operation,
    Message,
    ChannelBindings,
    AmqpChannelBinding,
    AmqpQueue,
    Tag
)

# Construct AsyncAPI by pydantic objects
async_api = AsyncAPI(
    info=Info(
        title="Email Service",
        version="1.0.0",
        description='description'
    ),
    channels={
        "user/signedup": ChannelItem(
            description='This channel is used to exchange messages about users signing up',
            subscribe=Operation(
                summary='A user signed up.',
                message=Message(
                    name='UserSignup',
                    title='User signup',
                    summary='Action to sign a user up.',
                    description='A longer description of the message',
                    contentType='application/json',
                    tags=[
                        Tag(name='user'),
                        Tag(name='signup'),
                        Tag(name='register')
                    ]
                ),
            ),
            bindings=ChannelBindings(
                amqp=AmqpChannelBinding(
                    param_is='queue',
                    queue=AmqpQueue(
                        name='my-queue-name',
                        durable=True,
                        exclusive=True,
                        autoDelete=False,
                        vhost='/'
                    )
                )
            )
        )
    }
)


if __name__ == "__main__":
    print(async_api.json(by_alias=True, exclude_none=True, indent=2))

    # # recursively delete "oneOf", "anyOf", "allOf", "enum" keys if they are []
    # for_delete = ['"oneOf": [],\n', '"anyOf": [],\n', '"allOf": [],\n', '"enum": [],\n']
    # for key in for_delete:
    #     json_data = json_data.replace(key, "")
    #
    # # dump to file sample.yaml
    # with open("asyncapi_docs.yaml", "w") as f:
    #     f.write(json_data)