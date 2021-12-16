from gui.EditDialogs import GotoEditDialog
from .Action import Action


class GotoAction(Action):
    name = 'Goto'
    category = 'Other'

    def __init__(self, comment='', loop_start=0):
        self.comment = str(comment)
        self.loop_start = int(loop_start)

        self.__stop_flag = False

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'loop_start': self.loop_start}

    def open_edit_dialog(self, parent):
        edit_dialog = GotoEditDialog.GotoEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            self.comment, self.loop_start = edit_dialog.properties

    def run(self) -> None | int:
        if self.__stop_flag:
            return None
        return self.loop_start

    def stop(self):
        self.__stop_flag = True

    def reset_stop(self):
        self.__stop_flag = False
