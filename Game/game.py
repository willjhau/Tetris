from random import randint
from Game import square
from Game import board
from Game.Tetrominoes import tetromino, linePiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece
import numpy as np
import threading
import time
import config

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

    def __init__(self, width, height):
        self.MAX_T_SIZE = max([tetromino.gridsize for tetromino in self.TETROMINOES])
        self.MAX_SPEED = config.MAX_SPEED
        self.width = width
        self.height = height
        self.board = board.GameBoard(width, height + self.MAX_T_SIZE)
        self.score = 0
        self.lines = 0
        self.speed = config.START_SPEED
        self.holdPiece = None
        self.nextPiece = None
        self.currentPiece = None
        self.eventQueue = []
        self.updated = True
        self.running = True

        # on one thread, start the game loop, on another start the block fall loop
        gameThread = threading.Thread(target=self.startGameLoop)
        blockFallThread = threading.Thread(target=self.blockFallLoop)
        gameThread.start()
        blockFallThread.start()

    
    def blockFallLoop(self):
        while self.running:
            self.softDrop()
            time.sleep(self.speed)

    
    
    def startGameLoop(self):
        self.newPiece()
        while True:
            if len(self.eventQueue) > 0:
                event = self.eventQueue.pop(0)
                self.handleEvent(event)

            if self.updated:
                self.updated = False
                print(self.board)

    def handleEvent(self, event):
        if event == self.MOVE_LEFT:
            self.movePiece(-1, 0)
        elif event == self.MOVE_RIGHT:
            self.movePiece(1, 0)
        elif event == self.SOFT_DROP:
            self.softDrop(0, -1)
        elif event == self.HARD_DROP:
            self.hardDrop()
        elif event == self.ROTATE_CLOCKWISE:
            self.rotatePiece(1)
        elif event == self.ROTATE_ANTI_CLOCKWISE:
            self.rotatePiece(-1)
        elif event == self.ROTATE_180:
            self.rotatePiece(2)
        elif event == self.HOLD:
            self.hold()

        
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
        else:
            self.lockPiece()
            self.clearLines()
            self.newPiece()

    def clearLines(self):
        level = self.lines // 10
        for h in range(self.height + self.MAX_T_SIZE):
            if all([self.board.getSquare(w, h).state == square.Square.STATIC for w in range(self.width)]):
                self.lines += 1
                for y in range(h, self.height + self.MAX_T_SIZE - 1):
                    for x in range(self.width):
                        self.board.getSquare(x, y).state = square.Square.EMPTY
                        self.board.getSquare(x, y).color = config.NULL_COLOR
                self.fixLines()
    
    def fixLines(self):
        """
        After clearing lines, move all the blocks above the cleared line down
        """
        pass

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

    def getNewPieceCoordinates(self):
        midpoint = self.width // 2
        return [(x + midpoint, y + self.height) for x, y in self.currentPiece.shape]

    def newPiece(self):
        if self.nextPiece is None:
            self.nextPiece = self.createPiece()
        self.currentPiece = self.nextPiece
        self.nextPiece = self.createPiece()
        return 
    
    def checkCollision(self, nextPos):
        for coord in nextPos:
            x, y = coord
            if self.board.getSquare(x, y).state == square.Square.STATIC:
                return True
            if y < 0:
                return True
            if x < 0 or x >= self.width or y >= self.height:
                return True
        return False

    def createPiece(self):
        return self.TETROMINOES[randint(0, len(self.TETROMINOES) - 1)]