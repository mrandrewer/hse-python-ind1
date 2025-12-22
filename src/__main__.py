from http.server import HTTPServer
import os
from ToDoHandler import ToDoHandler
from ToDoManager import ToDoManager
from functools import partial


def run_app(port: int = 8080, file: str = "tasks.txt"):
    server_address = ("", port)
    manager = ToDoManager(file)
    httpd = HTTPServer(server_address, partial(ToDoHandler, manager))
    print(f"Starting HTTP server on port {port}...")
    print(f"Data file: {file}...")
    print(f"Access the API at: http://localhost:{port}/tasks")
    httpd.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("TASKS_SERVER_PORT", "8080"))
    file = os.environ.get("TASKS_DATA_FILE", "tasks.txt")
    run_app(port, file)
