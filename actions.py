from abc import ABC, abstractmethod
import xml.etree.ElementTree as ET
import pyautogui
from typing import Tuple

from gui.EditDialogs import ClickEditDialog, MoveCursorEditDialog, CursorPathEditDialog, KeySequenceEditDialog, \
    WriteTextEditDialog, SleepEditDialog, LoopEditDialog


def handle_move_type(move_type: str, position_x: int, position_y: int,
                     mouse_position: Tuple[int, int]) -> Tuple[int, int]:
    if move_type == 'Absolute':
        x = position_x
        y = position_y
    else:
        x = mouse_position[0] + position_x
        y = mouse_position[1] + position_y

    return x, y


class Action(ABC):
    name = None
    category = None

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def open_edit_dialog(self, parent):
        raise NotImplementedError

    def get_xml_name(self):
        return self.name.lower().replace(' ', '_')

    @abstractmethod
    def xml(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


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

    def open_edit_dialog(self, parent):
        edit_dialog = ClickEditDialog.ClickEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            (self.comment, self.action, self.button, self.amount, self.interval, self.move_type, self.position_x,
             self.position_y, self.restore_cursor) = properties

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
        mouse_position = pyautogui.position()
        x, y = handle_move_type(self.move_type, self.position_x, self.position_y, mouse_position)

        if self.action == 'Press and release':
            pyautogui.click(x=x, y=y, clicks=self.amount, interval=self.interval, button=self.button)
        elif self.action == 'Press':
            pyautogui.mouseDown(x=x, y=y, button=self.button)
        else:
            pyautogui.mouseUp(x=x, y=y, button=self.button)

        if self.restore_cursor:
            pyautogui.moveTo(*mouse_position)


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


class CursorPathAction(Action):
    name = 'Cursor path'
    category = 'Mouse'

    def __init__(self, comment='', move_type='Absolute', path=None):
        if path is None:
            path = []
        if type(path) == str:
            path = eval(path)  # Sorry.
        self.comment = comment
        self.move_type = move_type
        self.path = path

    def open_edit_dialog(self, parent):
        edit_dialog = CursorPathEditDialog.CursorPathEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            self.comment = edit_dialog.comment_lineEdit.text()
            self.move_type = edit_dialog.move_type_comboBox.currentText()
            self.path = edit_dialog.table.get_points_list()

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'move_type': self.move_type,
                                                'path': str(self.path)})

    def run(self):
        # TODO
        super().run()


class KeySequenceAction(Action):
    name = 'Key sequence'
    category = 'Keyboard'

    def __init__(self, comment='', key_sequence='', action='Press and release', amount=1, interval=0):
        self.comment = comment
        self.key_sequence = key_sequence
        self.action = action
        self.amount = int(amount)
        self.interval = float(interval)

    def open_edit_dialog(self, parent):
        edit_dialog = KeySequenceEditDialog.KeySequenceEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            self.comment = edit_dialog.comment_lineEdit.text()
            self.key_sequence = edit_dialog.key_sequence_lineEdit.text()
            self.action = edit_dialog.action_comboBox.currentText()
            self.amount = edit_dialog.amount_spinBox.value()

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'key_sequence': self.key_sequence,
                                                'action': self.action,
                                                'amount': str(self.amount)})

    def run(self):
        super().run()


class WriteTextAction(Action):
    name = 'Write text'
    category = 'Keyboard'

    def __init__(self, comment='', text='', amount=1):
        self.comment = comment
        self.text = text
        self.amount = int(amount)

    def open_edit_dialog(self, parent):
        edit_dialog = WriteTextEditDialog.WriteTextEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            self.comment = edit_dialog.comment_lineEdit.text()
            self.text = edit_dialog.text_textEdit.toPlainText()
            self.amount = edit_dialog.amount_spinBox.value()

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'text': self.text,
                                                'amount': str(self.amount)})

    def run(self):
        super().run()


class SleepAction(Action):
    name = 'Sleep'
    category = 'Other'

    def __init__(self, comment='', duration=1):
        self.comment = comment
        self.duration = float(duration)

    def open_edit_dialog(self, parent):
        edit_dialog = SleepEditDialog.SleepEditDialog(parent, self)
        edit_dialog.exec_()

        if edit_dialog.user_clicked_ok:
            self.comment = edit_dialog.comment_lineEdit.text()
            self.duration = edit_dialog.duration_doubleSpinBox.value()

    def xml(self):
        return ET.Element(self.get_xml_name(), {'comment': self.comment,
                                                'duration': str(self.duration)})

    def run(self):
        from time import sleep

        sleep(self.duration)


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
        super().run()