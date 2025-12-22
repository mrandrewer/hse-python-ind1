from requests import get, post


class TestToDoAPI:

    BASE_URL = "http://localhost:8080"

    def test_get_empty_tasks_list(self):
        """Тест получения пустого списка задач"""

        response = get(f"{self.BASE_URL}/tasks")
        assert response.status_code == 200
        assert response.json() == []

    def test_create_task(self):
        """Тест создания задачи"""
        task_data = {"title": "Test task", "priority": "normal"}
        response = post(f"{self.BASE_URL}/tasks", json=task_data)
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Test task"
        assert data["priority"] == "normal"
        assert data["isDone"] is False
        assert "id" in data
        assert isinstance(data["id"], int)

    def test_create_task_invalid(self):
        """Тест создания задачи с невалидным приоритетом"""
        task_data = {"title": "Test task", "priority": "invalid"}

        response = post(f"{self.BASE_URL}/tasks", json=task_data)
        assert response.status_code == 400
        data = response.json()
        assert "errors" in data
