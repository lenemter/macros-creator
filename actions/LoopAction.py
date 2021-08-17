from xml.etree import ElementTree as ET

from actions.Action import Action
from gui.EditDialogs import LoopEditDialog


class LoopAction(Action):
    name = 'Loop'
    category = 'Other'

    def __init__(self, comment='', loop_start=0, count=5):
        self.comment = comment
        self.loop_start = int(loop_start)
        self.count = int(count)

    def open_edit_dialog(self, parent):
        edit_dialog = LoopEditDialog.LoopEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            self.comment = edit_dialog.comment_lineEdit.text()
            self.loop_start = int(edit_dialog.loop_start_comboBox.currentText())
            self.count = edit_dialog.count_spinBox.value()

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'loop_start': str(self.loop_start),
                                                'count': str(self.count)})

    def run(self):
        if self.count == 0:
            return None
        self.count -= 1
        return self.loop_start