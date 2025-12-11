from http.server import HTTPServer
from ToDoHandler import ToDoHandler
from ToDoManager import ToDoManager
from functools import partial


def run_app(port: int = 8080):
    server_address = ("", port)
    manager = ToDoManager()
    httpd = HTTPServer(server_address, partial(ToDoHandler, manager))
    print(f"Starting HTTP server on port {port}...")
    print(f"Access the API at: http://localhost:{port}/tasks")
    httpd.serve_forever()


if __name__ == "__main__":
    run_app()
