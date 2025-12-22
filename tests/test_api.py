from requests import get


class TestToDoAPI:

    BASE_URL = "http://localhost:8080"

    def test_get_empty_tasks_list(self):
        """Тест получения пустого списка задач"""

        response = get(f"{self.BASE_URL}/tasks")
        assert response.status_code == 200
        assert response.json() == []
