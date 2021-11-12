import pyautogui


class PyautoguiStopMixin:
    def stop(self):
        position = pyautogui.position()
        self.__stop_flag = True
        if hasattr(self, '__pause_action'):
            self.__pause_action.reset_stop()
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
        if hasattr(self, '__pause_action'):
            self.__pause_action.reset_stop()
