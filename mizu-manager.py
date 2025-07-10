import os
import py7zip
import json
import argparse
import sys

import tkinter as tk
from tkinter import messagebox

cli = argparse.ArgumentParser(description="Mizu Manager CLI")
cli.add_argument("--update", action="store_true", help="Update the mizu-manager repository")
cli.add_argument("--bottle-app", nargs=2, metavar=("<bottle_name>", "<app_executable>"), help="Create a bottle for the specified app")
cli.add_argument("--unplug-bottle", nargs=1, metavar=("<bottle_name>"), help="Unplug <bottle_name>")
cli.add_argument("--setup", action="store_true", help="Run initial setup. This acts like --ensure-path, with some extra steps.")
cli.add_argument("--ensure-path", action="store_true", help="Ensure that .localpath is in PATH.")
cli.add_argument("--plug-bottle", action="store_true", help="Plug <bottle_name>")

args = cli.parse_args()

def get_folder_of_bottle(bottle_name):
    return os.path.join(os.path.expanduser("~"), ".localpath", bottle_name)

def get_localpath():
    return os.path.join(os.path.expanduser("~"), ".localpath")

def make_config():
    """
    Creates the initial config.json file in the user's .localpath directory.
    """
    home = os.path.expanduser("~")
    localpath_dir = os.path.join(home, ".localpath")
    os.makedirs(localpath_dir, exist_ok=True)
    config = {
        "bottles": {}
    }
    with open(os.path.join(localpath_dir, "config.json"), "w") as f:
        json.dump(config, f, indent=4)

def update():
    """
    Copies files from the git repo to the user's home directory.
    """
    home = os.path.expanduser("~")
    localpath_dir = os.path.join(home, ".localpath")
    os.system(f"cd {localpath_dir} && git clone https://github.com/collinator-coder/mizu-manager.git")

def is_updatable():
    """
    Checks if the mizu-manager repository is updatable by checking the current version in the config vs the current version.
    """
    home = os.path.expanduser("~")
    config_path = os.path.join(home, ".localpath", "config.json")
    if not os.path.exists(config_path):
        return True  # If config doesn't exist, we can update
    with open(config_path, "r") as f:
        config = json.load(f)
    current_version = config.get("current_version", "0.0.0")
    return config.get("version", "0.0.0") != current_version

def bottle_app(app_name, app_executable):
    """Create a bottle for the app app_name and adds it to the config file."""
    with open(os.path.join(os.path.expanduser("~"), ".localpath", "config.json"), "r+") as f:
        config = json.load(f)
    config["bottles"][app_name] = {
        "path": os.path.join(os.path.expanduser("~"), ".localpath", app_name),
        "executable": app_executable
    }
    with open(os.path.join(os.path.expanduser("~"), ".localpath", "config.json"), "w") as f:
        json.dump(config, f, indent=4)

def launch_gui():

    root = tk.Tk()
    root.title("Mizu Manager")
    root.geometry("400x300")
    root.maxsize(400, 300)
    root.minsize(400,300)
    # Set taskbar icon to mizu.ico if it exists
    icon_path = os.path.join(os.path.dirname(__file__), "mizu.ico")
    if os.path.exists(icon_path):
        try:
            root.iconbitmap(icon_path)
        except Exception as e:
            pass  # Ignore icon errors for now


    label = tk.Label(root, text="Welcome to Mizu Manager!", font=("Arial", 16))
    label.pack(pady=20)

    # Listbox to show bottles
    bottles_listbox = tk.Listbox(root, width=40)
    bottles_listbox.pack(pady=10)

    # Load bottles from config.json
    home = os.path.expanduser("~")
    config_path = os.path.join(home, ".localpath", "config.json")
    bottles = []
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            bottles = config.get("bottles", {}).keys()
    for bottle in bottles:
        bottles_listbox.insert(tk.END, bottle)


    def show_options():
        selected = bottles_listbox.curselection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a bottle first.")
            return
        bottle_name = bottles_listbox.get(selected[0])
        # Options for a bottle
        options = [
            "Unplug (restore from 7z)",
            "Plug (create 7z)",
            "Delete"
        ]

        def unplug_bottle():
            messagebox.showinfo("Unplug", f"Unplug (restore from 7z) for {bottle_name} (not implemented)")
            opt_win.destroy()

        def plug_bottle():
            messagebox.showinfo("Plug", f"Plug (create 7z) for {bottle_name} (not implemented)")
            opt_win.destroy()

        def delete_bottle():
            messagebox.showinfo("Delete", f"Delete for {bottle_name} (not implemented)")
            opt_win.destroy()

        opt_win = tk.Toplevel(root)
        opt_win.title(f"Options for {bottle_name}")
        btns = [
            ("Unplug (restore from 7z)", unplug_bottle),
            ("Plug (create 7z)", plug_bottle),
            ("Delete", delete_bottle)
        ]
        for label, func in btns:
            btn = tk.Button(opt_win, text=label, command=func)
            btn.pack(fill='x', padx=10, pady=5)

    options_btn = tk.Button(root, text="Options", command=show_options)
    options_btn.pack(pady=10)

    root.mainloop()


if len(sys.argv) == 1:
    launch_gui()
else:
    if(args.update):
        update()

    if args.bottle_app:
        if len(args.bottle_app) != 2:
            print("Usage: --bottle-app <bottle_name> <app_executable>")
        else:
            bottle_app(args.bottle_app[0], args.bottle_app[1])