import xml.etree.ElementTree as ET
import pyautogui
from PyQt5.QtCore import QObject, pyqtSignal

import actions
from gui.StopDialog import StopWindow

# Read file ---

name_class_dict = dict()
for cls in actions.Action.Action.__subclasses__():
    name_class_dict[cls.name] = cls


def read_file_xml(filepath: str) -> tuple:
    actions_list = []
    tree = ET.parse(filepath)
    root = tree.getroot()
    settings = root.attrib
    for child in list(root):
        child = child
        tag = child.tag
        attrib = child.attrib
        action = name_class_dict[tag.capitalize().replace('_', ' ')](**attrib)  # create action
        actions_list.append(action)

    # noinspection PyTypeChecker
    settings['time_between'] = float(settings.get('time_between', 0.0))

    return actions_list, settings


# Write file ---

def write_file_xml(path, actions_list: list, settings: dict):
    settings = {str(x): str(y) for (x, y) in settings.items()}

    root = ET.Element('macro', settings)
    for action in actions_list:
        a = action.xml()
        root.append(a)
    tree = ET.ElementTree(root)
    with open(path, mode='wb') as file:
        tree.write(file, encoding='UTF-8')


def write_file_db(path, actions_list: list, settings: dict):
    import sqlite3

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE settings ('
                   'name TEXT PRIMARY KEY,'
                   'value TEXT)')
    cursor.execute('CREATE TABLE macro ('
                   'name TEXT PRIMARY KEY,'
                   'parameters TEXT)')

    for (setting, value) in settings.items():
        cursor.execute('INSERT INTO settings (name, value)'
                       'VALUES (?, ?)',
                       (setting, value))
    for action in actions_list:
        cursor.execute('INSERT INTO macro (name, parameters)'
                       'VALUES (?, ?)',
                       (action.name,))


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
        if self.__current_action != -1:  # bug fix. i have no idea why it works
            self.__current_action.stop()

    def run(self):
        time_between = actions.PauseAction.PauseAction(duration=self.__settings.get('time_between', 0.0))
        self.__current_action = actions.PauseAction.PauseAction(duration=1)
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
