import json
import os

from ToDoItem import TodoItem


# Менеджер задач
class ToDoManager:
    def __init__(self, filename="tasks.txt"):
        self.filename = filename
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.tasks = [TodoItem.from_dict(task) for task in data]
                    if self.tasks:
                        self.next_id = max(task.id for task in self.tasks) + 1
            except (json.JSONDecodeError, FileNotFoundError):
                self.tasks = []
                self.next_id = 1

    def save_tasks(self):
        """Сохранение задач в файл"""
        tasks_data = [task.to_dict() for task in self.tasks]
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(tasks_data, f, ensure_ascii=False, indent=2)

    def create_task(self, title, priority="normal"):
        """Создание новой задачи"""
        task = TodoItem(title, priority, False, self.next_id)
        self.next_id += 1
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_all_tasks(self):
        """Получение всех задач"""
        return self.tasks

    def get_task_by_id(self, task_id):
        """Получение задачи по ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def mark_task_complete(self, task_id):
        """Отметка задачи как выполненной"""
        task = self.get_task_by_id(task_id)
        if task:
            task.is_done = True
            self.save_tasks()
            return True
        return False
