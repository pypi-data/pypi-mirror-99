from pynemo.core.base.abstract.expression import Expression
from pynemo.core.base.operation import CreateOperation, MatchOperation, ReturnOperation


class Statement(Expression):
    def __init__(self):
        self.operations = []

    def match(self, *exp: Expression):
        op = MatchOperation(*exp)
        self.operations.append(op)
        return op.get_instances()

    def create(self, *exp: Expression):
        op = CreateOperation(*exp)
        self.operations.append(op)
        return op.get_instances()

    def return_values(self, *exp: Expression):
        op = ReturnOperation(*exp)
        self.operations.append(op)

    def to_cypher(self, *args, **kwargs):
        ops = []
        for op in self.operations:
            ops.append(op.to_cypher())

        result = '\n'.join(ops) + ';'
        return result
