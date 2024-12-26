from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

from ui_work_with_tables import TableView
from connection import Connection

class CustomLineEdit(QLineEdit):
    def __init__(self, placeholder_text):
        super().__init__()
        self.placeholder_text = placeholder_text
        self.setText(placeholder_text)
        self.is_placeholder = True

        self.textChanged.connect(self.on_text_changed)

    def on_text_changed(self, text):
        if self.is_placeholder and text:
            self.clear()
            self.is_placeholder = False
        elif not text and not self.is_placeholder:
            self.setText(self.placeholder_text)
            self.is_placeholder = True
        elif self.placeholder_text == "Пароль":
            self.setEchoMode(QLineEdit.Password)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        if self.is_placeholder:
            self.clear()
            self.is_placeholder = False

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        if not self.text():
            self.setText(self.placeholder_text)
            self.is_placeholder = True

class AuthView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

        self.showMaximized()

    def init_ui(self):
        central_widget = QWidget(self)
        self.parent.setCentralWidget(central_widget)
        self.parent.setStyleSheet(
            """background: url("icons/background.svg") no-repeat center; font: "Inter"; color: #E6C17A;""")

        layout = QVBoxLayout()

        login_input = CustomLineEdit("Логин")
        login_input.setMaximumWidth(int(self.parent.width() * 0.6))

        password_input = CustomLineEdit("Пароль")
        password_input.setMaximumWidth(int(self.parent.width() * 0.6))

        layout.setContentsMargins(710, 340, 0, 340)

        layout.addWidget(login_input)
        layout.addWidget(password_input)

        login_button = QPushButton()
        login_button.setIcon(QIcon("icons/login.svg"))
        login_button.setMaximumWidth(100)
        login_button.setMaximumHeight(100)
        login_button.setIconSize(QSize(100, 100))
        login_button.clicked.connect(lambda: self.authenticate_user(login_input.text(), password_input.text()))
        login_button.setStyleSheet("background: none; border: none;")

        layout_h = QHBoxLayout()
        layout_h.setContentsMargins(0, 0, 580, 160)

        layout_h.addLayout(layout)
        layout_h.addWidget(login_button)

        central_widget.setStyleSheet("""
            QLineEdit {
                background: #F6EDE3;
                color: white;
                font-size: 30px;
                color: #E6C17A;
                font-weight: regular;
                letter-spacing: 24px;
                border: none;
            }
        """)

        central_widget.setLayout(layout_h)

    def authenticate_user(self, username, password):
        if not username or not password:
            self.show_message("Ошибка", "Логин и пароль не могут быть пустыми.")
            return

        conn = Connection.connect_to_db(username, password)

        if conn:
            conn.close()
            self.show_message("Успех", f"Авторизация успешна.\n\nРоль: {username}")

            self.parent.clear_central_widget()

            self.parent.table_view = TableView(self.parent, username, password)
            self.parent.setCentralWidget(self.parent.table_view)
            self.parent.table_view.show()
        else:
            self.show_message("Ошибка", "Упс, ошибка!\n\nНеверный логин или пароль.")

    def show_message(self, title, message):
        error_box = QMessageBox()
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStyleSheet("""font: 24px "Inter"; background-color: #404041; color: #E6C17A;""")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()