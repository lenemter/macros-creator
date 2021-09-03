from time import sleep
from xml.etree import ElementTree as ET

from actions.Action import Action
from gui.EditDialogs import PauseEditDialog


class PauseAction(Action):
    name = 'Pause'
    category = 'Other'

    def __init__(self, comment='', duration=1):
        self.comment = comment
        self.duration = float(duration)

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = PauseEditDialog.PauseEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.duration) != properties
            if was_changed:
                self.comment, self.duration = properties
            return was_changed

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'duration': str(self.duration)})

    def run(self):
        sleep(self.duration)
