from pynemo.core.base.abstract.operation import Operation


class ReturnOperation(Operation):
    def to_cypher(self):
        results = []
        for e in self.expressions:
            results.append(e.to_cypher())

        results = ', '.join(results)
        return f'RETURN {results}'
