import pygame
from Renderer import outputSystem
import config
import numpy as np
import threading
import time

class Renderer(outputSystem.OutputSystem):
    def __init__(self, width, height):
        self.debugCounter = 0

        self.width = width
        self.height = height + 4
        self.SQUARE_SIZE = config.SQUARE_SIZE
        self.MARGIN = config.MARGIN
        self.NULL_COLOR = config.NULL_COLOR
        self.FONT_SIZE = config.FONT_SIZE
        self.FONT_COLOR = config.FONT_COLOR
        self.SEPARATOR = config.SEPARATOR
        self.BACKGROUND_COLOR = config.BACKGROUND_COLOR

        width = (self.width * (self.SQUARE_SIZE + self.MARGIN) +
                                            self.MARGIN+ 
                                            self.SEPARATOR * 4+
                                            (self.SQUARE_SIZE + self.MARGIN) * 8+ # 4 for the next and hold pieces each
                                            self.MARGIN * 2)
        
        height = (self.height * (self.SQUARE_SIZE + self.MARGIN) +
                                             self.MARGIN +
                                             self.SEPARATOR * 2 +
                                             self.FONT_SIZE * 2)
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.clock = pygame.time.Clock()
        
        pygame.font.init()
        self.font = pygame.font.SysFont(None, self.FONT_SIZE)
        pygame.display.set_caption('Tetris')

        self.eventQueueClearerThread = threading.Thread(target=self.eventQueueClearer)
        self.eventQueueClearerThread.start()

    def eventQueueClearer(self):
        while True:
            pygame.event.clear()
            time.sleep(0.1)

    def drawScreen(self, gameClass):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            else:
                pass


        self.screen.fill(self.BACKGROUND_COLOR)

        # Draw the sillhouette of the piece if it were to be hard dropped
        currentPos = gameClass.getCurrentPos()[:] # Copy the list
        nextPos = [(x, y-1) for x, y in currentPos]
        while (currentPos != []) and (not gameClass.checkCollision(nextPos)):
            currentPos = nextPos
            nextPos = [(x, y-1) for x, y in currentPos]
        for square in currentPos:
            pygame.draw.rect(self.screen,
                             (255, 255, 255),
                             [(self.MARGIN + self.SQUARE_SIZE) * square[0] +
                               self.SEPARATOR * 2 +
                               4 * (self.SQUARE_SIZE + self.MARGIN) + self.MARGIN,
                              (self.MARGIN + self.SQUARE_SIZE) * (gameClass.height-square[1]+3) +
                               self.FONT_SIZE * 2 + 
                               self.SEPARATOR,
                              self.SQUARE_SIZE+self.MARGIN*2,
                              self.SQUARE_SIZE+self.MARGIN*2])

        # Draw the board
        flippedBoard = gameClass.board.board[::-1]
        for rowI, rowV  in enumerate(flippedBoard):
            for col, square in enumerate(rowV):
                c = square.color
                if c == None:
                    c = self.NULL_COLOR
                pygame.draw.rect(self.screen,
                                 c,
                                 [(self.MARGIN + self.SQUARE_SIZE) * col +
                                   self.SEPARATOR * 2 + self.MARGIN +
                                   4 * (self.SQUARE_SIZE + self.MARGIN) + self.MARGIN,
                                  (self.MARGIN + self.SQUARE_SIZE) * rowI + self.MARGIN +
                                   self.FONT_SIZE * 2 + 
                                   self.SEPARATOR,
                                  self.SQUARE_SIZE,
                                  self.SQUARE_SIZE])
        
        # Draw the next piece
        # Draw the text
        text = self.font.render('NEXT:', True, self.FONT_COLOR)
        self.screen.blit(text,
                         (self.width * (self.SQUARE_SIZE + self.MARGIN) + 
                                self.MARGIN +
                                self.SEPARATOR * 3 + 
                                4* (self.SQUARE_SIZE+ self.MARGIN) + 
                                self.MARGIN, 
                                
                                self.FONT_SIZE*2 + self.SEPARATOR))
        # Draw the piece
        nextGrid = np.full((gameClass.nextPiece.gridsize,
                             gameClass.nextPiece.gridsize), '.')
        nextCenter = (int(gameClass.nextPiece.gridsize / 2), 0)
        for square in gameClass.nextPiece.shape:
            nextGrid[gameClass.nextPiece.gridsize-(nextCenter[1]+
                     square[1])-1][nextCenter[0]+
                                square[0]] = 'o'
        for row in range(gameClass.nextPiece.gridsize):
            for column in range(gameClass.nextPiece.gridsize):
                c = self.NULL_COLOR
                if nextGrid[row][column] == 'o':
                    c = gameClass.nextPiece.color
                pygame.draw.rect(self.screen,
                                 c,
                                 [self.width * (self.SQUARE_SIZE + self.MARGIN) + 
                                self.MARGIN +
                                self.SEPARATOR * 3 + 
                                4* (self.SQUARE_SIZE+ self.MARGIN) + 
                                self.MARGIN + column * (self.SQUARE_SIZE + self.MARGIN),

                                self.FONT_SIZE*3 + 
                                self.SEPARATOR +
                                row * (self.SQUARE_SIZE + self.MARGIN),
                                  self.SQUARE_SIZE,
                                  self.SQUARE_SIZE])
        
        # Draw the hold piece
        # Draw the text
        text = self.font.render('HOLD:', True, self.FONT_COLOR)
        self.screen.blit(text,
                         (self.SEPARATOR,
                            self.FONT_SIZE*2 + self.SEPARATOR)) 
        # Draw the piece
        holdGrid = np.full((4, 4), '.')
        gridsize = 4
        c = self.NULL_COLOR
        if gameClass.holdPiece is not None:
            gridsize = gameClass.holdPiece.gridsize
            c = gameClass.holdPiece.color
            holdCenter = (int(gameClass.holdPiece.gridsize / 2), 0)
            holdGrid = np.full((gameClass.holdPiece.gridsize,
                                gameClass.holdPiece.gridsize), '.')
            for square in gameClass.holdPiece.shape:
                holdGrid[gameClass.nextPiece.gridsize-(holdCenter[1]+square[1])-1][holdCenter[0]+
                                    square[0]] = 'o'  
        
        for row in range(gridsize):
            for column in range(gridsize):
                c = self.NULL_COLOR
                if holdGrid[row][column] == 'o':
                    c = gameClass.holdPiece.color
                pygame.draw.rect(self.screen,
                                    c,
                                    [self.SEPARATOR + column * (self.SQUARE_SIZE + self.MARGIN),
                                    self.FONT_SIZE*3 + self.SEPARATOR + row * (self.SQUARE_SIZE + self.MARGIN),
                                    self.SQUARE_SIZE,
                                    self.SQUARE_SIZE]) 

        # Draw the score
        text = self.font.render('SCORE: ' + str(gameClass.score), True, self.FONT_COLOR)
        self.screen.blit(text, (self.SEPARATOR, self.SEPARATOR))

        # Draw the number of lines
        text = self.font.render('LINES: ' + str(gameClass.lines), True, self.FONT_COLOR)
        self.screen.blit(text, (self.SEPARATOR, self.SEPARATOR + self.FONT_SIZE))

        # Draw the pivot point as a circle centered in the pivot point
        # pygame.draw.circle(self.screen, (255, 255, 255), 
        #                     [self.SEPARATOR * 2 + self.MARGIN + 4 * (self.SQUARE_SIZE + self.MARGIN) + self.MARGIN + gameClass.pivot[0] * (self.SQUARE_SIZE + self.MARGIN) + int(self.SQUARE_SIZE / 2),
        #                     self.SEPARATOR + self.MARGIN + self.FONT_SIZE * 2 + (gameClass.height-gameClass.pivot[1]+3) * (self.SQUARE_SIZE + self.MARGIN) + int(self.SQUARE_SIZE / 2)], 
        #                     int(self.SQUARE_SIZE / 2))


              
        
        pygame.display.flip()

        self.clock.tick(30)

    def updateBoard(self, gameClass):
        self.drawScreen(gameClass)

    def updateNextPiece(self, gameClass):
        self.drawScreen(gameClass)

    def updateHoldPiece(self, gameClass):
        self.drawScreen(gameClass)

    def updateScore(self, gameClass):
        self.drawScreen(gameClass)

    def updateLines(self, gameClass):
        self.drawScreen(gameClass)

    def updateGameOver(self, gameClass):
        # Draw GAME OVER in red text in the center of the screen
        text = self.font.render('GAME OVER', True, (255, 0, 0))
        self.screen.blit(text, (self.width * (self.SQUARE_SIZE + self.MARGIN) / 2, self.height / 2))
        pygame.display.flip()