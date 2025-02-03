import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
import json

# Nome do arquivo para salvar as tarefas
FILE_NAME = "tasks.json"

class ChecklistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Checklist de Desenvolvimento")
        self.root.geometry("400x550")
        self.root.resizable(False, False)
        self.style = tb.Style("darkly")

        # Lista de tarefas
        self.tasks = []

        # Frame principal
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Campo de entrada
        self.entry = ttk.Entry(self.frame, width=40)
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.add_task)

        # Botão de adicionar tarefa
        self.add_button = ttk.Button(self.frame, text="Adicionar", command=self.add_task, style="primary.Outline.TButton")
        self.add_button.pack(pady=5)

        # Contador de tarefas
        self.counter_label = ttk.Label(self.frame, text="Tarefas: 0 | Concluídas: 0 | Restantes: 0", font=("Helvetica", 10, "bold"))
        self.counter_label.pack(pady=5)

        # Canvas e Scrollbar para lista de tarefas
        self.canvas = tk.Canvas(self.frame, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.canvas.yview)
        self.task_frame = ttk.Frame(self.canvas)
        self.task_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.task_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        self.scrollbar.pack(side="right", fill="y")

        # Carregar tarefas salvas
        self.load_tasks()

    def add_task(self, event=None):
        task_text = self.entry.get().strip()
        if task_text:
            var = tk.BooleanVar()
            task = {"text": task_text, "var": var}
            self.tasks.append(task)
            self.entry.delete(0, tk.END)
            self.update_tasks()
            self.save_tasks()

    def update_tasks(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        
        for task in self.tasks:
            chk = ttk.Checkbutton(
                self.task_frame, text=task["text"], variable=task["var"],
                command=self.toggle_task_style, style="TCheckbutton"
            )
            chk.pack(anchor="w", pady=2)
            self.toggle_task_style()
        
        self.update_counters()

    def toggle_task_style(self):
        for task in self.tasks:
            style = "TCheckbutton" if not task["var"].get() else "TaskCompleted.TCheckbutton"
            self.style.configure("TaskCompleted.TCheckbutton", foreground="gray")
        
        self.save_tasks()
        self.update_counters()

    def update_counters(self):
        total = len(self.tasks)
        completed = sum(task["var"].get() for task in self.tasks)
        remaining = total - completed
        self.counter_label.config(text=f"Tarefas: {total} | Concluídas: {completed} | Restantes: {remaining}")

    def save_tasks(self):
        data = [(task["text"], task["var"].get()) for task in self.tasks]
        with open(FILE_NAME, "w") as file:
            json.dump(data, file)

    def load_tasks(self):
        try:
            with open(FILE_NAME, "r") as file:
                data = json.load(file)
                for text, done in data:
                    var = tk.BooleanVar(value=done)
                    self.tasks.append({"text": text, "var": var})
            self.update_tasks()
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ChecklistApp(root)
    root.mainloop()