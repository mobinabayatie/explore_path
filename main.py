from ttkbootstrap import Window, Label, Entry, Button, Treeview, OUTLINE, PRIMARY, INFO
import os
from datetime import datetime

window = Window(title="Explore Path app", themename="darkly")

window.rowconfigure(1, weight=1)
window.columnconfigure(1, weight=1)

path_label = Label(window, text="Label")
path_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

path_entry = Entry(window)
path_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

item_list = []


def explore_path():
    path = path_entry.get()

    for item in item_list:
        explore_tree_view.delete(item)
    item_list.clear()
    row_number = 1

    for dir_entry in os.scandir(path):
        entry_type = "File"
        entry_size = ""

        information = dir_entry.stat()
        if dir_entry.is_dir():
            entry_type = "Folder"

        else:
            entry_size = information.st_size // 1024

        created_time = datetime.fromtimestamp(information.st_birthtime)
        modified_time = datetime.fromtimestamp(information.st_mtime)
        accessed_date = datetime.fromtimestamp(information.st_atime)
        item = explore_tree_view.insert("", "end", iid=dir_entry.path, text=str(row_number),
                                        values=(dir_entry.name, entry_type, entry_size, created_time, modified_time,
                                                accessed_date))
        item_list.append(item)
        row_number += 1


explore_button = Button(window, text="Explore", command=explore_path)
explore_button.grid(row=0, column=2, padx=(0, 10), pady=10, sticky="w")


def open_folder():
    full_path = explore_tree_view.selection()[0]
    path_entry.delete(0, "end")
    path_entry.insert(0, full_path)
    explore_path()


open_button = Button(window, text="Open", command=open_folder)
open_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

explore_tree_view = Treeview(window, columns=("name", "type", "size", "created", "modified", "accessed"))
explore_tree_view.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="nsew")

explore_tree_view.heading("#0", text="#")
explore_tree_view.heading("#1", text="name")
explore_tree_view.heading("#2", text="Type")
explore_tree_view.heading("#3", text="Size(Kb)")
explore_tree_view.heading("#4", text="Date Created")
explore_tree_view.heading("#5", text="Date Modified")
explore_tree_view.heading("#6", text="Date Accessed")

explore_tree_view.column("#0", width=50)

window.mainloop()
