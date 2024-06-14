from Renderer.outputSystem import OutputSystem
import numpy as np

class terminalOutput(OutputSystem):
    def __init__(self):
        super().__init__()

    @staticmethod
    def printDetails(gameClass):
        squares = str(gameClass.board).split('\n')
        nextPiece = gameClass.nextPiece
        holdPiece = gameClass.holdPiece
        score = gameClass.score
        lines = gameClass.lines

        nextGrid = np.full((gameClass.nextPiece.gridsize,
                             gameClass.nextPiece.gridsize), '.')
        nextCenter = (int(gameClass.nextPiece.gridsize / 2), 0)
        for square in gameClass.nextPiece.shape:
            nextGrid[gameClass.nextPiece.gridsize-(nextCenter[1]+
                     square[1])-1][nextCenter[0]+
                                square[0]] = 'o'
                
        holdGrid = np.full((4, 4), '.')
        if gameClass.holdPiece is not None:
            holdCenter = (int(gameClass.holdPiece.gridsize / 2), 0)
            holdGrid = np.full((gameClass.holdPiece.gridsize,
                                gameClass.holdPiece.gridsize), '.')
            for square in gameClass.holdPiece.shape:
                holdGrid[gameClass.nextPiece.gridsize-(holdCenter[1]+square[1])-1][holdCenter[0]+
                                    square[0]] = 'o'

        print(f'SCORE: {score}')
        print(f'LINES CLEARED: {lines}\n\n')
        print(f'{squares[0]}\t\tNEXT:')
        for i in range(len(nextGrid)):
            print(f'{squares[i+1]}\t\t{str(nextGrid[i])[1:-1]}')
        print(f'{squares[1+len(nextGrid)]}')
        print(f'{squares[2+len(nextGrid)]}\t\tHOLD:')
        for i in range(len(holdGrid)):
            print(f'{squares[i+3+len(nextGrid)]}\t\t{str(holdGrid[i])[1:-1]}')
        iterator = range(3+len(nextGrid)+len(holdGrid), len(squares))
        for i in iterator:
            print(f'{squares[i]}')

    
    def updateBoard(self, gameClass):
        terminalOutput.printDetails(gameClass)
    
    def updateNextPiece(self, gameClass):
        terminalOutput.printDetails(gameClass)
    
    def updateHoldPiece(self, gameClass):
        terminalOutput.printDetails(gameClass)

    def updateScore(self, gameClass):
        terminalOutput.printDetails(gameClass)

    def updateLines(self, gameClass):
        terminalOutput.printDetails(gameClass)


    def updateGameOver(self, gameClass):
        terminalOutput.printDetails(gameClass)
        print('GAME OVER')
