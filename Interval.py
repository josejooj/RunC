import threading

class setInterval:
    def __init__(self,time,action) :
        self.time = time
        self.action = action
        self.canceled = 0
        self.__setInterval()

    def __setInterval(self) :
        if self.canceled != 1:
            threading.Timer(self.time, self.action).start()
            threading.Timer(self.time, self.__setInterval).start()

    def cancel(self) :
        self.canceled = 1
