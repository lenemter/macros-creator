import xml.etree.ElementTree as ElementTree
from abc import ABC, abstractmethod

import pyautogui

pyautogui.FAILSAFE = False


class Action(ABC):
    name = None
    category = None

    @property
    def xml_name(self) -> str:
        # e.g Write text -> write_text
        return self.name.lower().replace(' ', '_')

    @property
    def parameters(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def open_edit_dialog(self, parent):
        pass

    def xml(self) -> ElementTree.Element:
        xml_name = self.xml_name
        parameters = {str(key): str(value) for (key, value) in self.parameters.items()}
        return ElementTree.Element(xml_name, parameters)

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def reset_stop(self):
        pass
