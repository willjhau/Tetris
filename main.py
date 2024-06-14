from Game import game
from InputSystems import keyboardInput
from Renderer import arrayRenderer

if __name__ == '__main__':
    newGame = game.Game(10, 20, keyboardInput.TerminalInput, arrayRenderer.terminalOutput)