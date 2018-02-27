"""Schema utilities."""

from marshmallow import post_load


def to_model(model_cls):
    def inner(Cls):
        class ToModelSchema(Cls):

            def __init__(self, *args, session=None, check_existing=False,
                         **kwargs):
                kwargs.setdefault('context', {})
                kwargs['context'].setdefault('session', session)
                kwargs['context'].setdefault('check_existing', check_existing)
                super().__init__(*args, **kwargs)

            @post_load
            def to_model(self, data):
                session = self.context.get('session')
                if session and self.context.get('check_existing'):
                    return model_cls.get(session, **data) or model_cls(**data)
                return model_cls(**data)
        return ToModelSchema
    return inner