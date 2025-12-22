import pytest
import subprocess
import time
import os


@pytest.fixture(scope="session", autouse=True)
def start_server():
    """Фикстура для запуска и остановки сервера"""
    # Запуск сервера
    server_process = subprocess.Popen(
        ["python", "__main__.py"],
        env=os.environ
        | {"TASKS_SERVER_PORT": "8080", "TASKS_DATA_FILE": "test_tasks.txt"},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(3)

    yield

    # Остановка сервера
    server_process.terminate()
    server_process.wait()


@pytest.fixture(autouse=True)
def cleanup_files():
    """Очистка тестовых файлов после каждого теста"""
    yield
    test_files = ["test_tasks.txt"]
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
