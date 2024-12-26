from PyQt5.QtWidgets import QMessageBox, QApplication, QWidgetAction, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QLabel, QStatusBar, QToolBar, QToolButton, QScrollArea, QComboBox, QListWidget, QAbstractItemView, QHeaderView, QAction, QMenu, QGridLayout, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QIcon, QPixmap

from queries import QueryManager

class TableView(QWidget):
    def __init__(self, parent, username, password):
        super().__init__(parent)
        self.parent = parent
        self.password = password
        self.username = username

        self.name_query = "Название запроса"
        self.message = "Строка состояния"
        self.query_block_label = QLabel(self.name_query)

        self.queries_button = None
        self.help_button = None
        self.account_button = None

        self.query_block_layout = QVBoxLayout()

        self.button_style = """
                            QPushButton, QToolButton {
                                background-color: #404041;
                                color: #E6C17A;
                                font: 20px "Inter";
                                padding: 10px;
                                margin: 5px;
                                border-radius: 12px;
                            }
                            QPushButton:hover, QToolButton:hover {
                                background: #E6C17A;
                                color: #404041;
                            }
                        """

        self.table = QTableWidget(self)

        self.status_bar = QStatusBar(self)

        self.query_manager = QueryManager(self.username, self.password, self.table, self.query_block_layout, self.name_query, self.query_block_label, self.status_bar, self.message)

        self.init_ui()

    def init_ui(self):
        self.parent.setStyleSheet("""background-color: #404041; font: "Inter"; color: #E6C17A;""")

        query_manager = QueryManager(self.username, self.password, self.table, self.query_block_layout, self.name_query, self.query_block_label, self.status_bar, self.message)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout_th = QHBoxLayout()

        self.queries_button = QToolButton()
        self.queries_button.setText("Запросы")
        self.queries_button.clicked.connect(self.open_queries_menu)

        self.help_button = QToolButton()
        self.help_button.setText("Справка")
        self.help_button.clicked.connect(self.open_help_menu)

        self.account_button = QToolButton()
        self.account_button.setText("Аккаунт")
        self.account_button.clicked.connect(self.open_account_menu)

        title_label = QLabel("Программный модуль УП 02.01")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 48px;
            font-weight: bold;
            background-color: #F6EDE3;
            border-bottom-right-radius: 12px 12px;
            border-bottom-left-radius: 12px 12px;
        """)
        title_label.setContentsMargins(100, 0, 100, 0)

        toolbar_1 = QToolBar()
        toolbar_1.setStyleSheet("""QToolBar {
                        background-color: #F6EDE3;
                        border-bottom-right-radius: 12px 12px;
                    }""" + self.button_style)
        toolbar_1.setMovable(False)
        self.parent.addToolBar(toolbar_1)

        toolbar_2 = QToolBar()
        toolbar_2.setStyleSheet("""QToolBar {
                        background-color: #F6EDE3;
                        border-bottom-right-radius: 12px 12px;
                        border-bottom-left-radius: 12px 12px;
                    }""" + self.button_style)
        toolbar_2.setMovable(False)
        self.parent.addToolBar(toolbar_2)

        toolbar_3 = QToolBar()
        toolbar_3.setStyleSheet("""QToolBar {
                        background-color: #F6EDE3;
                        border-bottom-left-radius: 12px 12px;
                    }""" + self.button_style)
        toolbar_3.setMovable(False)
        self.parent.addToolBar(toolbar_3)

        toolbar_1.addWidget(self.queries_button)
        toolbar_1.addWidget(self.help_button)
        toolbar_2.addWidget(title_label)
        toolbar_3.addWidget(self.account_button)

        layout_th.addWidget(toolbar_1)
        layout_th.addStretch()
        layout_th.addWidget(toolbar_2)
        layout_th.addStretch()
        layout_th.addWidget(toolbar_3)

        layout.addLayout(layout_th)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionsClickable(False)
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
             QTableWidget {
                 border-radius: 12px;
                 gridline-color: #404041;
                 background-color: #F6EDE3;
                 color: #404041;
                 font: 16px "Inter";
             }
             QHeaderView::section {
                 background-color: #F6EDE3;
                 color: #404041;
                 font: 20px "Inter";
             }
         """)

        table_layout = QHBoxLayout()
        table_layout.setContentsMargins(15, 15, 0, 15)
        table_layout.addWidget(self.table)

        main_layout = QHBoxLayout()
        main_layout.addLayout(table_layout)

        layout_v = QVBoxLayout()

        list_of_tables_layout = QVBoxLayout()
        list_of_tables_label = QLabel("Список таблиц")
        list_of_tables_label.setAlignment(Qt.AlignCenter)
        list_of_tables_label.setStyleSheet("""
            font: 40px "Inter";
            color: #E6C17A; 
            font-weight: bold;
        """)
        list_of_tables_layout.addWidget(list_of_tables_label)

        tables = query_manager.get_tables_from_db()
        for table in tables:
            table_button = QPushButton(table)
            table_button.setStyleSheet("""
                    QPushButton {
                        background-color: #F6EDE3;
                        color: #404041;
                        font: 24px "Inter";
                        border-radius: 12px;
                        padding: 10px;
                        margin: 5px;
                        width: 400px;
                    }
                    QPushButton:hover {
                        background-color: #404041;
                        color: #F6EDE3;
                    }
                """)
            table_button.clicked.connect(lambda _, t=table: query_manager.select_table(t))
            list_of_tables_layout.addWidget(table_button)

        list_of_tables_widget = QWidget()
        list_of_tables_widget.setStyleSheet("""
            background-color: #F6EDE3;
            color: #E6C17A;
            padding: 10px;
            border-radius: 12px;
        """)
        list_of_tables_widget.setLayout(list_of_tables_layout)

        layout_v.addWidget(list_of_tables_widget)

        self.query_block_label = QLabel("Название запроса")
        self.query_block_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.query_block_label.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)
        self.query_block_layout.addWidget(self.query_block_label)

        no_query_label = QLabel("Запрос не выбран")
        no_query_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        no_query_label.setStyleSheet("font-size: 24px; color: #E6C17A;")
        self.query_block_layout.addWidget(no_query_label)

        query_block_widget = QWidget()
        query_block_widget.setStyleSheet("""
            background-color: #F6EDE3;
            padding: 10px;
            border-radius: 12px;
        """)
        query_block_widget.setLayout(self.query_block_layout)

        query_block_widget.setFixedWidth(450)
        query_block_widget.setFixedHeight(450)

        layout_v.addWidget(query_block_widget)
        layout_v.setContentsMargins(15, 15, 25, 15)

        main_layout.addLayout(layout_v)
        layout.addLayout(main_layout)

        self.status_bar.setStyleSheet("""
            background-color: #F6EDE3;
            color: #E6C17A;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            border-bottom-right-radius: 12px;
            font: 24px "Inter";
        """)
        self.status_bar.setFixedWidth(650)
        self.status_bar.showMessage(self.message)

        layout.addWidget(self.status_bar)

        self.setLayout(layout)

    def open_queries_menu(self):
        self.show_menu(["Добавить запись", "Удалить запись", "Фильтрация", "Сортировка"], self.queries_button)

    def open_help_menu(self):
        self.show_menu(["О программе", "FAQ"], self.help_button)

    def open_account_menu(self):
        self.show_account_menu()

    def show_menu(self, buttons, button):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #F6EDE3;
                color: #E6C17A;
                border-bottom-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
                padding: 10px;
            }
            QMenu::item {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 10px;
                margin: 5px;
                border-radius: 12px;
            }
            QMenu::item:selected {
                background: #E6C17A;
                color: #404041;
            }
        """)
        menu.setFixedWidth(300)
        menu.setContentsMargins(5, 10, 5, 10)

        button_actions = {
            "Добавить запись": self.query_manager.add_record,
            "Удалить запись": self.query_manager.delete_record,
            "Фильтрация": self.query_manager.filter_records,
            "Сортировка": self.query_manager.sort_records,
            "О программе": self.about_prog,
            "FAQ": self.show_faq,
        }

        for button_text in buttons:
            action = QAction(button_text, menu)
            if button_text in button_actions:
                action.triggered.connect(button_actions[button_text])
            menu.addAction(action)

        button_pos = button.mapToGlobal(QPoint(0, button.height()))
        menu.popup(button_pos)

    def show_account_menu(self):
        grid_widget = QWidget()
        grid_layout = QGridLayout()
        grid_widget.setStyleSheet("background-color: #F6EDE3;")

        grid_widget.setLayout(grid_layout)

        image_label = QLabel()
        image_label.setStyleSheet("border-radius: 50%;")
        image_label.setFixedSize(160, 100)
        pixmap = QPixmap("images/malee.png").scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setContentsMargins(60, 0, 0, 10)
        grid_layout.addWidget(image_label, 0, 0)

        user_info_label = QLabel(f"Пользователь\nРоль: {self.username}")
        user_info_label.setStyleSheet("font: 28px 'Inter'; color: #404041;")
        user_info_label.setAlignment(Qt.AlignLeft)
        grid_layout.addWidget(user_info_label, 0, 1)

        change_account_button = QPushButton("Сменить аккаунт")
        change_account_button.setStyleSheet(self.button_style)
        change_account_button.clicked.connect(self.change_account)
        grid_layout.addWidget(change_account_button, 1, 0)

        exit_button = QPushButton("Выйти")
        exit_button.setStyleSheet(self.button_style)
        exit_button.clicked.connect(lambda: QApplication.exit(0))
        grid_layout.addWidget(exit_button, 1, 1)

        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: #F6EDE3;
                color: #E6C17A;
                border-bottom-left-radius: 12px;
                border-top-right-radius: 12px;
                border-bottom-right-radius: 12px;
                padding: 10px;
            }
        """)
        menu.setContentsMargins(5, 10, 5, 10)

        widget_action = QWidgetAction(menu)
        widget_action.setDefaultWidget(grid_widget)
        menu.addAction(widget_action)

        button_pos = self.account_button.mapToGlobal(QPoint(self.account_button.width() - int(self.account_button.width() * 4), self.account_button.height()))
        menu.popup(button_pos)

    def change_account(self):
        from ui_window_auth import AuthView
        self.parent.clear_central_widget()
        self.parent.auth_view = AuthView(self.parent)
        self.parent.setCentralWidget(self.parent.auth_view)

    def about_prog(self):
        self.message = "О программе"
        self.status_bar.showMessage(self.message)

        about_text = (
            "Программный модуль УП 02.01\n"
            "Версия: 1.0\n"
            "Разработчик: Лисин С.А.\n"
            "Описание: Это приложение предназначено для работы с базой данных.\n"
            "Оно позволяет выполнять операции CRUD, фильтрацию и сортировку данных."
        )
        self.show_message("О программе", about_text)

    def show_faq(self):
        self.message = "FAQ"
        self.status_bar.showMessage(self.message)

        faq_text = (
            "FAQ:\n"
            "1. Как добавить новую запись?\n"
            "   - Выберите таблицу, затем нажмите 'Запросы' -> 'Добавить запись'.\n"
            "2. Как удалить запись?\n"
            "   - Выберите таблицу, затем нажмите 'Запросы' -> 'Удалить запись'.\n"
            "3. Как отфильтровать данные?\n"
            "   - Выберите таблицу, затем нажмите 'Запросы' -> 'Фильтрация'.\n"
            "4. Как отсортировать данные?\n"
            "   - Выберите таблицу, затем нажмите 'Запросы' -> 'Сортировка'."
        )
        self.show_message("FAQ", faq_text)

    def reset_table(self):
        if hasattr(self, "table") and self.table is not None:
            self.table.setParent(None)
            self.table.deleteLater()
            self.table = None

    def show_message(self, title, message):
        error_box = QMessageBox()
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStyleSheet("""font: 24px "Inter"; background-color: #404041; color: #E6C17A;""")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()