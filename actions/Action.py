from abc import ABC, abstractmethod
import pyautogui

pyautogui.FAILSAFE = False


class Action(ABC):
    name = None
    category = None

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    def open_edit_dialog(self, parent) -> bool:
        raise NotImplementedError

    def get_xml_name(self):
        return self.name.lower().replace(' ', '_')

    @abstractmethod
    def xml(self):
        raise NotImplementedError

    @abstractmethod
    def run(self):
        raise NotImplementedError


class NoneAction:
    name = ''
    comment = ''
