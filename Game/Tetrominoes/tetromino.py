class Tetromino:
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