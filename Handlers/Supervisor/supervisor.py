class supervisor():
    def __init__(self):
        self.data = {}
        self.bypass = False
        self.showRemanent = None
        self.Print = None
        self.blocked = False

    def init(self):
        self.data["isWaiting"] = False
