from PyQt5.QtWidgets import QLabel

class GridLabel(QLabel):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.setStyleSheet("border: 2px solid black; border-radius: 10px; background-color: white;")
        self.parent = parent
        self.toggled = False

    def enterEvent(self, event):
        if self.parent.dragging:
            self.parent.toggle_label(self)

    def leaveEvent(self, event):
        pass
