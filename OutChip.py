
class OutChip:
    def __init__(self, x, y, number):
        self.x = x
        self.y = y
        self.number = number
        self.state = 0

    def go(self, number):
        if self.state != 0: return
        if self.number == number:
            self.state = 2
        else:
            self.state = 1

    def reset(self):
        self.state = 0