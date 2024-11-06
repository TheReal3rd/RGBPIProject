#Just a template Mode.
class Mode():
    name = None
    controller = None

    def __init__(self, controller):
        self.name = "BLANK"
        self.controller = controller

    def update(self):
        pass
