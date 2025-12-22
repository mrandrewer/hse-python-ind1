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

    def test_get_task_by_id(self):
        """Тест получения задачи по ID"""
        # Сначала создаем задачу
        task_data = {"title": "Task for get test", "priority": "high"}
        create_response = post(f"{self.BASE_URL}/tasks", json=task_data)
        task_id = create_response.json()["id"]

        # Получаем задачу по ID
        get_response = get(f"{self.BASE_URL}/tasks/{task_id}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["id"] == task_id
        assert data["title"] == "Task for get test"
        assert data["priority"] == "high"

    def test_get_task_by_id_invalid(self):
        """Тест получения несуществующей задачи"""
        response = get(f"{self.BASE_URL}/tasks/999")
        assert response.status_code == 404

    def test_mark_task_complete(self):
        """Тест отметки задачи как выполненной"""
        # Создаем задачу
        task_data = {"title": "Task to complete", "priority": "low"}
        create_response = post(f"{self.BASE_URL}/tasks", json=task_data)
        task_id = create_response.json()["id"]

        # Отмечаем как выполненную
        complete_response = post(f"{self.BASE_URL}/tasks/{task_id}/complete")
        assert complete_response.status_code == 200

        # Проверяем, что задача выполнена
        get_response = get(f"{self.BASE_URL}/tasks/{task_id}")
        assert get_response.json()["isDone"] is True

    def test_mark_task_complete_invalid(self):
        """Тест отметки несуществующей задачи как выполненной"""
        response = post(f"{self.BASE_URL}/tasks/999/complete")
        assert response.status_code == 404
