import logging
import os
import datetime


class APILogger:
    def __init__(self, log_dir='logs', test_name=os.environ.get('PYTEST_CURRENT_TEST')):
        self.log_dir = log_dir
        self.logger = self.create_logger()
        self.test_name = test_name

    def create_logger(self):
        # Создание директории для логов, если она не существует
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # Настройка логгера
        logger = logging.getLogger('api_tests')
        logger.setLevel(logging.INFO)

        # Создание обработчика файла
        file_handler = logging.FileHandler(
            os.path.join(self.log_dir, f'api_tests_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'),
            encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        # Создание форматтера
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Добавление обработчика к логгеру
        logger.addHandler(file_handler)

        # Отключение вывода в консоль
        logger.propagate = False

        return logger

    def log_test_start(self):
        self.logger.info(f'Начало теста: {self.test_name}')
        self.logger.info(f'Запуск теста: {datetime.datetime.now()}')

    def log_request(self, method, url, headers=None, data=None):
        self.logger.info(f'Отправлен {method.upper()} запрос на {url}')
        if headers:
            self.logger.info(f'Заголовки: {headers}')
        if data:
            self.logger.info(f'Данные: {data}')
        self.logger.info('')

    def log_response(self, status_code, response_json):
        self.logger.info(f'Получен ответ со статусом {status_code}')
        self.logger.info(f'Ответ: {response_json}')
        self.logger.info('')

    def log_error(self, error_message, response_json):
        self.logger.error(f'Тест "{self.test_name}" упал с ошибкой: {error_message}')
        self.logger.error(f'Ответ: {response_json}')

    def log_separator(self):
        self.logger.info('\n')
