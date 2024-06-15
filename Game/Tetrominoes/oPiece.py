class oPiece:
    gridsize = 4
    shape = [(-1, 1), (0, 1), (-1, 2), (0, 2)]
    color = (247, 211, 8)
    pivot = (-0.5, 1.5)

    def __init__(self):
        pass

    @classmethod
    def rotate(cls, shape, pivot, direction, rotateState):
        return [(pivot, shape)]
