import pyautogui


class PyautoguiStopMixin:
    def stop(self):
        position = pyautogui.position()
        self.__stop_flag = True
        pyautogui.FAILSAFE = True
        try:
            while True:
                pyautogui.FAILSAFE = True
                pyautogui.moveTo(x=0, y=0)
        except pyautogui.FailSafeException:
            pass

    def reset_stop(self):
        self.__stop_flag = False
        pyautogui.FAILSAFE = False
