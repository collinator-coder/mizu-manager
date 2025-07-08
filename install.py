import os
import shutil
import winreg
from git import Repo

def add_path():
    home = os.path.expanduser("~")
    localpath_dir = os.path.join(home, ".localpath")
    os.makedirs(localpath_dir, exist_ok=True)

    # Read user PATH from registry
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_READ) as key:
        try:
            current_path, _ = winreg.QueryValueEx(key, 'PATH')
        except FileNotFoundError:
            current_path = ""

    if localpath_dir.lower() not in current_path.lower():
        new_path = current_path + (";" if current_path else "") + localpath_dir
        # Set new PATH
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Environment', 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, 'PATH', 0, winreg.REG_EXPAND_SZ, new_path)
        print(f"Added {localpath_dir} to user PATH. You may need to restart your terminal.")
    else:
        print(f"{localpath_dir} is already in PATH.")

def copy_files():
    """
    Copies files from the git repo to the user's home directory.
    """
    home = os.path.expanduser("~")
    localpath_dir = os.path.join(home, ".localpath")
    print("Cloning mizu-manager repository...")
    Repo.clone_from("https://github.com/yourusername/mizu-manager.git", localpath_dir)
