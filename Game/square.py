import config

class Square:
    VOLATILE = 2
    STATIC = 1
    EMPTY = 0

    def __init__(self, x, y, color, current):
        self.x = x
        self.y = y
        
        if color is None:
            self.color = config.NULL_COLOR
        else:
            self.color = color

        self.state = current # 0 = empty, 1 = static, 2 = volatile

