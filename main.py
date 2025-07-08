"""
We want to save the paths to a file
"""
import os.path
from typing import Callable, Dict, List

from rich.console import Console


# region Saving & Loading
def save_path(path: str):
    with open("paths.txt", "a") as file:
        file.write(path + "\n")


def load_paths() -> list[str]:
    if not os.path.exists("paths.txt"):
        with open("paths.txt", "w") as file:
            file.write("")
    with open("paths.txt", "r") as file:
        loaded_paths = file.readlines()
        return loaded_paths


# endregion

class Command:
    def __init__(self, description: str, callback: Callable[[str], None]) -> None:
        self.description: str = description
        self.callback: Callable[..., None] = callback


# region Commands
def help_command(*args: str) -> None:
    for key, command in commands.items():
        console.print(f"[green]{key}[/] - [blue]{command.description}[/]")


def exit_command(*args: str) -> None:
    print("\nExiting...")
    exit(0)


def clear_command(*args: str) -> None:
    console.clear()


def pick_command(*args: str) -> None:
    print(args)


def append_command(*args: str) -> None:
    path = args[0]
    save_path(path)
    
def list_command(*args: str) -> None:
    pass


# endregion

console = Console()

paths: List[str] = load_paths()

commands: Dict[str, Command] = {
    "help": Command("Lists all available commands", help_command),
    "pick": Command("Picks a random game for you to play", pick_command),
    "append-path": Command("Appends the selected path to the path list", append_command),
    
    "clear": Command("Clears the console", clear_command),
    "exit": Command("Exits the console", exit_command),
}


def interpret_command(line: str) -> None:
    for key, value in commands.items():
        if line.lower().startswith(key):
            args = line.split(" ")
            args.pop(0)
            value.callback(*args)


def main():
    console.clear()
    console.print("Run \"help\" for list of commands")
    while True:
        line = console.input("> ")
        interpret_command(line)
        if not line.lower().startswith("clear"):
            console.print("\n")


if __name__ == '__main__':
    main()
