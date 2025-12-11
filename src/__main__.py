from TodoManager import ToDoManager


def run_app():
    manager = ToDoManager()
    print(manager.create_item("test", "low"))
    print(manager.get_all_items())
    print(manager.mark_item_complete(1))
    print(manager.mark_item_complete(100))


if __name__ == "__main__":
    run_app()
