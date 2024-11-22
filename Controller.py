#This is used to manage all fixtures.
class Controller():

    _fixtures = {}

    def __init__(self):
        self.buildFixtures()

    def update(self):
        for fix in self._fixtures.keys():
            fixture = self._fixtures[fix]
            fixture.update()

    def buildFixtures(self):
        pass

    # Funcs

    def close(self):
        for fix in self._fixtures.keys():
            fixture = self._fixtures[fix]
            fixture.stop()

    def save(self):
        pass

    def load(self):
        pass

    # Getters

    def getFixtures(self):
        return self._fixtures

    # Setters