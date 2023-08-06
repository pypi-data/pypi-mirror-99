from pynemo.core.base.abstract.property import Property


class IntegerProperty(Property):
    @classmethod
    def validate(cls, v):
        return int(v)

    @classmethod
    def to_cypher(cls, v):
        return repr(int(v))
