# What to Play

This is a small project I wrote after being inspired by my good friend Joey.

## Installation / Setup

There are two options: [Install the exe](https://github.com/OccultParrot/what-to-play/releases), or clone the script and run it with Python.

### Cloning the Script

1. Clone the repository:
    ```bash
    git clone git@github.com:OccultParrot/what-to-play.git
   ```
2. Navigate to directory and set up a virtual environment:
   ```bash
   cd what-to-play
   python -m venv .venv
   ```
3. Activate the virtual environment:
    - On Windows:
      ```bash
      .venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source .venv/bin/activate
      ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the script:
   ```bash
    python what_to_play.py
    ```

## Usage
There are multiple commands built into the script:
- `help`: Displays all commands and their descriptions.
- `pick` - Picks a random game for you to play
- `append-path` - Appends the selected path to the path list
- `list-games` - Lists all games found in the paths
- `clear` - Clears the console
- `exit` - Exits the console

The script by default will look for games in the following directories:
- C:\Program Files (x86)\Steam\steamapps\common
- C:\Program Files (x86)\Epic Games
- C:\Users\[user]\AppData\Roaming\itch\apps

You can add additional paths by using the `append-path` command followed by the path you want to add.