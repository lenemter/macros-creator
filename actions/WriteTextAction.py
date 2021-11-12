import pyautogui

from gui.EditDialogs import WriteTextEditDialog
from .Action import Action


class WriteTextAction(Action):
    name = 'Write text'
    category = 'Keyboard'

    def __init__(self, comment='', text='', amount=1, interval=0.0):
        self.comment = str(comment)
        self.text = str(text)
        self.amount = int(amount)
        self.interval = float(interval)

        self.__stop_flag = False
        self.__pause_action = None

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'text': self.text,
                'amount': self.amount,
                'interval': self.interval}

    def open_edit_dialog(self, parent):
        edit_dialog = WriteTextEditDialog.WriteTextEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            self.comment, self.text, self.amount, self.interval = edit_dialog.properties

    def run(self):
        # Import is here because at the top of the file it triggers PauseAction import
        # and 'Other' category is becoming the first one
        from .PauseAction import PauseAction

        self.__pause_action = PauseAction(duration=self.interval)
        full_text = self.text * self.amount
        # can't stop using FailSafeException
        for char in full_text:
            if self.__stop_flag:
                break
            self.__pause_action.run()
            pyautogui.typewrite(char)

    def stop(self):
        self.__stop_flag = True
        self.__pause_action.stop()

    def reset_stop(self):
        self.__stop_flag = False
        self.__pause_action.reset_stop()
