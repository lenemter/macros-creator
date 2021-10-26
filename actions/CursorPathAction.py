from xml.etree import ElementTree as ET
import pyautogui

from actions.Action import Action
from . import mixins
from gui.EditDialogs import CursorPathEditDialog


def load_mouse_path(mouse_path: str) -> list:
    if not mouse_path:
        return []

    result = []
    tuples = mouse_path.split(' ')
    try:
        for tuple_str in tuples:
            x, y = [int(x) for x in tuple_str.split(',')]
            result.append((x, y))
    except ValueError:
        return []
    return result


def export_mouse_path(mouse_path: list) -> str:
    return ' '.join([f'{x},{y}' for (x, y) in mouse_path])


class CursorPathAction(mixins.PyautoguiStopMixin, Action):
    name = 'Cursor path'
    category = 'Mouse'

    def __init__(self, comment='', move_type='Absolute', duration=0, button='None', mouse_path=None):
        self.comment = comment
        self.move_type = move_type
        self.duration = float(duration)
        self.button = button
        if mouse_path is None:
            mouse_path = load_mouse_path('')
        elif isinstance(mouse_path, str):
            mouse_path = load_mouse_path(mouse_path)
        else:
            raise ValueError(f'Could not parse mouse_path: {mouse_path}')
        self.mouse_path = mouse_path

    @property
    def parameters(self):
        return {'comment': self.comment,
                'move_type': self.move_type,
                'duration': self.duration,
                'button': self.button,
                'path': export_mouse_path(self.mouse_path)}

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = CursorPathEditDialog.CursorPathEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.move_type, self.duration, self.button, self.mouse_path) != properties
            if was_changed:
                self.comment, self.move_type, self.duration, self.button, self.mouse_path = properties
            return was_changed

    def run(self):
        if self.mouse_path:
            if self.button != 'None':
                pyautogui.mouseDown(self.button)

            if self.move_type == 'Absolute':
                for x, y in self.mouse_path:
                    pyautogui.moveTo(x=x, y=y, duration=self.duration)
            elif self.move_type == 'Relative':
                for x, y in self.mouse_path:
                    pyautogui.moveRel(x=x, y=y, duration=self.duration)
            else:
                raise ValueError(f'Unknown move type: {self.move_type}')

            if self.button != 'None':
                pyautogui.mouseUp(self.button)
