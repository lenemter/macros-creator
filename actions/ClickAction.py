from time import sleep
from xml.etree import ElementTree as ET
from typing import Tuple
import pyautogui

from actions.Action import Action
from gui.EditDialogs import ClickEditDialog


def handle_move_type(move_type: str, position_x: int, position_y: int,
                     mouse_position: Tuple[int, int]) -> Tuple[int, int]:
    return x, y


class ClickAction(Action):
    name = 'Click'
    category = 'Mouse'

    def __init__(self, comment='', action='Press and release', button='Left', amount=1, interval=0,
                 move_type='Absolute', position_x=0, position_y=0, restore_cursor=False):
        self.comment = comment
        self.action = action
        self.button = button
        self.amount = int(amount)
        self.interval = float(interval)
        self.move_type = move_type
        self.position_x = int(position_x)
        self.position_y = int(position_y)
        self.restore_cursor = int(restore_cursor)  # 0 - False, 1 - True

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = ClickEditDialog.ClickEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.action, self.button, self.amount, self.interval, self.move_type,
                           self.position_x, self.position_y, self.restore_cursor) != properties
            if was_changed:
                (self.comment, self.action, self.button, self.amount, self.interval, self.move_type, self.position_x,
                 self.position_y, self.restore_cursor) = properties
            return was_changed

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'action': self.action,
                                                'button': self.button,
                                                'amount': str(self.amount),
                                                'interval': str(self.interval),
                                                'move_type': self.move_type,
                                                'position_x': str(self.position_x),
                                                'position_y': str(self.position_y),
                                                'restore_cursor': str(self.restore_cursor)})

    def run(self):
        if self.move_type == 'Absolute':
            mouse_position = pyautogui.position()
            if self.action == 'Press and release':
                pyautogui.click(x=self.position_x, y=self.position_y, clicks=self.amount, interval=self.interval,
                                button=self.button)
            elif self.action == 'Press':
                pyautogui.mouseDown(x=self.position_x, y=self.position_y, button=self.button)
            else:
                pyautogui.mouseUp(x=self.position_x, y=self.position_y, button=self.button)
            if self.restore_cursor:
                pyautogui.moveTo(*mouse_position)
        else:
            for _ in range(self.amount):
                mouse_position = pyautogui.position()
                x = mouse_position[0] + self.position_x
                y = mouse_position[1] + self.position_y
                if self.action == 'Press and release':
                    pyautogui.click(x=x, y=y, button=self.button)
                elif self.action == 'Press':
                    pyautogui.mouseDown(x=x, y=y, button=self.button)
                else:
                    pyautogui.mouseUp(x=x, y=y, button=self.button)
                if self.restore_cursor:
                    pyautogui.moveTo(*mouse_position)

                sleep(self.interval)
