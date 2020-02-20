class supervisor():
    def __init__(self):
        self.data = {}
        self.bypass = False

    def init(self):
        self.data["isWaiting"] = False
