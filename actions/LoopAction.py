from typing import Optional

from actions.Action import Action
from gui.EditDialogs import LoopEditDialog


class LoopAction(Action):
    name = 'Loop'
    category = 'Other'

    def __init__(self, comment='', loop_start=0, count=5):
        self.comment = str(comment)
        self.loop_start = int(loop_start)
        self.count = int(count)

        self.__count = self.count
        self.__stop_flag = False

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'loop_start': self.loop_start,
                'count': self.count}

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = LoopEditDialog.LoopEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.loop_start, self.count) != properties
            if was_changed:
                self.comment, self.loop_start, self.count = properties
            return was_changed

    def run(self) -> Optional[int]:
        if self.__count == 0 or self.__stop_flag:
            self.__count = self.count
            return None
        self.__count -= 1
        return self.loop_start

    def stop(self):
        self.__stop_flag = True

    def reset_stop(self):
        self.__stop_flag = False
        self.__count = self.count
