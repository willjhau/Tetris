from Game.game import Game
import matplotlib.pyplot as plt
import os
import numpy as np
import cv2
from Game.square import Square
from Game.board import GameBoard

class GreedyAgent:
    def __init__(self, inputFlag, eventQueue, game: Game):
        self.eventQueue = eventQueue
        inputFlag.flag = True
        self.game = game

        while not self.game.running:
            pass
        

        # Delete the production folder if it exists
        if os.path.exists('production'):
            for root, dirs, files in os.walk('production', topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir('production')

        os.makedirs('production')


        # check if production/counter.txt exists
        if not os.path.exists('production/counter.txt'):
            with open('production/counter.txt', 'w') as f:
                f.write('0')
        
        self.saveProjections()

        while self.game.running:
            if self.game.boardChanged:
                self.saveProjections()
                self.game.boardChanged = False
    
    def scorePosition(self, position):
        # the higher the score the better the position
        # EDIT THIS TO MODIFY THE ALGORITHM'S SELECTION CRITERIA
        score = 0
        rowsCleared = []
        maxHeight = 0
        minHeight = self.game.board.height
        minSet = False

        # Award points for clearing lines, with more points for clearing multiple lines at once
        for i, row in enumerate(self.game.board.board):
            rowArray = [((sq.state == Square.STATIC) or ((i, j) in position)) for j, sq in enumerate(row)]
            if all(rowArray):
                score += 3*(len(rowsCleared)+1)
                rowsCleared.append(i)
                maxHeight = i+1
            elif not (any(rowArray)):
                if not minSet:
                    minHeight = i
                    minSet = True
            else:
                if not minSet:
                    minHeight = i
                    minSet = True
                maxHeight = i+1
        
        # Award points for having a low height
        score += self.game.board.height - maxHeight
        
        # Deduct points for having a high height difference between columns
        score -= maxHeight - minHeight

        # Deduct points for having holes in the board
        

    def saveProjections(self):
        # read the counter
        with open('production/counter.txt', 'r') as f:
            counter = int(f.read())

        for i,position in enumerate(self.listAllPositions()):
            # Create an image of the board with the piece in the projected position
            # save the image to a file at production/{counter}/{INDEX}.png
            self.makeProjectionImage(position, counter, i)
            
        with open('production/counter.txt', 'r') as f:
            counter = int(f.read())
        with open('production/counter.txt', 'w') as f:
            f.write(str(counter + 1))

            
    def makeProjectionImage(self, projectionCoords, counter, index):
        grid = np.zeros((self.game.board.height, self.game.board.width, 3), dtype=np.uint8)
        for x, y in projectionCoords:
            grid[y][x] = self.game.currentPiece.color
        
        for x in range(self.game.board.width):
            for y in range(self.game.board.height):
                if self.game.board.getSquare(x, y).state == 1:
                    grid[y][x] = self.game.board.getSquare(x, y).color
        
        # Create an image of the board where one grid item is 20x20 pixels

        # check if the production/counter folder exists
        if not os.path.exists(f'production/{counter}'):
            os.makedirs(f'production/{counter}')

        # save the image to a file at production/{counter}/{INDEX}.png. convert RGB to BGR
        cv2.imwrite(f'production/{counter}/{index}.png', cv2.cvtColor(grid, cv2.COLOR_RGB2BGR))



    def listAllPositions(self):
        positions = [] 

        originalPos = self.game.getCurrentPos()[:]
        rawRotations = [originalPos, 
                        self.game.currentPiece.rotate(originalPos, self.game.pivot, 0, self.game.rotateState)[0][1], 
                        self.game.currentPiece.rotate(originalPos, self.game.pivot, 2, self.game.rotateState)[0][1], 
                        self.game.currentPiece.rotate(originalPos, self.game.pivot, 1, self.game.rotateState)[0][1]]
        rotations = []
        for rot in rawRotations: # Remove congruent rotations
            minX = min([x for x, y in rot])
            minY = min([y for x, y in rot])
            norm = [(x - minX, y - minY) for x, y in rot]
            if norm not in rotations:
                rotations.append(norm)
        
        for rot in rotations:
            for x in range(self.game.board.width):
                for y in range(self.game.board.height):
                    coords = [(x + x0, y + y0) for x0, y0 in rot]
                    shiftedPos = [(x, y-1) for x, y in coords]
                    if (self.game.checkCollision(shiftedPos) and 
                        not self.game.checkCollision(coords)):
                        flag = True
                        for c in positions:
                            b = all([(x, y) in c for x, y in coords])
                            if b:
                                flag = False
                        if flag:
                            positions.append(coords)
            
        return positions