from PyQt5.QtCore import QObject, pyqtSignal
import pyautogui

import actions
import actions.Action
from gui.StopDialog import StopWindow


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions_list):
        super().__init__()
        self._actions_list = actions_list
        self._current_action = None
        self._stop_flag = False

    def stop(self) -> None:
        self._stop_flag = True
        self._current_action.stop()

    def run(self) -> None:
        self._current_action: actions.Action.Action = actions.PauseAction.PauseAction(duration=1)
        self._current_action.run()

        i = 0
        while i < len(self._actions_list) and not self._stop_flag:
            self._current_action = self._actions_list[i]
            try:
                next_line = self._current_action.run()
            except pyautogui.FailSafeException:
                # mixins.PyautoguiStopMixin handles this
                break
            self._current_action._stop_flag = False
            if next_line is None:
                next_line = i + 1
            else:
                next_line -= 1  # Convert line to index
            i = next_line
        self._stop_flag = False
        self.finished.emit()


def run(actions_list: list) -> None:
    window = StopWindow(Runner, actions_list)
    window.exec_()
