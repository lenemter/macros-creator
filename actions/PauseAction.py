from xml.etree import ElementTree as ET
import time

from actions.Action import Action
from gui.EditDialogs import PauseEditDialog


class PauseAction(Action):
    name = 'Pause'
    category = 'Other'

    def __init__(self, comment='', duration=1):
        self.comment = comment
        self.duration = float(duration)
        self._stop_flag = False

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = PauseEditDialog.PauseEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.duration) != properties
            if was_changed:
                self.comment, self.duration = properties
            return was_changed

    def xml(self) -> ET.Element:
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'duration': str(self.duration)})

    def run(self) -> None:
        for _ in range(int(self.duration // 0.25)):
            if self._stop_flag:
                return None
            time.sleep(0.25)

        if self._stop_flag:
            return None
        time.sleep(self.duration % 0.25)

    def stop(self) -> None:
        self._stop_flag = True
