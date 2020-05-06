from constraints.declarativeconstraint import DeclarativeConstraints


class DummyRules(DeclarativeConstraints):

    def __init__(self):
        super().__init__([])