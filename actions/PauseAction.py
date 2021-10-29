import time

from gui.EditDialogs import PauseEditDialog
from .Action import Action


class PauseAction(Action):
    name = 'Pause'
    category = 'Other'

    def __init__(self, comment='', duration=1.0):
        self.comment = str(comment)
        self.duration = float(duration)

        self.__stop_flag = False

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'duration': self.duration}

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = PauseEditDialog.PauseEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.duration) != properties
            if was_changed:
                self.comment, self.duration = properties
            return was_changed

    def run(self):
        for _ in range(int(self.duration // 0.25)):
            if self.__stop_flag:
                return
            time.sleep(0.25)

        if self.__stop_flag:
            return
        time.sleep(self.duration % 0.25)

    def stop(self):
        self.__stop_flag = True

    def reset_stop(self):
        self.__stop_flag = False
