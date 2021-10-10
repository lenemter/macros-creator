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
    read_file_xml(filepath)


def read_file_xml(filepath: str) -> list:
    actions = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    for child in list(root):
        child: ET.Element = child
        tag = child.tag
        attrib = child.attrib
        action = name_class_dict[tag.capitalize().replace('_', ' ')](**attrib)
        actions.append(action)
    return actions


# Write file ---

def write_file(path: str, actions: list):
    write_file_xml(path, actions)


def write_file_xml(path: str, actions: list):
    root = ET.Element('macro')
    for action in actions:
        root.append(action.xml())
    tree = ET.ElementTree(root)
    tree.write(path)


# Run ---

def run(actions_list: list):
    window = StopWindow(Runner, actions_list)
    window.exec_()


class Runner(QObject):
    finished = pyqtSignal()

    def __init__(self, actions_list):
        super().__init__()
        self._actions_list = actions_list
        self._current_action = None
        self._stop_flag = False

    def stop(self):
        self._stop_flag = True
        self._current_action.stop()

    def run(self):
        self._current_action = actions.PauseAction.PauseAction(duration=1)
        self._current_action.run()

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
        self._stop_flag = False
        self.finished.emit()
