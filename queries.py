from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QPushButton, QTableWidgetItem, QLabel, QComboBox, QLineEdit, QListWidget, QScrollArea
from PyQt5.QtCore import Qt
from connection import Connection

current_table_name = None
column_names = None

class QueryManager:
    def __init__(self, username, password, table_widget, query_block_layout, name_query, query_block_label, status_bar, message):
        self.username = username
        self.password = password

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

        self.column_combo = None
        self.value_input = None
        self.operator_combo = None
        self.line_edits = None
        self.check_column = None
        self.list_widget = None
        self.rows = None
        self.query_block_layout = query_block_layout
        self.name_query = name_query
        self.query_block_label = query_block_label
        self.table = table_widget
        self.status_bar = status_bar
        self.message = message

        self.apply_button = QPushButton("Применить")
        self.apply_button.setStyleSheet(self.button_style)

        self.cancel_button = QPushButton("Отмена")
        self.cancel_button.setStyleSheet(self.button_style)
        self.cancel_button.clicked.connect(self.reset_query_block)

    def get_tables_from_db(self):
        connection = Connection.connect_to_db(self.username, self.password)
        cursor = connection.cursor()
        try:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            return tables
        except Exception as e:
            print(f"Ошибка при получении списка таблиц: {e}")
            return []
        finally:
            cursor.close()
            connection.close()

    def select_table(self, table):
        global current_table_name
        current_table_name = table
        connection = Connection.connect_to_db(self.username, self.password)
        cursor = connection.cursor()
        try:
            cursor.execute(f"""SELECT * FROM {table};""")
            self.rows = cursor.fetchall()

            global column_names
            column_names = [desc[0] for desc in cursor.description]

            self.table.setRowCount(len(self.rows))
            self.table.setColumnCount(len(column_names))
            self.table.verticalHeader().setVisible(False)
            self.table.setHorizontalHeaderLabels(column_names)

            for i, row in enumerate(self.rows):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
        finally:
            connection.commit()
            cursor.close()
            connection.close()

    def add_record(self):
        print(f"Выбрана таблица: {current_table_name}")

        if self.table.rowCount() <= 0:
            self.show_message("Ошибка", "Не удалось загрузить данные из таблицы.")
            return

        self.reset_query_block()

        self.name_query = "Запрос на добавление"
        self.query_block_label = QLabel(self.name_query)
        self.query_block_label.setStyleSheet("""
                            font-size: 32px;
                            font-weight: bold;
                        """)
        self.query_block_layout.setAlignment(Qt.AlignTop)
        self.query_block_layout.setSpacing(10)
        self.query_block_layout.setContentsMargins(10, 10, 10, 10)
        self.query_block_layout.addWidget(self.query_block_label)

        self.status_bar.showMessage(self.message)

        params_layout = QVBoxLayout()
        params_layout.setSpacing(10)
        params_layout.setContentsMargins(0, 0, 0, 0)

        self.line_edits = []

        for column_name in column_names:
            name_of_param = QLabel(column_name)
            name_of_param.setStyleSheet("""
                QLabel {
                    background-color: #404041;
                    color: #E6C17A;
                    font: 20px "Inter";
                    padding: 5px;
                    border-radius: 12px;
                }""")
            params_layout.addWidget(name_of_param)

            line = QLineEdit()
            line.setStyleSheet("""
                QLineEdit {
                    background-color: #404041;
                    color: #E6C17A;
                    font: 20px "Inter";
                    padding: 5px;
                    border-radius: 12px;
                }""")
            params_layout.addWidget(line)

            self.line_edits.append(line)

        params_widget = QWidget()
        params_widget.setLayout(params_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(params_widget)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical {
                background-color: #404041;
                width: 5px;
                margin: 0px;
                border: none;
            }
            QScrollBar::handle:vertical {
                min-height: 10px;
            }
        """)
        self.query_block_layout.addWidget(scroll_area)

        self.apply_button.clicked.connect(self.apply_add_query)
        self.query_block_layout.addWidget(self.apply_button)
        self.query_block_layout.addWidget(self.cancel_button)

    def apply_add_query(self):
        connection = Connection.connect_to_db(self.username, self.password)
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_name = '{current_table_name}'
            """)
            column_info = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка при получении информации о столбцах: {e}")
            return
        finally:
            cursor.close()
            connection.close()

        column_types = {column_name: data_type for column_name, data_type in column_info}

        values = []
        for column_name, line_edit in zip(column_names, self.line_edits):
            value = line_edit.text().strip()

            if not value:
                self.show_message("Ошибка", f"Поле '{column_name}' не может быть пустым")
                return

            data_type = column_types.get(column_name)
            if data_type in ["integer", "float", "numeric"]:
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    self.show_message("Ошибка", f"Неверный формат числа для поля '{column_name}'")
                    return
                values.append(str(value))
            else:
                values.append(f"""'{value}'""")

        text_of_lines = ", ".join(values)

        connection = Connection.connect_to_db(self.username, self.password)
        cursor = connection.cursor()
        try:
            cursor.execute(f"""INSERT INTO {current_table_name} ({", ".join(column_names)}) VALUES ({text_of_lines})""")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
        finally:
            connection.commit()
            cursor.close()
            connection.close()

        self.select_table(self.table)
        self.show_message("Успех", f"Новая строка добавлена.")
        self.reset_query_block(self.query_block_layout)

    def delete_record(self):
        if self.table.rowCount() <= 0:
            self.show_message("Ошибка", "Вы не выбрали таблицу, либо на пуста.")
            return

        self.reset_query_block()

        self.name_query = "Запрос на удаление"
        self.query_block_label = QLabel(self.name_query)
        self.query_block_layout.setAlignment(Qt.AlignTop)
        self.query_block_label.setStyleSheet("""
                            font-size: 32px;
                            font-weight: bold;
                        """)
        self.query_block_layout.setSpacing(10)
        self.query_block_layout.setContentsMargins(10, 10, 10, 10)
        self.query_block_layout.addWidget(self.query_block_label)

        self.message = self.name_query
        self.status_bar.showMessage(self.message)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
               QListWidget {
                   background-color: #404041;
                   color: #E6C17A;
                   font: 20px "Inter";
                   border-radius: 12px;
               }
               QListWidget::item:selected {
                   background-color: #E6C17A;
                   color: #404041;
               }
           """)

        for i in range(self.table.rowCount()):
            self.list_widget.addItem(str(i + 1))

        self.query_block_layout.addWidget(self.list_widget)

        self.apply_button.clicked.connect(lambda: self.apply_delete_query(self.list_widget.currentRow()))
        self.query_block_layout.addWidget(self.apply_button)
        self.query_block_layout.addWidget(self.cancel_button)

    def apply_delete_query(self, row_index):
        if row_index < 0:
            self.show_message("Ошибка", "Выберите строку для удаления")
            return

        connection = Connection.connect_to_db(self.username, self.password)
        cursor = connection.cursor()
        try:
            cursor.execute(f"""DELETE FROM {current_table_name} WHERE {column_names[0]} = {self.rows[row_index][0]}""")
        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при удалении записи: {e}")
            print(f"Ошибка при загрузке данных: {e}")
        finally:
            connection.commit()
            cursor.close()
            connection.close()

        self.select_table(current_table_name)
        self.show_message("Успех", f"Строка {row_index + 1} успешно удалена")
        self.reset_query_block()

    def filter_records(self):
        if self.table.rowCount() <= 0:
            self.show_message("Ошибка", "Выберите таблицу прежде чем работать с запросом.")
            return

        self.reset_query_block()

        self.name_query = "Запрос на фильтрацию"
        self.query_block_label = QLabel(self.name_query)
        self.query_block_label.setStyleSheet("""
                    font-size: 32px;
                    font-weight: bold;
                """)
        self.query_block_layout.setAlignment(Qt.AlignTop)
        self.query_block_layout.setSpacing(10)
        self.query_block_layout.setContentsMargins(10, 10, 10, 10)
        self.query_block_layout.addWidget(self.query_block_label)

        self.message = self.name_query
        self.status_bar.showMessage(self.message)

        column_label = QLabel("Столбец:")
        column_label.setStyleSheet("""
            QLabel {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 5px;
                border-radius: 12px;
            }""")
        self.query_block_layout.addWidget(column_label)

        self.column_combo = QComboBox()
        self.column_combo.addItems(column_names)
        self.column_combo.setStyleSheet("""
            QComboBox {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 5px;
                border-radius: 12px;
            }""")
        self.query_block_layout.addWidget(self.column_combo)

        operator_label = QLabel("Оператор:")
        operator_label.setStyleSheet("""
            QLabel {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 5px;
                border-radius: 12px;
            }""")
        self.query_block_layout.addWidget(operator_label)

        self.operator_combo = QComboBox()
        self.operator_combo.addItems(["=", "!=", "<", ">", "<=", ">="])
        self.operator_combo.setStyleSheet("""
            QComboBox {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 5px;
                border-radius: 12px;
            }""")
        self.query_block_layout.addWidget(self.operator_combo)

        value_label = QLabel("Значение:")
        value_label.setStyleSheet("""
            QLabel {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 5px;
                border-radius: 12px;
            }""")
        self.query_block_layout.addWidget(value_label)

        self.value_input = QLineEdit()
        self.value_input.setStyleSheet("""
            QLineEdit {
                background-color: #404041;
                color: #E6C17A;
                font: 20px "Inter";
                padding: 5px;
                border-radius: 12px;
            }""")
        self.query_block_layout.addWidget(self.value_input)

        self.apply_button.clicked.connect(self.apply_filter_query)
        self.query_block_layout.addWidget(self.apply_button)
        self.query_block_layout.addWidget(self.cancel_button)

    def apply_filter_query(self):
        selected_column = self.column_combo.currentText()
        selected_operator = self.operator_combo.currentText()
        input_value = self.value_input.text().strip()

        if not selected_column or not selected_operator or not input_value:
            self.show_message("Ошибка", "Заполните все поля для фильтрации")
            return

        connection = Connection.connect_to_db(self.username, self.password)
        cursor = connection.cursor()
        try:
            cursor.execute(f"""
                SELECT data_type
                FROM information_schema.columns
                WHERE table_name = '{current_table_name}' AND column_name = '{selected_column}'
            """)
            column_type = cursor.fetchone()[0]

            if column_type in ["integer", "float", "numeric"]:
                try:
                    input_value = float(input_value) if '.' in input_value else int(input_value)
                except ValueError:
                    self.show_message("Ошибка", "Неверный формат числа")
                    return
                value_for_query = str(input_value)
            else:
                value_for_query = f"'{input_value}'"

            # Формируем запрос
            cursor.execute(f"""
                SELECT * FROM {current_table_name}
                WHERE {selected_column} {selected_operator} {value_for_query}
            """)
            self.rows = cursor.fetchall()

            self.table.setRowCount(len(self.rows))
            for i, row in enumerate(self.rows):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))

        except Exception as e:
            self.show_message("Ошибка", f"Ошибка при выполнении фильтрации: {e}")
            print(f"Ошибка при выполнении фильтрации: {e}")
        finally:
            connection.commit()
            cursor.close()
            connection.close()

        self.show_message("Успех", "Фильтрация выполнена успешно")
        self.reset_query_block()

    def sort_records(self):
        if self.table.rowCount() <= 0:
            self.show_message("Ошибка", "Выберите таблицу прежде чем работать с запросом.")
            return

        self.reset_query_block()

        self.name_query = "Запрос на сортировку"
        self.query_block_label = QLabel(self.name_query)
        self.query_block_label.setStyleSheet("""
                    font-size: 32px;
                    font-weight: bold;
                """)
        self.query_block_layout.setAlignment(Qt.AlignTop)
        self.query_block_layout.setSpacing(10)
        self.query_block_layout.setContentsMargins(10, 10, 10, 10)
        self.query_block_layout.addWidget(self.query_block_label)

        self.message = self.name_query
        self.status_bar.showMessage(self.message)

        self.check_column = QListWidget()
        self.check_column.setStyleSheet("""
                       QListWidget {
                           background-color: #404041;
                           color: #E6C17A;
                           font: 20px "Inter";
                           border-radius: 12px;
                       }
                       QListWidget::item:selected {
                           background-color: #E6C17A;
                           color: #404041;
                       }
                   """)

        for name in column_names:
            self.check_column.addItem(name)

        self.query_block_layout.addWidget(self.check_column)

        self.list_widget = QListWidget()
        self.list_widget.setStyleSheet("""
                       QListWidget {
                           background-color: #404041;
                           color: #E6C17A;
                           font: 20px "Inter";
                           border-radius: 12
                       }
                       QListWidget::item:selected {
                           background-color: #E6C17A;
                           color: #404041;
                       }
                   """)

        adesc = {
            "ASC": "ASC",
            "DESC": "DESC",
        }

        self.list_widget.addItem(adesc["ASC"])
        self.list_widget.addItem(adesc["DESC"])

        self.query_block_layout.addWidget(self.list_widget)

        self.apply_button.clicked.connect(self.apply_sort_query)
        self.query_block_layout.addWidget(self.apply_button)
        self.query_block_layout.addWidget(self.cancel_button)

    def apply_sort_query(self):
        try:
            selected_column_item = self.check_column.currentItem().text()
            if not selected_column_item:
                self.show_message("Ошибка", "Выберите столбец для сортировки")
                return

            selected_direction_item = self.list_widget.currentItem().text()
            if not selected_direction_item:
                self.show_message("Ошибка", "Выберите направление сортировки")
                return

            connection = Connection.connect_to_db(self.username, self.password)
            cursor = connection.cursor()
            try:
                cursor.execute(
                    f"""SELECT * FROM {current_table_name} ORDER BY {selected_column_item} {selected_direction_item}""")
                self.rows = cursor.fetchall()

                self.table.setRowCount(len(self.rows))
                for i, row in enumerate(self.rows):
                    for j, value in enumerate(row):
                        self.table.setItem(i, j, QTableWidgetItem(str(value)))
            except Exception as e:
                self.show_message("Ошибка", f"Ошибка при выполнении сортировки: {e}")
                print(f"Ошибка при выполнении сортировки: {e}")
            finally:
                connection.commit()
                cursor.close()
                connection.close()

            self.show_message("Успех", f"Сортировка успешна.")
        except Exception as e:
            self.show_message("Ошибка", f"Непредвиденная ошибка: {e}")
        finally:
            self.reset_query_block()

    def reset_query_block(self):
        self.query_block_layout.addWidget(self.apply_button)
        self.query_block_layout.addWidget(self.cancel_button)

        while self.query_block_layout.count():
            item = self.query_block_layout.takeAt(0)
            if item.widget() and item.widget() != self.apply_button and item.widget() != self.cancel_button and item.widget() != current_table_name:
                item.widget().deleteLater()
            if item.layout():
                while item.layout().count():
                    child_item = item.layout().takeAt(0)
                    if child_item.widget():
                        child_item.widget().deleteLater()
                    elif child_item.layout():
                        child_item.layout().deleteLater()
                item.layout().deleteLater()

    def show_message(self, title, message):
        error_box = QMessageBox()
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStyleSheet("""font: 24px "Inter"; background-color: #404041; color: #E6C17A;""")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()