from Game import game
from InputSystems import keyboardInput
from Renderer import arrayRenderer, renderer

if __name__ == '__main__':
    # newGame = game.Game(10, 20, keyboardInput.TerminalInput, arrayRenderer.terminalOutput, None, None)
    newGame = game.Game(10, 20, keyboardInput.TerminalInput, renderer.Renderer, None, (10, 20))


