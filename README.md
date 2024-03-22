# Tic-Tac-Toe Game with AI

This is a command-line based Tic-Tac-Toe game implemented in Python. The game supports both single player and two player modes. In single player mode, you can play against an AI with three difficulty levels: easy, medium, and hard.

## Requirements

- Python 3.6 or higher

## Installation

No additional libraries are required. You can run the game directly using Python.

## Usage

To start the game, run the `tictactoe.py` script:

```bash
python tictactoe.py
```

The game will prompt you to input a command. The available commands are:

- `start [user, easy, medium, hard] [user, easy, medium, hard]`: Starts a new game. The first parameter is for the first player and the second parameter is for the second player. You can choose between 'user' for a human player and 'easy', 'medium', 'hard' for an AI player with different difficulty levels.
- `exit`: Exits the game.

Here is an example of starting a new game with a human player against a hard AI:

```bash
Input command: start user hard
```

During the game, if you are the current player, you will be asked to enter the coordinates for your move. The coordinates should be two numbers from 1 to 3 separated by a space. The first number is the row and the second number is the column.

For example, to place your move in the top right corner of the board, you would enter:

```bash
Enter the coordinates: 1 3
```

The game continues until there is a winner or the board is full and the game is a draw.