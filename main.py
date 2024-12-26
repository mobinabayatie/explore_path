from tkinter import ttk
from tkinter.messagebox import WARNING
from ttkbootstrap import Window, Label, Entry, Button, Treeview, OUTLINE, PRIMARY, INFO, SUCCESS, WARNING, DANGER
import os
from pathlib import Path
from datetime import datetime
from ttkbootstrap.dialogs import Messagebox
from fnmatch import fnmatch


window = Window(title="Explore Path App", themename="flatly")

window.rowconfigure(4, weight=1)
window.columnconfigure(1, weight=1)

path_label = Label(window, text="Path")
path_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

path_entry = Entry(window)
path_entry.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="ew")

item_list = []

progress_bar = ttk.Progressbar(
    window,
    orient="horizontal",
    mode="determinate",
    length=300,
)
progress_bar.grid(row=5, column=0, columnspan=4, pady=(10, 0), padx=10, sticky="ew")
progress_bar.grid_remove()


def explore_path():
    progress_bar.grid()  # نمایش ProgressBar
    progress_bar["value"] = 0  # مقدار اولیه

    path = path_entry.get()
    for item in item_list:
        explore_tree_view.delete(item)
    item_list.clear()

    row_number = 1
    path_lib = Path(path)
    total_items = len(list(path_lib.iterdir()))

    for idx, windows_path in enumerate(path_lib.iterdir(), start=1):
        entry_type = "File"
        entry_size = ""

        information = windows_path.stat()

        if windows_path.is_dir():
            entry_type = "Folder"
        else:
            entry_size = information.st_size // 1024

        date_created = datetime.fromtimestamp(information.st_ctime)
        date_modified = datetime.fromtimestamp(information.st_mtime)
        date_accessed = datetime.fromtimestamp(information.st_atime)

        item = explore_tree_view.insert(
            "", "end", iid=str(windows_path), text=str(row_number),
            values=(windows_path.name, entry_type, entry_size, date_created, date_modified, date_accessed)
        )
        item_list.append(item)
        row_number += 1

        progress_bar["value"] = (idx / total_items) * 100  # به‌روزرسانی مقدار ProgressBar
        window.update_idletasks()

    progress_bar.grid_remove()

    # for dir_entry in os.scandir(path):
    #     entry_type = "File"
    #     entry_size = ""
    #
    #     information = dir_entry.stat()
    #     if dir_entry.is_dir():
    #         entry_type = "Folder"
    #
    #     else:
    #         entry_size = information.st_size // 1024
    #
    #     created_time = datetime.fromtimestamp(information.st_birthtime)
    #     modified_time = datetime.fromtimestamp(information.st_mtime)
    #     accessed_date = datetime.fromtimestamp(information.st_atime)
    #     item = explore_tree_view.insert("", "end", iid=dir_entry.path, text=str(row_number),
    #                                     values=(dir_entry.name, entry_type, entry_size, created_time, modified_time,
    #                                             accessed_date))
    #     item_list.append(item)
    #     row_number += 1


explore_button = Button(window, text="Explore", bootstyle=SUCCESS + OUTLINE, command=explore_path)
explore_button.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="ew")


def open_folder():
    full_path = explore_tree_view.selection()[0]
    path_entry.delete(0, "end")
    path_entry.insert(0, full_path)
    explore_path()


open_button = Button(window, text="Open", bootstyle=INFO + OUTLINE, command=open_folder)
open_button.grid(row=0, column=3, padx=10, pady=10, sticky="w")

new_folder_label = Label(window, text="New Folder")
new_folder_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="e")

new_folder_entry = Entry(window)
new_folder_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")


def create_folder():
    new_folder = new_folder_entry.get()
    path_lib = Path(new_folder)

    # if os.path.exists(new_folder):
    if path_lib.exists():
        Messagebox.show_error(title="Exists", message="Cannot create a file when that file already exists")
    else:
        # os.mkdir(new_folder)
        path_lib.mkdir()
        Messagebox.show_info(title="Info", message="Folder has been created .")


search_label = Label(window, text="Search")
search_label.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="e")

search_entry = Entry(window)
search_entry.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="ew")


def search():
    term = search_entry.get()
    path = path_entry.get()

    for item in item_list:
        explore_tree_view.delete(item)
    item_list.clear()

    row_number = 1

    for main_folder, folder_list, file_list in os.walk(path):
        for file in file_list:
            if fnmatch(file, term):
                fullpath = os.path.join(main_folder, file)

                try:
                    path_lib = Path(fullpath)

                    entry_type = "File"
                    entry_size = ""

                    if path_lib.is_dir():
                        entry_type = "Folder"
                    else:
                        entry_size = path_lib.stat().st_size // 1024

                    date_created = datetime.fromtimestamp(path_lib.stat().st_ctime)
                    date_modified = datetime.fromtimestamp(path_lib.stat().st_mtime)
                    date_accessed = datetime.fromtimestamp(path_lib.stat().st_atime)

                    item = explore_tree_view.insert("", "end", iid=str(path_lib), text=str(row_number),
                                                    values=(path_lib.name, entry_type, entry_size, date_created,
                                                            date_modified, date_accessed))
                    item_list.append(item)
                    row_number += 1

                except FileNotFoundError:
                    Messagebox.show_error(title="Error", message=f"File not found: {fullpath}")
                except PermissionError:
                    Messagebox.show_error(title="Error", message=f"Permission denied: {fullpath}")



search_button = Button(window, text="Search", bootstyle=WARNING + OUTLINE, command=search)
search_button.grid(row=2, column=2, padx=(0, 10), pady=(0, 10), sticky="ew")

new_folder_button = Button(window, text="New Folder", bootstyle=PRIMARY + OUTLINE, command=create_folder)
new_folder_button.grid(row=1, column=2, padx=(0, 10), pady=(0, 10), sticky="w")

def delete_file():
    delete_file=explore_tree_view.selection()
    for file in delete_file:
        os.remove(file)


    explore_path()

delete_file_button=Button(window,text="Delete",bootstyle=DANGER+OUTLINE,command=delete_file)
delete_file_button.grid(row=3, column=1, padx=(0, 10), pady=(0, 10), sticky="nsew")

explore_tree_view = Treeview(window, columns=("name", "type", "size", "created", "modified", "accessed"))
explore_tree_view.grid(row=4, column=1, padx=(0, 10), pady=(0, 10), sticky="nsew")

explore_tree_view.heading("#0", text="#")
explore_tree_view.heading("#1", text="name")
explore_tree_view.heading("#2", text="Type")
explore_tree_view.heading("#3", text="Size(Kb)")
explore_tree_view.heading("#4", text="Date Created")
explore_tree_view.heading("#5", text="Date Modified")
explore_tree_view.heading("#6", text="Date Accessed")

explore_tree_view.column("#0", width=50, anchor="center")
explore_tree_view.column("#1", width=150, anchor="center")
explore_tree_view.column("#2", width=100, anchor="center")
explore_tree_view.column("#3", width=80, anchor="center")


window.mainloop()
