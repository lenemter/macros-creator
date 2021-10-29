import pyautogui

from gui.EditDialogs import PressKeyEditDialog
from . import mixins
from .Action import Action


class PressKeyAction(mixins.PyautoguiStopMixin, Action):
    name = 'Press key'
    category = 'Keyboard'

    def __init__(self, comment='', key='', action='Press and release', amount=1, interval=0.0):
        self.comment = str(comment)
        self.key = str(key)
        self.action = str(action)
        self.amount = int(amount)
        self.interval = float(interval)

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'key': self.key,
                'action': self.action,
                'amount': self.amount,
                'interval': self.interval}

    def open_edit_dialog(self, parent):
        edit_dialog = PressKeyEditDialog.PressKeyEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            self.comment, self.key, self.action, self.amount, self.interval = edit_dialog.properties

    def run(self):
        # Import is here because at the top of the file it triggers PauseAction import
        # and 'Other' category is becoming the first one
        from .PauseAction import PauseAction

        pause_action = PauseAction(duration=self.interval)
        if self.action == 'Press and release':
            pyautogui.press(self.key)
            for _ in range(self.amount - 1):
                pyautogui.press(self.key)
                pause_action.run()
        elif self.action == 'Press':
            pyautogui.keyDown(self.key)
        elif self.action == 'Release':
            pyautogui.keyUp(self.key)
        else:
            raise ValueError(f'Unknown action: {self.action}')
