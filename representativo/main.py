from Interval import setInterval

class toTest():
    def __init__(self):
        self.interval = setInterval(1, self.func)
        self.i = 0

    def func(self):
        print(self.i)
        self.i = self.i + 1
        if self.i == 10:
            self.interval.cancel()

toTest()