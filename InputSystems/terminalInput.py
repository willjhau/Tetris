from pynput import keyboard
from Game import game

class TerminalInput:
    # CONTROLS
    MOVE_LEFT = keyboard.Key.left
    MOVE_RIGHT = keyboard.Key.right
    SOFT_DROP = keyboard.Key.down
    HARD_DROP = keyboard.Key.up
    ROTATE_CLOCKWISE = keyboard.KeyCode.from_char('r')
    ROTATE_ANTI_CLOCKWISE = keyboard.KeyCode.from_char('e')
    ROTATE_180 = keyboard.KeyCode.from_char('w')
    HOLD = keyboard.KeyCode.from_char('q')
    ESCAPE = keyboard.Key.esc

    def __init__(self, eventQueue):
        self.eventQueue = eventQueue
        keyboard.Listener(on_press=self.on_press).start()

    def on_press(self, key):
        if key == TerminalInput.ESCAPE:
            # Stop listener
            return False
        elif key == TerminalInput.MOVE_LEFT:
            self.eventQueue.append(game.Game.MOVE_LEFT)
        elif key == TerminalInput.MOVE_RIGHT:
            self.eventQueue.append(game.Game.MOVE_RIGHT)
        elif key == TerminalInput.SOFT_DROP:
            self.eventQueue.append(game.Game.SOFT_DROP)
        elif key == TerminalInput.HARD_DROP:
            self.eventQueue.append(game.Game.HARD_DROP)
        elif key == TerminalInput.ROTATE_CLOCKWISE:
            self.eventQueue.append(game.Game.ROTATE_CLOCKWISE)
        elif key == TerminalInput.ROTATE_ANTI_CLOCKWISE:
            self.eventQueue.append(game.Game.ROTATE_ANTI_CLOCKWISE)
        elif key == TerminalInput.ROTATE_180:
            self.eventQueue.append(game.Game.ROTATE_180)
        elif key == TerminalInput.HOLD:
            self.eventQueue.append(game.Game.HOLD)
if __name__ == "__main__":
    terminalInput = TerminalInput()