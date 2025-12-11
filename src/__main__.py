from http.server import HTTPServer
import ToDoHandler


def run_app(port: int = 8080):
    server_address = ("", port)
    httpd = HTTPServer(server_address, ToDoHandler)
    print(f"Starting HTTP server on port {port}...")
    print(f"Access the API at: http://localhost:{port}/tasks")
    httpd.serve_forever()


if __name__ == "__main__":
    run_app()
