import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TASK_FILE = os.path.join(BASE_DIR, "tasks.txt")

def load_tasks():
    tasks = []
    if not os.path.exists(TASK_FILE):
        return tasks
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            for line in file:
                tasks.append(json.loads(line.strip()))
    except:
        pass
    return tasks

def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w", encoding="utf-8") as file:
            for task in tasks:
                file.write(json.dumps(task, ensure_ascii=False) + "\n")
    except:
        pass
