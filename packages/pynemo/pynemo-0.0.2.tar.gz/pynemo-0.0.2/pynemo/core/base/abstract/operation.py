from .expression import Expression


class Operation(Expression):
    def __init__(self, *expressions: Expression):
        self.expressions = expressions

    def get_instances(self):
        s = []
        for e in self.expressions:
            s.extend(e.get_instances())
        return s

    def to_cypher(self, *args, **kwargs):
        raise NotImplementedError()
