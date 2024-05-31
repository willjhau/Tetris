import pygame

class Renderer:
    def __init__(self, gameBoard):
        self.gameBoard = gameBoard
        self.width = gameBoard.width
        self.height = gameBoard.height
        self.square_size = 50
        self.margin = 10
        self.colors = {
            None: (255, 255, 255),
            True: (0, 0, 0),
            False: (255, 0, 0)
        }
        self.font = pygame.font.Font(None, 36)