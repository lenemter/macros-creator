import sys
import pyautogui


class PyautoguiStopMixin:
    def stop(self) -> None:
        self._stop_flag = True
        pyautogui.FAILSAFE = True
        stderr = sys.stderr
        position = pyautogui.position()
        # sys.stderr stuff for suppressing exception
        while True:
            try:
                pyautogui.moveTo(x=0, y=0, duration=0)
            except pyautogui.FailSafeException:
                sys.stderr = object
                break
        sys.stderr = stderr
        pyautogui.FAILSAFE = False
        # move cursor to previous location
        if (position.x, position.y) != (0, 0):
            pyautogui.moveTo(x=position.x, y=position.y, duration=0)


class NoStopMixin:
    @staticmethod
    def stop() -> None:
        pass
