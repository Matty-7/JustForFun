import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Minesweeper")

cols = 5
rows = 5

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
    print("Clear cell at", row, col)

# Function to handle mark action
def mark(row, col):
    print("Mark cell at", row, col)

# Start the main event loop
window.mainloop()
