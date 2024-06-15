from Game.Tetrominoes.tetromino import Tetromino

class LinePiece:
    gridsize = 4
    shape = [(-2, 2), (-1, 2), (0, 2), (1, 2)]
    color = (49, 199, 239)
    pivot = (-0.5, 1.5)

    kickTable = {
        '01': [(-2, 0), (1, 0), (-2, -1), (1, 2)],
        '10': [(2, 0), (-1, 0), (2, 1), (-1, -2)],
        '12': [(-1, 0), (2, 0), (-1, 2), (2, -1)],
        '21': [(1, 0), (-2, 0), (1, -2), (-2, 1)],
        '23': [(2, 0), (-1, 0), (2, 1), (-1, -2)],
        '32': [(-2, 0), (1, 0), (-2, -1), (1, 2)],
        '30': [(1, 0), (-2, 0), (1, -2), (-2, 1)],
        '03': [(-1, 0), (2, 0), (-1, 2), (2, -1)],
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