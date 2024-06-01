class Tetromino:
    """
    To add a new tetromino, create a new class in this directory with the following attributes:

    gridsize: the size of the grid that the tetromino occupies
    shape: a list of tuples representing the squares that make up the tetromino
    color: the color of the tetromino
    pivot: the square that the tetromino rotates around

    Then add the class to the TETROMINOES list in Game/game.py
    """


    def __init__(self):
        pass

    @staticmethod
    def rotate(shape, pivot, direction):
        # subtract the pivot from each square to rotate around the pivot
        rotated = []
        for square in shape:
            x = square[0] - pivot[0]
            y = square[1] - pivot[1]
            if direction == 0: # rotate clockwise
                rotated.append((y + pivot[0], -x + pivot[1]))
            elif direction == 1: # rotate counterclockwise
                rotated.append((-y + pivot[0], x + pivot[1]))
            elif direction == 2: # rotate 180 degrees
                rotated.append((-x + pivot[0], -y + pivot[1]))
        return rotated