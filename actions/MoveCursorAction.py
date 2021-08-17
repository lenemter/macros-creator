from xml.etree import ElementTree as ET
import pyautogui

from actions.Action import Action
from gui.EditDialogs import MoveCursorEditDialog


class MoveCursorAction(Action):
    name = 'Move cursor'
    category = 'Mouse'

    def __init__(self, comment='', move_type='Absolute', position_x=-1, position_y=-1, duration=0, button='None'):
        self.comment = comment
        self.move_type = move_type
        self.position_x = int(position_x)
        self.position_y = int(position_y)
        self.duration = float(duration)
        self.button = button

    def open_edit_dialog(self, parent):
        edit_dialog = MoveCursorEditDialog.MoveCursorEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            self.comment, self.move_type, self.position_x, self.position_y, self.duration, self.button = properties

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'move_type': self.move_type,
                                                'position_x': str(self.position_x),
                                                'position_y': str(self.position_y),
                                                'duration': str(self.duration),
                                                'button': self.button})

    def run(self):
        if self.button == 'None':
            if self.move_type == 'Absolute':
                pyautogui.moveTo(x=self.position_x, y=self.position_y, duration=self.duration)
            else:
                pyautogui.move(x=self.position_x, y=self.position_y, duration=self.duration)
        else:
            if self.move_type == 'Absolute':
                pyautogui.dragTo(x=self.position_x, y=self.position_y, duration=self.duration, button=self.button)
            else:
                pyautogui.drag(x=self.position_x, y=self.position_y, duration=self.duration, button=self.button)