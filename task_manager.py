from file_handler import load_tasks, save_tasks

tasks = load_tasks()

def add_task(description, priority="Medium", due_date=None):
    if not description.strip():
        return False
    task = {
        "description": description,
        "completed": False,
        "priority": priority,
        "due_date": due_date
    }
    tasks.append(task)
    save_tasks(tasks)
    return True

def list_tasks():
    if not tasks:
        return []
    return tasks

def edit_task(index, new_description):
    if 0 <= index < len(tasks) and new_description.strip():
        tasks[index]["description"] = new_description
        save_tasks(tasks)
        return True
    return False

def delete_task(index):
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
        return True
    return False

def toggle_task(index):
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]
        save_tasks(tasks)
        return True
    return False

def mark_all_complete():
    for task in tasks:
        task["completed"] = True
    save_tasks(tasks)

def clear_completed_tasks():
    global tasks
    tasks = [t for t in tasks if not t["completed"]]
    save_tasks(tasks)
