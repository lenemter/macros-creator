from gui.StopDialog import StopDialog
from PyQt5.QtCore import QObject, pyqtSignal
import pyautogui

import actions


def run(actions_list: list, settings: dict) -> int:
    window = StopDialog(Runner, actions_list, settings)
    return window.exec()


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions_list, settings: dict):
        super().__init__()

        self.__actions_list = actions_list.copy()
        self.__settings = settings.copy()
        self.__current_action = None
        self.__stop_flag = False

    def stop(self):
        self.__stop_flag = True
        if self.__current_action != -1:  # bug fix. i have no idea why it works
            self.__current_action.stop()

    def run(self):
        time_between = actions.PauseAction(duration=self.__settings['time_between'])
        self.__current_action = actions.PauseAction(duration=1)
        self.__current_action.run()

        i = 0  # current action index
        while i < len(self.__actions_list) and not self.__stop_flag:
            self.__current_action = self.__actions_list[i]  # get action
            try:
                next_line = self.__current_action.run()  # run
            except pyautogui.FailSafeException:
                break
            next_line = i + 1 if next_line is None else next_line - 1  # get next index
            i = next_line
            time_between.run()

        self.__current_action = -1

        for action in self.__actions_list:
            action.reset_stop()

        self.__stop_flag = False
        self.finished.emit()
