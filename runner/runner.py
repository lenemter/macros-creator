from gui.StopDialog import StopDialog
from PyQt5.QtCore import QObject, pyqtSignal
import pyautogui

from actions import PauseAction


def run(actions_list: list, settings: dict) -> int:
    window = StopDialog(Runner, actions_list, settings)
    return window.exec()


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions: list, settings: dict):
        super().__init__()

        self.__actions = actions.copy()
        self.__settings = settings.copy()
        self.__current_action = None
        self.__stop_flag = False

    def stop(self):
        self.__stop_flag = True
        if self.__current_action is not None:
            self.__current_action.stop()

    def run(self):
        actions = self.__actions

        time_between = PauseAction(duration=self.__settings['time_between'])
        self.__current_action = PauseAction(duration=1)
        self.__current_action.run()

        i = 0  # current action index
        while i < len(actions) and not self.__stop_flag:
            self.__current_action = actions[i]  # get action
            try:
                next_line = self.__current_action.run()  # run
            except pyautogui.FailSafeException:
                break
            next_line = i + 1 if next_line is None else next_line - 1  # get next index
            i = next_line
            time_between.run()

        self.__current_action = None
        self.__stop_flag = False
        for action in self.__actions:
            action.reset_stop()
        self.finished.emit()
