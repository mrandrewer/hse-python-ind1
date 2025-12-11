VALID_PRIORITIES = ["low", "normal", "high"]


# Класс для представления задачи
class TodoItem:
    def __init__(self, item_id, title, priority="normal", is_done=False):
        self.validate_title(title)
        self.validate_priority(priority)

        self.id = item_id
        self.title = title
        self.priority = priority
        self.is_done = is_done

    def validate_title(self, title):
        """Проверка значения задания"""
        if not title:
            raise "Invalid title: title cannot be empty"

    def validate_priority(self, priority):
        """Проверка значения приоритета"""
        if not priority or priority.lower() not in VALID_PRIORITIES:
            raise f"Invalid priority value: {priority}"

    def export(self):
        """Экспорт данных в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "isDone": self.is_done,
        }

    @classmethod
    def load(cls, data):
        """Импорт данных из словаря"""
        return cls(
            item_id=data.get("id"),
            title=data.get("title", ""),
            priority=data.get("priority", "normal"),
            is_done=data.get("isDone", False),
        )
