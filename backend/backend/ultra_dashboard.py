import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from monitor import shared_data
from collections import deque

root = tk.Tk()
root.title("IoT Security ULTRA Dashboard")
root.geometry("1100x700")
root.configure(bg="#121212")

title = tk.Label(root, text="IoT Security Monitoring (ULTRA)",
                 font=("Arial", 18, "bold"),
                 fg="white", bg="#121212")
title.pack(pady=10)

status_label = tk.Label(root, text="System Status: SECURE",
                        font=("Arial", 14),
                        fg="green", bg="#121212")
status_label.pack()

search_var = tk.StringVar()
tk.Entry(root, textvariable=search_var).pack(pady=5)

frame = tk.Frame(root, bg="#121212")
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame, columns=("IP", "Packets", "Threat"), show="headings")
for col in ("IP", "Packets", "Threat"):
    tree.heading(col, text=col)
    tree.column(col, anchor="center")

tree.pack(fill="both", expand=True)

canvas = tk.Canvas(root, height=200, bg="black")
canvas.pack(fill="x")

history = deque(maxlen=20)

def get_threat(count):
    if count < 200:
        return "LOW"
    elif count < 500:
        return "MEDIUM"
    return "HIGH"

def update_dashboard():
    while True:
        data = dict(shared_data)
        history.append(data)

        for row in tree.get_children():
            tree.delete(row)

        high = False
        search = search_var.get()

        for ip, count in data.items():
            if search and search not in ip:
                continue

            threat = get_threat(count)

            if threat == "HIGH":
                high = True

            tree.insert("", "end", values=(ip, count, threat))

        if high:
            status_label.config(text="System Status: UNDER THREAT", fg="red")
        else:
            status_label.config(text="System Status: SECURE", fg="green")

        canvas.delete("all")

        x = 10
        for snapshot in history:
            for ip, count in snapshot.items():
                y = 200 - min(count, 500)/2
                canvas.create_oval(x, y, x+5, y+5, fill="cyan")
            x += 20

        time.sleep(2)

threading.Thread(target=update_dashboard, daemon=True).start()

root.mainloop()