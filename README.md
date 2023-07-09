# JustForFun
It's my playground that use GPT-4 code interpreter to generate some interesting codes!

# Minesweeper Game

This is a Minesweeper game implemented in Python. The game can be played in a command-line interface.

## Game Rules

1. At the start of the game, the player is asked to enter the size of the game board (number of rows and columns).
2. Each cell on the game board may hide a mine. The goal of the player is to reveal all cells that don't contain a mine, without revealing any cell that does contain a mine.
3. The player can choose to reveal a cell or mark a cell. Revealing a cell shows whether it contains a mine. Marking a cell helps the player keep track of where they suspect a mine is hidden.
4. If the player reveals a cell that contains a mine, the game ends immediately. If the player reveals all cells that don't contain a mine, they win the game.
5. After each round, the system will display the number of remaining mines, the number of marked mines, and how many mines have not been marked.

## How to Run

In your terminal, run `python minesweeper.py`.
