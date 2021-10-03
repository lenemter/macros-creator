from xml.etree import ElementTree as ET
from typing import Optional

from actions.Action import Action
from gui.EditDialogs import LoopEditDialog


class LoopAction(Action):
    name = 'Loop'
    category = 'Other'

    def __init__(self, comment='', loop_start=0, count=5):
        self.comment = comment
        self.loop_start = int(loop_start)
        self.count = int(count)
        self._count = self.count
        self._stop_flag = False

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = LoopEditDialog.LoopEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.loop_start, self.count) != properties
            if was_changed:
                self.comment, self.loop_start, self.count = properties
            return was_changed

    def xml(self) -> ET.Element:
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'loop_start': str(self.loop_start),
                                                'count': str(self.count)})

    def run(self) -> Optional[int]:
        if self._count == 0 or self._stop_flag:
            self._count = self.count
            return None
        self._count -= 1
        return self.loop_start

    def stop(self):
        self._stop_flag = True
