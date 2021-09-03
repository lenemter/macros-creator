from time import sleep
from xml.etree import ElementTree as ET
import pyautogui

from actions.Action import Action
from gui.EditDialogs import PressKeyEditDialog


class PressKeyAction(Action):
    name = 'Press key'
    category = 'Keyboard'

    def __init__(self, comment='', key='', action='Press and release', amount=1, interval=0):
        self.comment = comment
        self.key = key
        self.action = action
        self.amount = int(amount)
        self.interval = float(interval)

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = PressKeyEditDialog.PressKeyEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.key, self.action, self.amount, self.interval) != properties
            if was_changed:
                self.comment, self.key, self.action, self.amount, self.interval = properties
            return was_changed

    def xml(self) -> ET.Element:
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'key': self.key,
                                                'action': self.action,
                                                'amount': str(self.amount),
                                                'interval': str(self.interval)})

    def run(self) -> None:
        if self.action == 'Press and release':
            for _ in range(self.amount):
                pyautogui.typewrite(self.key)
                sleep(self.interval)
        elif self.action == 'Press':
            pyautogui.keyDown(self.key)
        else:
            pyautogui.keyUp(self.key)
