from PyQt5.QtCore import QObject, pyqtSignal
from gui.StopDialog import StopWindow
import pyautogui
from time import sleep
import sys


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions):
        super().__init__()
        self.actions = actions

    def close(self):
        pyautogui.FAILSAFE = True
        stderr = sys.stderr
        position = pyautogui.position()
        while True:
            try:
                pyautogui.moveTo(x=0, y=0, duration=0)
            except pyautogui.FailSafeException:
                sys.stderr = object
                break
        # sys.stderr stuff for suppressing exception
        sys.stderr = stderr
        pyautogui.FAILSAFE = False
        # move cursor to previous location
        if (position.x, position.y) != (0, 0):
            pyautogui.moveTo(x=position.x, y=position.y, duration=0)

    def run(self):
        sleep(1)
        i = 0
        while i < len(self.actions):
            try:
                next_line = self.actions[i].run()
            except pyautogui.FailSafeException:
                # it will be closed in close()
                break
            if next_line is None:
                next_line = i + 1
            else:
                next_line -= 1  # Convert line to index
            i = next_line
        self.finished.emit()


def run(actions):
    window = StopWindow(Runner, actions)
    window.exec_()
