import numpy as np
from . import square

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = np.array([
            [square.Square(x, y, None, False) for x in range(width)] for y in range(height)
            ])
        
    def getSquare(self, x, y):
        return self.board[y][x]


        