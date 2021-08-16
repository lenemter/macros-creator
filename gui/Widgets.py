from PyQt5.QtWidgets import QStyledItemDelegate, QFrame


class ReadOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, *args):
        return None


class HorizontalLine(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class VerticalLine(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)
