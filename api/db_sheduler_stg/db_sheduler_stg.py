import pyodbc
import api_testing_project.config as config
from config import TestEnvironment


class DatabaseConnection:
    """Класс для управления подключением к БД"""

    def __init__(self):
        self.server = TestEnvironment.SERVER
        self.data_base = TestEnvironment.DATA_BASE
        self.user_name = TestEnvironment.USER_NAME
        self.password = TestEnvironment.PASSWORD_DB
        self.connection = None

    def connect(self):
        """Установка соединения с БД"""
        driver = "ODBC Driver 17 for SQL Server"

        try:
            connection_string = f'DRIVER={driver};' \
                                f'SERVER={self.server};' \
                                f'DATABASE={self.data_base};' \
                                f'UID={self.user_name};' \
                                f'PWD={self.password};'
            self.connection = pyodbc.connect(connection_string, Trusted_Connection='No')
            print(f'Соединение с базой данных {self.data_base} установлено')
        except Exception as e:
            print(f'Ошибка соединения при подключении к БД {self.data_base}. \n{e}')

    def close(self):
        """Закрытие соединения с БД"""
        if self.connection:
            self.connection.close()
            print(f'Соединение с БД {self.data_base} закрыто')

    def execute_query(self, query: str):
        """Выполнение запроса"""
        if not self.connection:
            print('Нет активного соединения')
            return

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            res = []
            columns = [column[0] for column in cursor.description]  # Получение всех колонок из ответа

            # Сохраняем результаты в виде словаря
            rows = cursor.fetchall()
            for row in rows:
                res.append(dict(zip(columns, row)))

            return res
        except Exception as e:
            print(f'Ошибка выполнения запроса к БД {self.data_base}. \n{e}')
            return None
