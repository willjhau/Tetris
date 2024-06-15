from random import randint
from Game import square
from Game import board
from Game.Tetrominoes import tetromino, linePiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece
from InputSystems import keyboardInput
import numpy as np
import threading
import time
import config
from Renderer import arrayRenderer, renderer

class Flag:
    def __init__(self, flag=False):
        self.flag = flag
    


class Game:
    TETROMINOES = [linePiece.LinePiece,
                   jPiece.jPiece,
                   lPiece.lPiece,
                   oPiece.oPiece,
                   sPiece.sPiece,
                   tPiece.tPiece,
                   zPiece.zPiece
                     ]
    
    MOVE_LEFT = 0
    MOVE_RIGHT = 1
    SOFT_DROP = 2
    HARD_DROP = 3
    ROTATE_CLOCKWISE = 4
    ROTATE_ANTI_CLOCKWISE = 5
    ROTATE_180 = 6
    HOLD = 7

    def __init__(self, width, height, inputSystem, outputSystem, inputArgs, outputArgs):
        self.MAX_T_SIZE = max([tetromino.gridsize for tetromino in self.TETROMINOES])
        self.MAX_SPEED = config.MAX_SPEED
        self.width = width
        self.height = height
        self.board = board.GameBoard(width, height + self.MAX_T_SIZE)
        self.score = 0
        self.lines = 0
        self.speed = config.START_SPEED
        self.pivot = (0, 0)
        self.holdPiece = None
        self.nextPiece = None
        self.currentPiece = None
        self.eventQueue = []
        self.running = True
        self.holdUsed = False
        self.level = 0
        if outputArgs is None:
            self.outputSystem = outputSystem()
        else:
            self.outputSystem = outputSystem(*outputArgs)

        # on one thread, start the game loop, on another start the block fall loop
        # gameThread = threading.Thread(target=self.startGameLoop)
        blockFallThread = threading.Thread(target=self.blockFallLoop)

        inputFlag = Flag()
        if inputArgs is None:
            inputThread = threading.Thread(target=inputSystem, args=(inputFlag, self.eventQueue,), daemon=True)
        else:
            inputThread = threading.Thread(target=inputSystem, args=(inputFlag, self.eventQueue, *inputArgs), daemon=True)
        # gameThread.start()
        inputThread.start()
        blockFallThread.start()
        self.startGameLoop()
    
    def blockFallLoop(self):
        while self.running:
            self.eventQueue.insert(0, self.SOFT_DROP)
            time.sleep(1/self.speed)

    def startGameLoop(self):
        self.newPiece()
        
        while self.running:
            if len(self.eventQueue) > 0:
                event = self.eventQueue.pop(0)
                self.handleEvent(event)

            # if self.updated:
            #     self.updated = False
            #     # print(f'NEXT PIECE: {self.nextPiece}')
            #     # print(f'HOLD PIECE: {self.holdPiece}')
            #     # print(f'SCORE: {self.score}')
            #     # print(f'LINES CLEARED: {self.lines}')
            #     # # print(f'pivot: {self.pivot}')
            #     # print(self.board)
            #     arrayRenderer.terminalOutput().updateBoard(self)


    def handleEvent(self, event):
        if event == self.MOVE_LEFT:
            self.movePiece(-1)
        elif event == self.MOVE_RIGHT:
            self.movePiece(1)
        elif event == self.SOFT_DROP:
            self.softDrop()
        elif event == self.HARD_DROP:
            self.hardDrop()
        elif event == self.ROTATE_CLOCKWISE:
            self.rotatePiece(0)
        elif event == self.ROTATE_ANTI_CLOCKWISE:
            self.rotatePiece(1)
        elif event == self.ROTATE_180:
            self.rotatePiece(2)
        elif event == self.HOLD:
            self.hold()

    def hold(self):
        if self.holdUsed:
            return
        
        self.holdUsed = True

        if self.holdPiece is None:
            self.holdPiece = self.currentPiece

            currentPos = self.getCurrentPos()
            for coord in currentPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.EMPTY
                self.board.getSquare(x, y).color = None

            self.newPiece()

        else:
            temp = self.currentPiece
            self.currentPiece = self.holdPiece
            self.holdPiece = temp

            currentPos = self.getCurrentPos()
            for coord in currentPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.EMPTY
                self.board.getSquare(x, y).color = None

            coords, pivot = self.getNewPieceCoordinates()

            for coord in coords:
                x, y = coord
                if self.board.getSquare(x, y).state == square.Square.STATIC:
                    print(f"Game Over: {x}, {y}")
                    self.running = False
                    print("Game Over")
                    return
                
                self.board.getSquare(x, y).state = square.Square.VOLATILE
                self.board.getSquare(x, y).color = self.currentPiece.color
                self.pivot = pivot
            
        self.outputSystem.updateBoard(self)
        return

    def rotatePiece(self, direction):
        currentPos = self.getCurrentPos()
        nextPos = tetromino.Tetromino.rotate(currentPos, self.pivot, direction)
        canRotate = not self.checkCollision(nextPos)
        if canRotate:
            for coord in currentPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.EMPTY
                self.board.getSquare(x, y).color = None
            for coord in nextPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.VOLATILE
                self.board.getSquare(x, y).color = self.currentPiece.color
            
            self.outputSystem.updateBoard(self)


    def hardDrop(self):
        originalPos = self.getCurrentPos()
        currentPos = self.getCurrentPos()
        nextPos = [(x, y-1) for x, y in currentPos]
        

        while not self.checkCollision(nextPos):
            currentPos = nextPos
            nextPos = [(x, y-1) for x, y in currentPos]

        for coord in originalPos:
            x, y = coord
            self.board.getSquare(x, y).state = square.Square.EMPTY
            self.board.getSquare(x, y).color = None

        for coord in currentPos:
            x, y = coord
            self.board.getSquare(x, y).state = square.Square.STATIC
            self.board.getSquare(x, y).color = self.currentPiece.color
        self.clearLines()
        self.newPiece()
        self.holdUsed = False
        
        self.outputSystem.updateBoard(self)

        
    def softDrop(self):
        currentPos = self.getCurrentPos()
        nextPos = [(x, y-1) for x, y in currentPos]

        canMove = not self.checkCollision(nextPos)
        if canMove:
            for coord in currentPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.EMPTY
                self.board.getSquare(x, y).color = None
            for coord in nextPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.VOLATILE
                self.board.getSquare(x, y).color = self.currentPiece.color

            self.pivot = (self.pivot[0], self.pivot[1] - 1)

        else:
            self.lockPiece()
            self.clearLines()
            self.newPiece()
            self.holdUsed = False

        self.outputSystem.updateBoard(self)

    def clearLines(self):
        linesCleared = []
        initialLevel = self.level
        for h in range(self.height + self.MAX_T_SIZE):
            if all([self.board.getSquare(w, h).state == square.Square.STATIC for w in range(self.width)]):
                self.lines += 1
                linesCleared.append(h)
                for x in range(self.width):
                    self.board.getSquare(x, h).state = square.Square.EMPTY
                    self.board.getSquare(x, h).color = config.NULL_COLOR

        if len(linesCleared) > 0:
            self.fixLines(linesCleared)
            level = self.lines // 10

            if level > initialLevel:
                self.speed = min(self.MAX_SPEED, self.speed + config.SPEED_INCREASE)
                self.level = level
            
            if len(linesCleared) == 1:
                self.score += 40 * (self.level + 1)
            elif len(linesCleared) == 2:
                self.score += 100 * (self.level + 1)
            elif len(linesCleared) == 3:
                self.score += 300 * (self.level + 1)
            elif len(linesCleared) == 4:
                self.score += 1200 * (self.level + 1)
            
            self.outputSystem.updateBoard(self)
    
    def fixLines(self, linesCleared):
        """
        After clearing lines, move all the blocks above the cleared line down
        """
        h = linesCleared[0]
        for y in range(h, self.height + self.MAX_T_SIZE - 1):
            for x in range(self.width):
                self.board.getSquare(x, y).state = self.board.getSquare(x, y+1).state
                self.board.getSquare(x, y).color = self.board.getSquare(x, y+1).color
        for x in range(self.width):
            self.board.getSquare(x, self.height + self.MAX_T_SIZE - 1).state = square.Square.EMPTY
            self.board.getSquare(x, self.height + self.MAX_T_SIZE - 1).color = config.NULL_COLOR

        if len(linesCleared) > 1:
            linesCleared = [linesCleared[i]-1 for i in range(1, len(linesCleared))]
            self.fixLines(linesCleared)


        return

    def getCurrentPos(self):
        currentPos = []
        for h in range(self.height + self.MAX_T_SIZE):
            for w in range(self.width):
                if self.board.getSquare(w, h).state == square.Square.VOLATILE:
                    currentPos.append((w, h))
        return currentPos

    def lockPiece(self):
        currentPos = self.getCurrentPos()
        for coord in currentPos:
            x, y = coord
            self.board.getSquare(x, y).state = square.Square.STATIC
            # self.board.getSquare(x, y).color = self.currentPiece.color

    def movePiece(self, dx):
        currentPos = self.getCurrentPos()
        nextPos = [(x + dx, y) for x, y in currentPos]

        if not self.checkCollision(nextPos):
            for coord in currentPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.EMPTY
                self.board.getSquare(x, y).color = None
            for coord in nextPos:
                x, y = coord
                self.board.getSquare(x, y).state = square.Square.VOLATILE
                self.board.getSquare(x, y).color = self.currentPiece.color
        
            self.pivot = (self.pivot[0] + dx, self.pivot[1])

        self.outputSystem.updateBoard(self)

    def getNewPieceCoordinates(self):
        midpoint = self.width // 2
        return ([(x + midpoint, y + self.height) for x, y in self.currentPiece.shape],
                 (midpoint+self.currentPiece.pivot[0], self.height+self.currentPiece.pivot[1]))

    def newPiece(self):
        if self.nextPiece is None:
            self.nextPiece = self.createPiece()
        self.currentPiece = self.nextPiece
        self.nextPiece = self.createPiece()

        coords, pivot = self.getNewPieceCoordinates()

        for coord in coords:
            x, y = coord
            if self.board.getSquare(x, y).state == square.Square.STATIC:
                print(f"Game Over: {x}, {y}")
                self.running = False
                print("Game Over")
                return
            
            self.board.getSquare(x, y).state = square.Square.VOLATILE
            self.board.getSquare(x, y).color = self.currentPiece.color
            self.pivot = pivot
        
        return 
    
    def checkCollision(self, nextPos):
        for coord in nextPos:
            x, y = coord
            if y < 0:
                return True
            if x < 0 or x >= self.width or y >= (self.height + self.MAX_T_SIZE):
                return True
            if self.board.getSquare(x, y).state == square.Square.STATIC:
                return True

        return False

    def createPiece(self):
        return self.TETROMINOES[randint(0, len(self.TETROMINOES) - 1)]