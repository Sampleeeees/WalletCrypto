import json


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