import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_window_auth import AuthView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Программный модуль УП 02.01')
        self.setWindowIcon(QIcon("images/logo.png"))
        self.auth_view = AuthView(self)
        self.auth_view.show()

    def clear_central_widget(self):
        self.setCentralWidget(None)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())