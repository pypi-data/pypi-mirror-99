class Expression:
    def to_cypher(self, *args, **kwargs):
        raise NotImplementedError()

    def get_instances(self):
        return []
