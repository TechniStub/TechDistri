import SimpleMFRC522 as readerLib
from threading import Thread

class RFIDHandler(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.reader = readerLib.SimpleMFRC522()
        self.readed = False
        self.lastId = 0
        self.id = 0
        self.stop = False

    def run(self):
        while not(self.stop):
            while self.lastId == self.id and not(self.stop):
                self.id = self.reader.read_id_no_block()
            self.lastId = self.id
            self.readed = True

if __name__ == "__main__":
    t1 = RFIDHandler()

    t1.start()
    try:
        while True:
            if(t1.readed):
                print(t1.lastId)
                t1.readed = False
    except:
        t1.stop = True
        t1.join()
