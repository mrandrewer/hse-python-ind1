# Класс для представления задачи
class TodoItem:
    def __init__(self, title, priority="normal", is_done=False, item_id=None):
        self.title = title
        self.priority = priority
        self.is_done = is_done
        self.id = item_id

    def to_dict(self):
        """Экспорт данных в словарь"""
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "isDone": self.is_done,
        }

    @classmethod
    def from_dict(cls, data):
        """Импорт данных из словаря"""
        return cls(
            title=data.get("title", ""),
            priority=data.get("priority", "normal"),
            is_done=data.get("isDone", False),
            item_id=data.get("id"),
        )
