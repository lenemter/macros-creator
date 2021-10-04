from xml.etree import ElementTree as ET
import pyautogui
from collections import UserList

from actions.Action import Action
from . import mixins
from gui.EditDialogs import CursorPathEditDialog


class Path(UserList):
    def __init__(self, path_str=None):
        super().__init__()
        if path_str is None:
            return
        tuples = path_str.split(' ')
        for t in tuples:
            x, y = [int(x) for x in t.split(',')]
            self.data.append((x, y))


def convert(path: Path):
    return ' '.join([f'{x},{y}' for (x, y) in path])


class CursorPathAction(mixins.PyautoguiStopMixin, Action):
    name = 'Cursor path'
    category = 'Mouse'

    def __init__(self, comment='', move_type='Absolute', duration=0, button='None', path=None):
        self.comment = comment
        self.move_type = move_type
        self.duration = float(duration)
        self.button = button
        if path is None:
            path = Path()
        elif type(path) == str:
            path = Path(path)
        self.path = path

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = CursorPathEditDialog.CursorPathEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.move_type, self.duration, self.button, self.path) != properties
            if was_changed:
                self.comment, self.move_type, self.duration, self.button, self.path = properties
            return was_changed

    def xml(self) -> ET.Element:
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'move_type': self.move_type,
                                                'duration': str(self.duration),
                                                'button': self.button,
                                                'path': convert(self.path)})

    def run(self):
        if self.path:
            if self.button != 'None':
                pyautogui.mouseDown(self.button)
            if self.move_type == 'Absolute':
                for x, y in self.path:
                    pyautogui.moveTo(x=x, y=y, duration=self.duration)
            else:
                for x, y in self.path:
                    pyautogui.moveRel(x=x, y=y, duration=self.duration)
            if self.button != 'None':
                pyautogui.mouseUp(self.button)
