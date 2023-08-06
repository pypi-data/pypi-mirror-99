class Property:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        raise NotImplementedError()

    @classmethod
    def to_cypher(cls, v):
        raise NotImplementedError()
