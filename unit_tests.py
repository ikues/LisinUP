import unittest
from PyQt5.QtWidgets import QMessageBox
from ui_window_auth import AuthView

class TestAuthView(unittest.TestCase):
    def setUp(self):
        self.auth_view = AuthView()

    def test_AuthenticateUser_ValidCredentials(self):
        result = self.auth_view.authenticate_user("Admin", "neadmin")
        self.assertTrue(result)

    def test_AuthenticateUser_InvalidCredentials(self):
        result = self.auth_view.authenticate_user("wronguser", "wrongpassword")
        self.assertFalse(result)

    def test_AuthenticateUser_EmptyUsernameAndPassword(self):
        result = self.auth_view.authenticate_user("", "")
        self.assertFalse(result)

class TestQueryManager(unittest.TestCase):
    def setUp(self):
        self.query_manager = QueryManager("user123", "password123", None, None, None, None, None, None)

    def test_SelectTable_ValidTableName(self):
        result = self.query_manager.select_table("Агенты")
        self.assertTrue(result)

    def test_SelectTable_InvalidTableName(self):
        result = self.query_manager.select_table("нету такой таблицы")
        self.assertFalse(result)

    def test_AddRecord_ValidData(self):
        data = {"name": "John Doe", "age": 30, "position": "Developer"}
        result = self.query_manager.add_record(data)
        self.assertTrue(result)

    def test_AddRecord_InvalidData(self):
        data = {"name": "", "age": "", "position": ""}
        result = self.query_manager.add_record(data)
        self.assertFalse(result)

    def test_DeleteRecord_ValidRow(self):
        result = self.query_manager.delete_record(0)
        self.assertTrue(result)

    def test_DeleteRecord_InvalidRow(self):
        result = self.query_manager.delete_record(999)
        self.assertFalse(result)

    def test_FilterRecords_ValidCriteria(self):
        criteria = "age > 25"
        result = self.query_manager.filter_records(criteria)
        self.assertTrue(result)

    def test_SortRecords_AscendingOrder(self):
        result = self.query_manager.sort_records("name", "ASC")
        self.assertTrue(result)

    def test_SortRecords_DescendingOrder(self):
        result = self.query_manager.sort_records("name", "DESC")
        self.assertTrue(result)

    def show_message(self, title, message):
        error_box = QMessageBox()
        error_box.setWindowTitle(title)
        error_box.setText(message)
        error_box.setStyleSheet("""font: 24px "Inter"; background-color: #404041; color: #E6C17A;""")
        error_box.setStandardButtons(QMessageBox.Ok)
        error_box.exec_()

if __name__ == "__main__":
    unittest.main()