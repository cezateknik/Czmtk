from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDateEdit, QLineEdit


class NumericInput(QLineEdit):
    def __init__(self, maximum=1000000, parent=None):
        super().__init__(parent)
        self.setValidator(QIntValidator(0, maximum, self))
        self.setAlignment(Qt.AlignRight)
        self.setFixedHeight(30)
        self.setMinimumWidth(68)
        self.setMaximumWidth(96)
        self.setStyleSheet(
            "QLineEdit { background: white; border: 1px solid #c9d4e3; "
            "border-radius: 6px; padding: 4px 8px; selection-background-color: #dce6fb; }"
            "QLineEdit:focus { border: 1px solid #6f89bf; background: #fbfdff; }"
        )

    def wheelEvent(self, event):
        event.ignore()

    def value(self):
        text = self.text().strip()
        return int(text) if text else 0


class NoWheelDateEdit(QDateEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(30)
        self.setMinimumWidth(132)
        self.setMaximumWidth(150)

    def wheelEvent(self, event):
        event.ignore()
