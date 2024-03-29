# The code will be modified based on the provided file.

import tkinter as tk
import random
from tkinter import messagebox
from tkinter import simpledialog

# Create the main window
window = tk.Tk()
window.title("Minesweeper")

# Ask the player for the size of the board
rows = simpledialog.askinteger("Input", "Please enter the number of rows: ", minvalue=1, maxvalue=100)
cols = simpledialog.askinteger("Input", "Please enter the number of columns: ", minvalue=1, maxvalue=100)

# Ask the player for the difficulty
difficulty = simpledialog.askstring("Input", "Please enter the difficulty (easy, medium, hard): ")

# Validate the difficulty
if difficulty not in ["easy", "medium", "hard"]:
    messagebox.showerror("Error", "Invalid difficulty")
    window.quit()
    exit()

# Calculate the number of mines
if difficulty == "easy":
    num_mines = random.randint(int(0.15 * rows * cols), int(0.20 * rows * cols))
elif difficulty == "medium":
    num_mines = random.randint(int(0.20 * rows * cols), int(0.25 * rows * cols))
else:  # hard
    num_mines = random.randint(int(0.25 * rows * cols), int(0.30 * rows * cols))

# Variable to keep track of the number of marked mines
num_marked_mines = 0

# Initialize the minefield and the numbers matrix
minefield = [[0 for _ in range(cols)] for _ in range(rows)]
numbers = [[0 for _ in range(cols)] for _ in range(rows)]

first_click = True

# Variable to keep track of whether the 'm' key is pressed
mark_mode = tk.BooleanVar(window, False)

# Create a label frame for displaying game status information
status_frame = tk.Frame(window)
status_frame.grid(row=0, column=0, columnspan=cols)

# Create a label to display the current mode and add it to the status frame
mode_label = tk.Label(status_frame, text="Mode: Clear")
mode_label.pack(side='left')

# Create a label to display the number of marked mines and remaining mines, and add it to the status frame
mines_label = tk.Label(status_frame)
mines_label.pack(side='left')

def update_mode_label():
    mode_label["text"] = "Mode: Mark" if mark_mode.get() else "Mode: Clear"

def update_mines_label():
    mines_label["text"] = f"Mines marked: {num_marked_mines} / Remaining: {num_mines - num_marked_mines}"

update_mode_label()
update_mines_label()

def check_game_over():
    for i in range(rows):
        for j in range(cols):
            button_text = buttons[i][j]["text"]
            if minefield[i][j] == 1:  # mine
                if button_text != "M":  # not marked
                    return
            else:  # not mine
                if button_text == "_" or button_text == "M":  # not cleared or wrongly marked
                    return
    # If we reach here, the player has won
    messagebox.showinfo("Congratulations", "You win!")
    window.quit()

# Function to handle key press and release events
def toggle_mark_mode(event):
    mark_mode.set(not mark_mode.get())
    update_mode_label()

window.bind('m', toggle_mark_mode)

# Create a new frame for the labels
label_frame = tk.Frame(window)
label_frame.grid(row=0, column=0, sticky='ew')

# Move the labels into the new frame
mode_label.master = label_frame
mines_label.master = label_frame

mode_label.pack(side='left')
mines_label.pack(side='left')

# Create a button for each cell
buttons = [[None for _ in range(cols)] for _ in range(rows)]
for i in range(rows):
    for j in range(cols):
        button = tk.Button(window, text="_", width=2)
        button.grid(row=i+1, column=j)  # Add 1 to the row index to make room for the mode label
        buttons[i][j] = button

        # Bind the left mouse button click to the clear or mark action, depending on the mark_mode variable
        button.bind("<Button-1>", lambda event, row=i, col=j: mark(row, col) if mark_mode.get() else clear(row, col))

# Configure the rows and columns to expand proportionally with the window size
for i in range(rows+1):
    window.grid_rowconfigure(i, weight=1)
for j in range(cols):
    window.grid_columnconfigure(j, weight=1)

def update_button(row, col):
    button = buttons[row][col]
    colors = ["", "blue", "green", "red", "purple", "maroon", "turquoise", "black", "gray"]
    if minefield[row][col] == 1:  # mine
        button.config(text="M", bg="red")
    elif numbers[row][col] > 0:  # number
        button.config(text=str(numbers[row][col]), bg="white", fg=colors[numbers[row][col]])
    else:  # empty cell
        button.config(text="", bg="white")

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

    # Check if the move is on a mine
    if minefield[row][col] == 1:
        messagebox.showinfo("Game over", "You hit a mine!")
        window.quit()
        return

    update_button(row, col)
    if numbers[row][col] == 0:
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if 0 <= row + x < rows and 0 <= col + y < cols and buttons[row + x][col + y]["text"] == "_":
                    clear(row + x, col + y)

    check_game_over()

# Function to handle mark action
def mark(row, col):
    global num_marked_mines
    button = buttons[row][col]
    if button["text"] == "M":  # if the cell is already marked, unmark it
        button.config(text="_", bg="light grey")
        num_marked_mines -= 1
    else:  # mark the cell
        button.config(text="M", bg="red")
        num_marked_mines += 1
    update_mines_label()
    check_game_over()

# Start the main event loop
window.mainloop()
