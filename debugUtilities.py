import time
class prints:
    @staticmethod
    def log(classname, key, information):
        print("[" + str(classname) + "] >>>>>> " + str(key) + ": " + str(information))

class timer:
    def __init__(self):
        self.s_time = 0

    def start(self):
        self.s_time = time.time()

    def getElapsed(self):
        return time.time() - self.s_time
    
    def printElapsed(self):
        prints.log("Timer", "elapsed time", self.getElapsed())
