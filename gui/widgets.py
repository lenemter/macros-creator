from PyQt5.QtWidgets import QFrame, QLabel


class HorizontalLine(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


class DescriptionLabel(QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWordWrap(True)
        font = self.font()
        font.setPointSize(font.pointSize() - 1)
        self.setFont(font)
