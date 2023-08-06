from pynemo.core.base.abstract.property import Property


class StringProperty(Property):
    @classmethod
    def validate(cls, v):
        return str(v)

    @classmethod
    def to_cypher(cls, v):
        return repr(str(v))
