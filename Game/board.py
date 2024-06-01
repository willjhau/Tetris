import numpy as np
from Game import square

class GameBoard:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.board = np.array([
            [square.Square(x, y, None, square.Square.EMPTY) for x in range(width)] for y in range(height)
        ])
        
    def getSquare(self, x, y):
        if int(x) != x or int(y) != y:
            raise ValueError(f"Coordinates must be integers: {x}, {y}")
        
        return self.board[int(y)][int(x)]


    def __str__(self):
        # Print the board with a space if the square is empty, an x if the square is static, and an o if the square is volatile
        return '\n'.join([
            ' '.join([
                '.' if sq.state == square.Square.EMPTY else 'x' if sq.state == square.Square.STATIC else 'o' for sq in row
            ]) for row in self.board[::-1]
        ])