import pygame
from random import randint
from . import board, square
from .Tetrominoes import tetromino, linePiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece
import numpy as np

class Game:
    TETROMINOES = [linePiece.LinePiece,
                   jPiece.jPiece,
                   lPiece.lPiece,
                   oPiece.oPiece,
                   sPiece.sPiece,
                   tPiece.tPiece,
                   zPiece.zPiece
                     ]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = board.GameBoard(width, height+4)
        self.score = 0
        self.lines = 0
        self.holdPiece = None
        self.nextPiece = None
        self.currentPiece = None
    
    def startGameLoop(self):
        self.new_piece()

    def getNewPieceCoordinates(self):
        pass

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