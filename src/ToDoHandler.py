import json
import re
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse


# Обработчик HTTP запросов для задач
class ToDoHandler(BaseHTTPRequestHandler):
    def __init__(self, manager, *args, **kwargs):
        self.todo_manager = manager
        super().__init__(*args, **kwargs)

    def _set_response(self, status_code, data=None, content_type=None):
        """Установка параметров ответа"""
        self.send_response(status_code)
        if content_type:
            self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        if data:
            self.wfile.write(data)

    def _return_json(self, data, code=200):
        """Возврат ответа типа json"""
        self._set_response(
            code, json.dumps(data).encode("utf-8"), content_type="application/json"
        )

    def _return_errors(self, data, code=400):
        """Возврат ответа c ошибками"""
        if isinstance(data, list):
            self._return_json({"errors": data}, code)
        else:
            self._return_json({"errors": [data]}, code)

    def _parse_request_data(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)
        try:
            return json.loads(post_data.decode("utf-8"))
        except json.JSONDecodeError:
            return None

    def _get_items(self):
        """Получение списка задач"""
        items = self.todo_manager.get_all_items()
        items_data = [item.export() for item in items]
        self._return_json(items_data)

    def _get_item(self, id):
        """Получение задачи по ид"""
        item = self.todo_manager.get_item_by_id(id)
        if item is None:
            self._return_errors("Not found", 404)
        else:
            self._return_json(item.export())

    def _create_item(self):
        """Создание задачи"""
        item_data = self._parse_request_data()
        if item_data is None:
            self._return_errors("Invalid JSON")
            return

        errors = []
        title = item_data.get("title")
        if not title:
            errors.append("title cannot be empty")

        priority = item_data.get("priority", "normal")
        if priority not in ["low", "normal", "high"]:
            errors.append("priority must be one of [low, normal, high]")

        if errors:
            self._return_errors(errors)
            return

        task = self.todo_manager.create_item(title, priority)
        self._return_json(task.export())

    def _mark_item_complete(self, id):
        """Выполнение задачи"""
        if not self.todo_manager.mark_item_complete(id):
            self._return_errors("Not found", 404)
        else:
            self._set_response(200)

    def do_OPTIONS(self):
        """Обработка preflight запросов для CORS"""
        self._set_response(200)

    def do_GET(self):
        """Обработка GET запросов"""
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/tasks":
            self._get_items()
            return

        match = re.match(r"^/tasks/(\d+)$", parsed_path.path)
        if match:
            id = int(match.group(1))
            self._get_item(id)
        else:
            self._return_errors("Invalid url", 404)

    def do_POST(self):
        """Обработка POST запросов"""
        parsed_path = urlparse(self.path)
        if parsed_path.path == "/tasks":
            self._create_item()
            return

        match = re.match(r"^/tasks/(\d+)/complete$", parsed_path.path)
        if match:
            id = int(match.group(1))
            self._mark_item_complete(id)
        else:
            self._return_errors("Invalid url", 404)
