from xml.etree import ElementTree as ET
import pyautogui

from actions.Action import Action
from gui.EditDialogs import WriteTextEditDialog


class WriteTextAction(Action):
    name = 'Write text'
    category = 'Keyboard'

    def __init__(self, comment='', text='', amount=1, interval=0):
        self.comment = comment
        self.text = text
        self.amount = int(amount)
        self.interval = float(interval)

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = WriteTextEditDialog.WriteTextEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.text, self.amount, self.interval) != properties
            if was_changed:
                self.comment, self.text, self.amount, self.interval = properties
            return was_changed

    def xml(self) -> ET.Element:
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'text': self.text,
                                                'amount': str(self.amount),
                                                'interval': str(self.interval)})

    def run(self) -> None:
        pyautogui.typewrite(self.text * self.amount, interval=self.interval)
