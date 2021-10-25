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

def write_file(path, actions: list, settings: dict):
    return write_file_xml(path, actions, settings)


def write_file_xml(path, actions: list, settings: dict):
    settings = {str(x): str(y) for (x, y) in settings.items()}
    root = ET.Element('macro', settings)
    for action in actions:
        a = action.xml()
        root.append(a)
    tree = ET.ElementTree(root)
    tree.write(path)


def write_file_db(path, actions: list, settings: dict):
    import sqlite3

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE settings ('
                   'name TEXT PRIMARY KEY,'
                   'value TEXT);')
    cursor.execute('CREATE TABLE macro ('
                   'name TEXT PRIMARY KEY,'
                   'parameters TEXT);')
    for action in actions:
        cursor.execute()

# Run ---

def run(actions_list: list, settings):
    window = StopWindow(Runner, actions_list, settings)
    window.exec()


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
        self.__current_action.stop()

    def run(self):
        time_between = actions.PauseAction.PauseAction(duration=self.__settings.get('time_between', 0.0))
        self.__current_action = actions.PauseAction.PauseAction(duration=1)
        self.__current_action.run()

        i = 0  # current action index
        while i < len(self.__actions_list) and not self.__stop_flag:
            self.__current_action = self.__actions_list[i]  # get action
            self.__current_action.__stop_flag = False  # reset stop flag
            next_line = self.__current_action.run()  # run
            next_line = i + 1 if next_line is None else next_line - 1  # get next index
            i = next_line
            time_between.run()
        self.__stop_flag = False
        self.finished.emit()
