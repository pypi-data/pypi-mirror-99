from pynemo.core.base.abstract.property import Property


class FloatProperty(Property):
    @classmethod
    def validate(cls, v):
        return float(v)

    @classmethod
    def to_cypher(cls, v):
        return repr(float(v))
