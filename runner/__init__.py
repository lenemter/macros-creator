import actions
import xml.etree.ElementTree as ET
import pyautogui

from PyQt5.QtCore import QObject, pyqtSignal
from gui.StopDialog import StopWindow

# Read file ---

name_class_dict = dict()
for cls in actions.Action.Action.__subclasses__():
    name_class_dict[cls.name] = cls


def read_file(filepath: str):
    return read_file_xml(filepath)


def read_file_xml(filepath: str) -> tuple:
    actions = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    settings = root.attrib
    for child in list(root):
        child: ET.Element = child
        tag = child.tag
        attrib = child.attrib
        action = name_class_dict[tag.capitalize().replace('_', ' ')](**attrib)
        actions.append(action)

    # noinspection PyTypeChecker
    settings['time_between'] = float(settings.get('time_between', '0'))

    return actions, settings


# Write file ---

def write_file(path: str, actions: list, settings: dict = None):
    return write_file_xml(path, actions, settings)


def write_file_xml(path: str, actions: list, settings: dict):
    if settings is None:
        settings = {}
    settings = {str(x): str(y) for (x, y) in settings.items()}
    root = ET.Element('macro', settings)
    for action in actions:
        root.append(action.xml())
    tree = ET.ElementTree(root)
    tree.write(path)


# Run ---

def run(actions_list: list, settings):
    window = StopWindow(Runner, actions_list, settings)
    window.exec_()


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions_list, settings: dict):
        super().__init__()
        self._actions_list = actions_list
        self.settings = settings.copy()
        self._current_action = None
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True
        self._current_action.stop()

    def run(self):
        self._current_action = actions.PauseAction.PauseAction(duration=1)
        self._current_action.run()

        time_between = actions.PauseAction.PauseAction(duration=self.settings.get('time_between', 0.0))

        i = 0  # current action index
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
            time_between.run()
        self._stop_flag = False
        self.finished.emit()
