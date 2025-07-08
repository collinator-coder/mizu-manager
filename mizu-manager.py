import os
import py7zip
import json
import argparse

cli = argparse.ArgumentParser(description="Mizu Manager CLI")
cli.add_argument("--update", action="store_true", help="Update the mizu-manager repository")
cli.add_argument("--bottle-app", nargs=3, metavar=("<bottle_name>", "<app_path>", "<app_executable>"), help="Create a bottle for the specified app")
cli.add_argument("--crack-bottle", nargs=1, metavar=("<bottle_name>"), help="Create the initial config.json file in the user's .localpath directory")
cli.add_argument("--setup", action="store_true", help="Run initial setup. This acts like --ensure-path, with some extra steps.")
cli.add_argument("--ensure-path", action="store_true", help="Ensure that .localpath is in PATH.")

args = cli.parse_args()

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

if(args.update):
    update()

if args.bottle_app:
    if len(args.bottle_app) != 3:
        print("Usage: --bottle-app <bottle_name> <app_path> <app_executable>")
    else:
        bottle_app(args.bottle_app[0], args.bottle_app[1], args.bottle_app[2])
