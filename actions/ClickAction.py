import pyautogui

from gui.EditDialogs import ClickEditDialog
from . import mixins
from .Action import Action


class ClickAction(mixins.PyautoguiStopMixin, Action):
    name = 'Click'
    category = 'Mouse'

    def __init__(self, comment='', action='Click', button='Left', amount=1, interval=0.0,
                 move_type='Absolute', position_x=0, position_y=0, restore_cursor=False):
        self.comment = str(comment)
        self.action = str(action)
        self.button = str(button)
        self.amount = int(amount)
        self.interval = float(interval)
        self.move_type = str(move_type)
        self.position_x = int(position_x)
        self.position_y = int(position_y)
        self.restore_cursor = int(restore_cursor)  # 0 - False, 1 - True

        self.__stop_flag = False

    @property
    def parameters(self) -> dict:
        return {'comment': self.comment,
                'action': self.action,
                'button': self.button,
                'amount': self.amount,
                'interval': self.interval,
                'move_type': self.move_type,
                'position_x': self.position_x,
                'position_y': self.position_y,
                'restore_cursor': self.restore_cursor}

    def open_edit_dialog(self, parent) -> bool:
        edit_dialog = ClickEditDialog.ClickEditDialog(parent, self)
        edit_dialog.exec()

        if edit_dialog.user_clicked_ok:
            properties = edit_dialog.properties()
            was_changed = (self.comment, self.action, self.button, self.amount, self.interval, self.move_type,
                           self.position_x, self.position_y, self.restore_cursor) != properties
            if was_changed:
                (self.comment, self.action, self.button, self.amount, self.interval, self.move_type, self.position_x,
                 self.position_y, self.restore_cursor) = properties
            return was_changed

    def run(self):
        if self.move_type == 'Absolute':
            self.__click_move_absolute()
        elif self.move_type == 'Relative':
            self.__click_move_relative()
        else:
            raise ValueError(f'Unknown move typle: {self.move_type}')

    def __click_move_absolute(self):
        mouse_position = pyautogui.position()

        if self.action == 'Click':
            pyautogui.click(x=self.position_x, y=self.position_y, clicks=self.amount, interval=self.interval,
                            button=self.button)
        elif self.action == 'Press':
            pyautogui.mouseDown(x=self.position_x, y=self.position_y, button=self.button)
        elif self.action == 'Release':
            pyautogui.mouseUp(x=self.position_x, y=self.position_y, button=self.button)
        else:
            raise ValueError(f'Unknown action: {self.action}')

        if self.restore_cursor:
            pyautogui.moveTo(x=mouse_position.x, y=mouse_position.y)

    def __click_move_relative(self):
        # Import is here because at the top of the file it triggers PauseAction import
        # and 'Other' category is becoming the first one
        from .PauseAction import PauseAction

        pause_action = PauseAction(duration=self.interval)
        for _ in range(self.amount):
            if self.__stop_flag:
                return None

            mouse_position = pyautogui.position()
            x = mouse_position[0] + self.position_x
            y = mouse_position[1] + self.position_y
            if self.action == 'Click':
                pyautogui.click(x=x, y=y, button=self.button)
            elif self.action == 'Press':
                pyautogui.mouseDown(x=x, y=y, button=self.button)
            elif self.action == 'Release':
                pyautogui.mouseUp(x=x, y=y, button=self.button)
            else:
                raise ValueError(f'Unknown action: {self.action}')

            if self.restore_cursor:
                pyautogui.moveTo(*mouse_position)

            pause_action.run()
