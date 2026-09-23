"""A simple command-line to-do list with persistent JSON storage."""

import json
from pathlib import Path

FILE_PATH = Path(__file__).with_name("tasks.json")


def load_tasks():
    """Load tasks from the JSON file or return an empty list."""
    try:
        with FILE_PATH.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list): 
                return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Warning: tasks file is empty or corrupted. Starting with a new list.")
        return []
    return []


def save_tasks(tasks):
    """Write all tasks to the JSON file."""
    with FILE_PATH.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)  


def get_next_id(tasks):
    """Return the next available task ID."""
    if not tasks:
        return 1
    return max(task.get("id", 0) for task in tasks) + 1

 
def add_task(tasks, description):
    """Create a new task with a unique ID."""
    task = {
        "id": get_next_id(tasks),
        "description": description,
        "completed": False,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added: {description}")


def view_tasks(tasks):
    """Display all tasks in a readable format."""
    if not tasks:
        print("No tasks available.")
        return

    print("\nYour tasks:")
    for task in tasks:
        status = "Done" if task.get("completed") else "Pending"
        print(f"{task.get('id', '?')}. {task.get('description', 'Unknown')} [{status}]")


def mark_task_complete(tasks, task_id):
    """Mark a task as complete if it exists."""
    for task in tasks:
        if task.get("id") == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Task {task_id} marked as completed.")
            return

    raise ValueError(f"Task {task_id} does not exist.")


def delete_task(tasks, task_id):
    """Delete a task by ID."""
    for index, task in enumerate(tasks):
        if task.get("id") == task_id:
            removed = tasks.pop(index)
            save_tasks(tasks)
            print(f"Deleted task: {removed.get('description', 'Unknown')}")
            return

    raise ValueError(f"Task {task_id} does not exist.")


def get_valid_task_id(tasks):
    """Prompt for a valid task ID and return it as an integer."""
    while True:
        try:
            task_id = int(input("Enter task ID: "))
            if not any(task.get("id") == task_id for task in tasks):
                raise ValueError(f"Task {task_id} does not exist.")
            return task_id
        except ValueError as error:
            print(f"Invalid task ID: {error}")


def show_menu():
    """Show the menu."""
    print("\n===== TO-DO LIST =====")
    print("1. Add task")
    print("2. View tasks")
    print("3. Mark task as completed")
    print("4. Delete task")
    print("5. Exit")


def main():
    """Run the to-do list application."""
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            description = input("Enter task description: ").strip()
            if not description:
                print("Task description cannot be empty.")
                continue
            add_task(tasks, description)

        elif choice == "2":
            view_tasks(tasks)

        elif choice == "3":
            try:
                task_id = get_valid_task_id(tasks)
                mark_task_complete(tasks, task_id)
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "4":
            try:
                task_id = get_valid_task_id(tasks)
                delete_task(tasks, task_id)
            except ValueError as error:
                print(f"Error: {error}")

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid menu choice. Please select a valid option.")


if __name__ == "__main__":
    main()
