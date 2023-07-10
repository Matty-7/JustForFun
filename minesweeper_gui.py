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

# Calculate the number of mines
num_mines = random.randint(int(0.20 * rows * cols), int(0.25 * rows * cols))
num_marked_mines = 0

# Create a label to display the game status
status_label = tk.Label(window, text=f"Rows: {rows}, Columns: {cols}, Mines: {num_mines}, Unmarked: {num_mines}")
status_label.grid(row=0, column=0, columnspan=cols)


# Initialize the minefield and the numbers matrix
minefield = [[0 for _ in range(cols)] for _ in range(rows)]
numbers = [[0 for _ in range(cols)] for _ in range(rows)]

first_click = True

# Variable to keep track of whether the 'm' key is pressed
mark_mode = tk.BooleanVar(window, False)

# Function to update the status label
def update_status():
    status_label["text"] = f"Rows: {rows}, Columns: {cols}, Mines: {num_mines}, Unmarked: {num_mines - num_marked_mines}"

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
    update_status()


# Function to handle key press and release events
def toggle_mark_mode(event):
    mark_mode.set(not mark_mode.get())

window.bind('m', toggle_mark_mode)

# Create a button for each cell
buttons = [[None for _ in range(cols)] for _ in range(rows)]
for i in range(1, rows + 1):  # Shift the rows down by 1 to make space for the status label
    for j in range(cols):
        button = tk.Button(window, text="_", width=2)
        button.grid(row=i, column=j)
        buttons[i - 1][j] = button  # Subtract 1 from i because buttons uses 0-indexing

# Configure the rows and columns to expand proportionally with the window size
for i in range(rows):
    window.grid_rowconfigure(i, weight=1)
for j in range(cols):
    window.grid_columnconfigure(j, weight=1)

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
    update_button(row, col)
    check_game_over()

def update_button(row, col):
    button = buttons[row][col]
    if minefield[row][col] == 1:  # mine
        button.config(text="M", bg="red")
    elif numbers[row][col] > 0:  # number
        button.config(text=str(numbers[row][col]), bg="white")
    else:  # empty cell
        button.config(text="", bg="white")
    update_status()

# Start the main event loop
window.mainloop()