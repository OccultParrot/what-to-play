import os.path
import random
import sys
from typing import Callable, Dict, List, Any, Generator

from rich.console import Console


def get_data_path() -> str:
    """
    Returns the path to the data directory, handling both development and bundled environments.
    """
    # Production environment
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'data')
    # Development environment
    else:
        return os.path.join(os.path.dirname(__file__), 'data')


# region Saving & Loading        
def save_paths() -> None:
    """
    Saves the paths to a file named "paths.txt". If the file already exists, it will be overwritten.
    """
    data_dir = get_data_path()
    with open(os.path.join(data_dir, "paths.txt"), "w") as file:
        for path in paths:
            file.write(path + "\n")
    print("Paths saved successfully.")


def load_paths() -> list[str]:
    """
    Loads the paths from a file, or uses a default file if it does not exist.
    """
    data_dir = get_data_path()
    path = os.path.join(data_dir, "paths.txt")
    if not os.path.exists(path):
        path = os.path.join(data_dir, "paths.default.txt")
    with open(path, "r") as file:
        loaded_paths = file.readlines()
        return [path.strip().replace("[user]", os.environ["username"]) for path in loaded_paths]


# endregion

def get_games() -> Generator[str, Any, None]:
    """
    Generator that yields available games.
    :return: The name of the game, formatted with spaces and title case.
    """
    for path in paths:
        if not os.path.exists(path):
            print(f"Path {path} does not exist, skipping...")
            continue
        for child in os.listdir(path):
            yield child.replace("_", " ").title().strip()


class Command:
    """
    This is so I can easily add commands to the console, and have the array actually look good.
    """

    def __init__(self, description: str, callback: Callable[[str], None]) -> None:
        self.description: str = description
        self.callback: Callable[..., None] = callback


# region Commands
def help_command(*args: str) -> None:
    for key, command in commands.items():
        console.print(f"[green]{key}[/] - [blue]{command.description}[/]")


def exit_command(*args: str) -> None:
    print("\nExiting...")
    save_paths()
    sys.exit(0)


def clear_command(*args: str) -> None:
    console.clear()


def pick_command(*args: str) -> None:
    console.print(f"Play [bold green]{random.choice([game for game in get_games()])}[/]")


def append_command(*args: str) -> None:
    path = args[0]
    paths.append(path)


def list_command(*args: str) -> None:
    for game in get_games():
        console.print(game)


# endregion

console = Console()

paths: List[str] = load_paths()

commands: Dict[str, Command] = {
    "help": Command("Lists all available commands", help_command),
    "pick": Command("Picks a random game for you to play", pick_command),
    "append-path": Command("Appends the selected path to the path list", append_command),
    "list-games": Command("Lists all games found in the paths", list_command),
    "clear": Command("Clears the console", clear_command),
    "exit": Command("Exits the console", exit_command),
}


def interpret_command(line: str) -> bool:
    """
    Looks at the line the user entered and checks if it starts with any of the commands.
    :param line: The line the user entered, usually structured like command arg1 arg2 ...
    :return: false if the command was not found, true if it was found and executed. \
        (EXCEPT FOR THE CLEAR COMMAND WHICH ALWAYS RETURNS FALSE)
    """
    for key, value in commands.items():
        if line.lower().startswith(key):
            args = line.split(" ")
            args.pop(0)
            value.callback(*args)
            # so we dont have a newline after we clear the console
            if key == "clear":
                return False
            return True
    return False


def main():
    load_paths()

    console.clear()
    console.print("Run \"help\" for list of commands")

    while True:
        try:
            line = console.input("> ")
            if interpret_command(line):
                console.print()  # Print a newline after command execution
        except KeyboardInterrupt:
            exit_command()


if __name__ == '__main__':
    main()