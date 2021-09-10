from xml.etree import ElementTree as ET
import pyautogui

from actions.Action import Action
from . import mixins
from gui.EditDialogs import CursorPathEditDialog


class CursorPathAction(mixins.PyautoguiStopMixin, Action):
    name = 'Cursor path'
    category = 'Mouse'

    def __init__(self, comment='', move_type='Absolute', duration=0, button='None', path=None):
        self.comment = comment
        self.move_type = move_type
        self.duration = float(duration)
        self.button = button
        if path is None:
            path = []
        if type(path) == str:
            path = eval(path)  # Sorry. Wait there is actually a vulnerability # todo: fix it
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
                                                'path': str(self.path)})

    def run(self) -> None:
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
