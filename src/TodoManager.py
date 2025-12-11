import json
import os

from ToDoItem import ToDoItem


# Менеджер задач
class ToDoManager:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.items = []
        self.next_id = 1
        self.load_items()

    def load_items(self):
        """Загрузка задач из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.items = [ToDoItem.load(record) for record in data]
                    if self.items:
                        self.next_id = max(item.id for item in self.items) + 1
            except (json.JSONDecodeError, FileNotFoundError):
                self.items = []
                self.next_id = 1

    def save_items(self):
        """Сохранение задач в файл"""
        data = [task.export() for task in self.items]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def create_item(self, title, priority="normal"):
        """Создание новой задачи"""
        item = ToDoItem(self.next_id, title, priority, False)
        self.next_id += 1
        self.items.append(item)
        self.save_items()
        return item

    def get_all_items(self):
        """Получение всех задач"""
        return self.items

    def get_item_by_id(self, item_id):
        """Получение задачи по ID"""
        for item in self.items:
            if item.id == item_id:
                return item
        return None

    def mark_item_complete(self, item_id):
        """Отметка задачи как выполненной"""
        item = self.get_item_by_id(item_id)
        if item:
            item.is_done = True
            self.save_items()
            return True
        return False
