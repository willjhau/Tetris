from Game.Tetrominoes.tetromino import Tetromino

class tPiece:
    gridsize = 3
    shape = [(-1, 1), (0, 1), (1, 1), (0, 2)]
    color = (173, 77, 156)
    pivot = (0, 1)

    kickTable = {
        '01': [(-1, 0), (-1, 1), (-1, -2)],
        '10': [(1, 0), (1, -1), (0, 2), (1, 2)],
        '12': [(1, 0), (1, -1), (0, 2), (1, 2)],
        '21': [(-1, 0), (0, -2), (-1, -2)],
        '23': [(1, 0), (0, -2), (1, -2)],
        '32': [(-1, 0), (-1, -1), (0, 2), (-1, 2)],
        '30': [(-1, 0), (-1, -1), (0, 2), (-1, 2)],
        '03': [(1, 0), (1, 1), (1, -2)],
        '02': [],
        '20': [],
        '13': [],
        '31': []
    }

    def __init__(self):
        pass

    @classmethod
    def rotate(cls, shape, pivot, direction, rotateState):
        if direction == 0:
            targetRotateState = (rotateState + 1) % 4
        elif direction == 1:
            targetRotateState = (rotateState - 1) % 4
        else:
            targetRotateState = (rotateState + 2) % 4
        
        key = str(rotateState) + str(targetRotateState)
        coordSet = []
        rotatedCoords = Tetromino.rotate(shape, pivot, direction)
        coordSet.append((pivot, rotatedCoords))
        for x, y in cls.kickTable[key]:
            newPivot = (pivot[0] + x, pivot[1] + y)
            newCoords = [(square[0] + x, square[1] + y) for square in rotatedCoords]
            coordSet.append((newPivot, newCoords))
        
        return coordSet
