import tkinter as tk

# Create the main window
window = tk.Tk()
window.title("Minesweeper")

# Create a button for each cell
buttons = [[None for _ in range(cols)] for _ in range(rows)]
for i in range(rows):
    for j in range(cols):
        button = tk.Button(window, text="_", width=2)
        button.grid(row=i, column=j)
        buttons[i][j] = button

# Start the main event loop
window.mainloop()
