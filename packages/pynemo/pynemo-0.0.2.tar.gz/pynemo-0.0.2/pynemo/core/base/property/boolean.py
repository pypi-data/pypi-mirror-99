from pynemo.core.base.abstract.property import Property


class BooleanProperty(Property):
    @classmethod
    def validate(cls, v):
        assert v in (True, False)
        return bool(v)

    @classmethod
    def to_cypher(cls, v):
        return repr(cls.validate(v)).lower()
