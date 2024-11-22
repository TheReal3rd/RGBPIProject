#Template Fixture. This is intended to add expandability.
class FixtureBase():
    _name = None

    def __init__(self, name, ):
        self._name = name

    def stop(self):
        pass

    # Getter

    def getName(self):
        return self._name

    # Setter
    