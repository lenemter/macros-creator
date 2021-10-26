import pyautogui

from actions.Action import Action
from . import mixins
from gui.EditDialogs import MoveCursorEditDialog


class MoveCursorAction(mixins.PyautoguiStopMixin, Action):
    name = 'Move cursor'
    category = 'Mouse'

    def __init__(self, comment='', move_type='Absolute', position_x=-1, position_y=-1, duration=0, button='None'):
        self.comment = str(comment)
        self.move_type = str(move_type)
        self.position_x = int(position_x)
        self.position_y = int(position_y)
        self.duration = float(duration)
        self.button = str(button)

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'move_type': self.move_type,
                'position_x': self.position_x,
                'position_y': self.position_y,
                'duration': self.duration,
                'button': self.button}

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = MoveCursorEditDialog.MoveCursorEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.move_type, self.position_x, self.position_y, self.duration,
                           self.button) != properties
            if was_changed:
                self.comment, self.move_type, self.position_x, self.position_y, self.duration, self.button = properties
            return was_changed

    def run(self):
        if self.button == 'None':
            if self.move_type == 'Absolute':
                pyautogui.moveTo(x=self.position_x, y=self.position_y, duration=self.duration)
            elif self.move_type == 'Relative':
                pyautogui.moveRel(xOffset=self.position_x, yOffset=self.position_y, duration=self.duration)
            else:
                raise ValueError(f'Unknown move type: {self.move_type}')
        else:
            if self.move_type == 'Absolute':
                pyautogui.dragTo(x=self.position_x, y=self.position_y, duration=self.duration, button=self.button)
            elif self.move_type == 'Relative':
                pyautogui.dragRel(xOffset=self.position_x, yOffset=self.position_y, duration=self.duration,
                                  button=self.button)
            else:
                raise ValueError(f'Unknown move type: {self.move_type}')
