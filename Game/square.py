class Square:
    VOLATILE = 2
    STATIC = 1
    EMPTY = 0

    def __init__(self, x, y, color, current):
        self.x = x
        self.y = y
        self.color = color
        self.state = current

