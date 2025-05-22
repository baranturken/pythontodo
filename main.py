from task_manager import add_task, list_tasks, edit_task, delete_task, toggle_task

def display_tasks():
    tasks = list_tasks()
    if not tasks:
        print("\nNo tasks available.")
    else:
        print("\n--- TASK LIST ---")
        for i, task in enumerate(tasks):
            status = "✅" if task["completed"] else "❌"
            due = task["due_date"] or "None"
            print(f"{i+1}. {task['description']} [Priority: {task['priority']}, Due: {due}] {status}")
    print()

def main():
    while True:
        print("\n--- TO-DO LIST MENU ---")
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Toggle Completion")
        print("6. Exit")

        choice = input("Your choice (1-6): ").strip()

        if choice == "1":
            display_tasks()

        elif choice == "2":
            desc = input("Task description: ")
            priority = input("Priority (Low/Medium/High): ")
            due = input("Due date (YYYY-MM-DD) or leave blank: ") or None
            if add_task(desc, priority, due):
                print("Task added successfully.")
            else:
                print("Invalid task. Please try again.")

        elif choice == "3":
            display_tasks()
            try:
                index = int(input("Task number to edit: ")) - 1
                new_desc = input("New description: ")
                new_priority = input("New priority (optional): ")
                new_due = input("New due date (optional): ")
                if edit_task(index, new_desc, new_priority or None, new_due or None):
                    print("Task updated.")
                else:
                    print("Invalid input or task number.")
            except:
                print("Please enter a valid number.")

        elif choice == "4":
            display_tasks()
            try:
                index = int(input("Task number to delete: ")) - 1
                if delete_task(index):
                    print("Task deleted.")
                else:
                    print("Invalid task number.")
            except:
                print("Please enter a valid number.")

        elif choice == "5":
            display_tasks()
            try:
                index = int(input("Task number to toggle: ")) - 1
                if toggle_task(index):
                    print("Task status changed.")
                else:
                    print("Invalid task number.")
            except:
                print("Please enter a valid number.")

        elif choice == "6":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please enter 1-6.")

if __name__ == "__main__":
    main()
