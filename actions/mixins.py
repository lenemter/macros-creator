import sys
from contextlib import suppress
import pyautogui


class PyautoguiStopMixin:
    # noinspection PyUnreachableCode
    def stop(self):
        self._stop_flag = True
        pyautogui.FAILSAFE = True
        position = pyautogui.position()
        with suppress(pyautogui.FailSafeException):
            while True:
                pyautogui.moveTo(x=0, y=0)
        pyautogui.FAILSAFE = False
        # move cursor to previous location
        if (position.x, position.y) != (0, 0):
            pyautogui.moveTo(x=position.x, y=position.y)
