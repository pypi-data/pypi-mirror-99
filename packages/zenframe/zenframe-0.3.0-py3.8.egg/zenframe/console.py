from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
from zenframe.util import print_to_stderr


class ConsoleWidget(QTextEdit):
    append_signal = pyqtSignal(str)

    def __init__(self, rebind=True):
        if rebind:
            self.stdout = sys.stdout
            sys.stdout = self

        QTextEdit.__init__(self)
        pallete = self.palette()
        pallete.setColor(QPalette.Base, QColor(30, 30, 30))
        pallete.setColor(QPalette.Text, QColor(255, 255, 255))
        self.setPalette(pallete)

        self.cursor = self.textCursor()
        self.setReadOnly(True)

        font = QFont()
        font.setFamily("Monospace")
        font.setPointSize(10)
        font.setStyleHint(QFont.Monospace)
        self.setFont(font)

        metrics = QFontMetrics(font)
        self.setTabStopWidth(metrics.width("    "))

        self.append_signal.connect(self.append, Qt.QueuedConnection)

    def write_native(self, data):
        self.stdout.write(data)
        self.stdout.flush()

    def flush(self):
        self.stdout.flush()

    def clear(self):
        self.setText("")

    def write(self, data):
        self.append_signal.emit(data)
        self.write_native(data)

    def append(self, data):
        if data.startswith("\r"):  # TODO: Update last string
            pass

        self.cursor.insertText(data)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
