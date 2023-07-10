import tkinter as tk
import random

# Create the main window
window = tk.Tk()
window.title("Minesweeper")

cols = 10
rows = 10
num_mines = int(0.2 * rows * cols)

# Create the minefield and the numbers that represent the number of mines around a cell
minefield = [[0 for _ in range(cols)] for _ in range(rows)]
numbers = [[0 for _ in range(cols)] for _ in range(rows)]
first_click = True

# Variable to keep track of whether the 'm' key is pressed
mark_mode = tk.BooleanVar(window, False)

# Function to handle key press and release events
def toggle_mark_mode(event):
    mark_mode.set(not mark_mode.get())

window.bind('m', toggle_mark_mode)

# Create a button for each cell
buttons = [[None for _ in range(cols)] for _ in range(rows)]
for i in range(rows):
    for j in range(cols):
        button = tk.Button(window, text="_", width=2)
        button.grid(row=i, column=j)
        buttons[i][j] = button

        # Bind the left mouse button click to the clear or mark action, depending on the mark_mode variable
        button.bind("<Button-1>", lambda event, row=i, col=j: mark(row, col) if mark_mode.get() else clear(row, col))

# Function to handle clear action
def clear(row, col):
    global first_click
    if first_click:
        # Place the mines after the first move
        first_click = False
        # Make sure the first move is not a mine
        safe_cells = list(range(rows * cols))
        safe_cells.remove(cols * row + col)
        mines = random.sample(safe_cells, num_mines)
        for mine in mines:
            mine_row = mine // cols
            mine_col = mine % cols
            minefield[mine_row][mine_col] = 1

        # Calculate the numbers that represent the number of mines around a cell
        for i in range(rows):
            for j in range(cols):
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if 0 <= i + x < rows and 0 <= j + y < cols and minefield[i + x][j + y] == 1:
                            numbers[i][j] += 1

    print("Clear cell at", row, col)

# Function to handle mark action
def mark(row, col):
    print("Mark cell at", row, col)

# Start the main event loop
window.mainloop()
