import tkinter as tk
from tkinter import messagebox
from task_manager import add_task, list_tasks, delete_task, toggle_task
from task_manager import mark_all_complete  # we'll add this function next
from task_manager import clear_completed_tasks  # Add this at the top if not already
from datetime import datetime

visible_tasks = []

def handle_mark_all_complete():
    mark_all_complete()
    refresh_listbox()

def handle_clear_completed():
    clear_completed_tasks()
    refresh_listbox()

def refresh_listbox():
    keyword = search_var.get().lower()
    sort_method = sort_var.get()
    
    all_tasks = list_tasks()

    # Filter by search
    global visible_tasks
    visible_tasks = [t for t in all_tasks if keyword in t["description"].lower()]

    # Sort logic
    if sort_method == "Priority":
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        visible_tasks.sort(key=lambda t: priority_order.get(t["priority"], 3))
    elif sort_method == "Due Date":
        visible_tasks.sort(key=lambda t: t["due_date"] or "9999-99-99")
    elif sort_method == "Completion":
        visible_tasks.sort(key=lambda t: t["completed"])

    task_listbox.delete(0, tk.END)

    for i, task in enumerate(visible_tasks):
        status = "✅" if task["completed"] else "❌"
        due = task["due_date"] or "None"

        is_overdue = False
        if task["due_date"]:
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d").date()
                is_overdue = not task["completed"] and due_date < datetime.today().date()
            except:
                pass

        display = f"{i+1}. {task['description']} [Priority: {task['priority']}, Due: {due}] {status}"

        index = task_listbox.size()
        task_listbox.insert(tk.END, display)

        if task["completed"]:
            task_listbox.itemconfig(index, fg="green")
        elif is_overdue:
            task_listbox.itemconfig(index, fg="red")
        else:
            task_listbox.itemconfig(index, fg="yellow")




def handle_add():
    desc = task_entry.get().strip()
    if not desc:
        messagebox.showerror("Error", "Task description cannot be empty.")
        return
    priority = priority_var.get()
    due = due_entry.get().strip() or None
    if add_task(desc, priority, due):
        refresh_listbox()
        task_entry.delete(0, tk.END)
        due_entry.delete(0, tk.END)

def handle_delete():
    selection = task_listbox.curselection()
    if not selection:
        messagebox.showinfo("Info", "No task selected.")
        return
    index = selection[0]
    task = visible_tasks[index]
    toggle_task(list_tasks().index(task))
    refresh_listbox()

def handle_toggle():
    selection = task_listbox.curselection()
    if not selection:
        messagebox.showinfo("Info", "No task selected.")
        return
    index = selection[0]
    task = visible_tasks[index]
    toggle_task(list_tasks().index(task))
    refresh_listbox()




root = tk.Tk()
root.title("To-Do List")
root.geometry("800x420")
root.configure(bg="#1e1e2f", padx=10, pady=10)
input_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame = tk.Frame(root, bg="#1e1e2f")


priority_var = tk.StringVar(value="Medium")

def update_priority_color(*args):
    val = priority_var.get()
    if val == "Low":
        priority_menu.configure(bg="#4CAF50", fg="white")  # Green
    elif val == "Medium":
        priority_menu.configure(bg="#2196F3", fg="white")  # Blue
    elif val == "High":
        priority_menu.configure(bg="#f44336", fg="white")  # Red




# Input Frame
input_frame = tk.Frame(root, bg="#1e1e2f")
input_frame.pack(pady=10, fill=tk.X)


task_entry = tk.Entry(input_frame, width=40)

task_label = tk.Label(input_frame, text="Task Name:", bg="#1e1e2f", fg="white")
task_label.pack(side=tk.LEFT, padx=(0, 5))

task_entry.pack(side=tk.LEFT, padx=5)
task_entry.configure(bg="#1e1e2f", fg="#FFFFFF", insertbackground="#1e1e2f")

priority_menu = tk.OptionMenu(input_frame, priority_var, "Low", "Medium", "High")
priority_menu.configure(width=8, font=("Segoe UI", 10), highlightthickness=0, bd=0)
priority_menu.pack(side=tk.LEFT, padx=5)

priority_var.trace_add("write", update_priority_color)
update_priority_color()

due_entry = tk.Entry(input_frame, width=15)
due_entry.insert(0, "YYYY-MM-DD")
due_entry.pack(side=tk.LEFT, padx=5)
due_entry.configure(bg="#1e1e2f", fg="#FFFFFF", insertbackground="#1e1e2f")


add_btn = tk.Button(input_frame, text="Add Task", bg="#4CAF50", fg="white", command=handle_add)
add_btn.pack(side=tk.LEFT, padx=5)

search_var = tk.StringVar()

search_frame = tk.Frame(root, bg="#1e1e2f")
search_frame.pack(pady=(0, 5), fill=tk.X)


search_label = tk.Label(search_frame, text="Search:", bg="#1e1e2f", fg="white")
search_label.pack(side=tk.LEFT, padx=(0, 5))

search_entry = tk.Entry(search_frame, textvariable=search_var, width=40)
search_entry.pack(side=tk.LEFT, padx=5)
search_entry.configure(bg="#1e1e2f", fg="#FFFFFF", insertbackground="#FFFFFF")


search_var.trace_add("write", lambda *args: refresh_listbox())

sort_container = tk.Frame(search_frame, bg="#1e1e2f")
sort_container.pack(side=tk.RIGHT, padx=5)

sort_var = tk.StringVar(value="None")

sort_label = tk.Label(search_frame, text="Sort:", bg="#1e1e2f", fg="white")
sort_label.pack(side=tk.LEFT, padx=(0, 5))

sort_menu = tk.OptionMenu(
    search_frame,
    sort_var,
    "None",        
    "Priority",
    "Due Date",
    "Completion"
)
sort_menu.configure(width=12, font=("Segoe UI", 10), highlightthickness=0, bd=0, bg="#333", fg="white")
sort_menu.pack(side=tk.LEFT, padx=5)

sort_var.trace_add("write", lambda *args: refresh_listbox())



# task list
task_listbox = tk.Listbox(root, width=100, height=12, font=("Segoe UI", 10), bg="#2c2c3c", fg="white", selectbackground="#444", selectforeground="white")
task_listbox.pack(pady=10)

# buttons frame
btn_frame = tk.Frame(root, bg="#1e1e2f")
btn_frame.pack(pady=5)

toggle_btn = tk.Button(btn_frame, text="Toggle Status", bg="#2196F3", fg="white", width=20, command=handle_toggle)
toggle_btn.pack(side=tk.LEFT, padx=10)

delete_btn = tk.Button(btn_frame, text="Delete Task", bg="#f44336", fg="white", width=20, command=handle_delete)
delete_btn.pack(side=tk.LEFT, padx=10)

mark_all_btn = tk.Button(btn_frame, text="Mark All Complete", bg="#9C27B0", fg="white", width=20, command=handle_mark_all_complete)
mark_all_btn.pack(side=tk.LEFT, padx=10)

clear_btn = tk.Button(btn_frame, text="Clear Completed", bg="#FF9800", fg="white", width=20, command=handle_clear_completed)
clear_btn.pack(side=tk.LEFT, padx=10)


refresh_listbox()
root.mainloop()