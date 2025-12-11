from TodoManager import ToDoManager


def run_app():
    manager = ToDoManager()
    print(manager.create_task("test", "low"))
    print(manager.get_all_tasks())
    print(manager.mark_task_complete(1))
    print(manager.mark_task_complete(100))


if __name__ == "__main__":
    run_app()
