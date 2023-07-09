import random
from colorama import Fore, Style

# Define the text for the game in both English and Chinese
text = {
    "en": {
        "ask_rows": "Please enter the number of rows: ",
        "invalid_input": "Invalid input, please enter a positive integer.",
        "ask_cols": "Please enter the number of columns: ",
        "num_mines": "There are {} mines in this game.",
        "ask_action": "Choose an action (clear(c) or mark(m)): ",
        "ask_move_row": "Enter the row of your move (1-{}): ",
        "ask_move_col": "Enter the column of your move (1-{}): ",
        "hit_mine": "Game over, you hit a mine!",
        "safe": "Safe, continue the game!",
        "mark": "Cell has been marked.",
        "unmark": "Cell has been unmarked.",
        "win": "Congratulations, you win!",
        "remaining_mines": "There are {} mines in this game. {} mines have been marked, {} mines are still unmarked."
    },
    "zh": {
        "ask_rows": "请输入棋盘的行数：",
        "invalid_input": "输入无效，请输入一个非零自然数。",
        "ask_cols": "请输入棋盘的列数：",
        "num_mines": "本局有{}颗地雷。",
        "ask_action": "请选择一个操作（清除(c)或者标记(m)）：",
        "ask_move_row": "请输入你的移动行（1-{}）：",
        "ask_move_col": "请输入你的移动列（1-{}）：",
        "hit_mine": "游戏结束，你踩到了地雷！",
        "safe": "安全，继续游戏！",
        "mark": "格子已被标记。",
        "unmark": "格子已被取消标记。",
        "win": "恭喜你，你赢了！",
        "remaining_mines": "本局有{}颗地雷。已标记了{}颗地雷，还有{}颗地雷未被标记。"
    }
}

# Ask the player for the language
language = input("Please choose a language (English(en) or Chinese(zh)): ")
while language not in ["en", "zh"]:
    print("Invalid input, please enter 'en' for English or 'zh' for Chinese.")
    language = input("Please choose a language (English(en) or Chinese(zh)): ")
# Ask the player for the size of the board
rows = int(input(text[language]["ask_rows"]))
while rows <= 0:
    print(text[language]["invalid_input"])
    rows = int(input(text[language]["ask_rows"]))

cols = int(input(text[language]["ask_cols"]))
while cols <= 0:
    print(text[language]["invalid_input"])
    cols = int(input(text[language]["ask_cols"]))

# Calculate the number of mines
num_mines = random.randint(int(0.20 * rows * cols), int(0.25 * rows * cols))
print(text[language]["num_mines"].format(num_mines))

# Step 1: Initialize the game / minefield
minefield = [[0 for _ in range(cols)] for _ in range(rows)]
# The game board that the player sees
game_board = [["_" for _ in range(cols)] for _ in range(rows)]

def reveal_adjacent_cells(row, col):
    for x in [-1, 0, 1]:
        for y in [-1, 0, 1]:
            if 0 <= row + x < rows and 0 <= col + y < cols and game_board[row + x][col + y] == "_" and minefield[row + x][col + y] == 0:
                game_board[row + x][col + y] = str(numbers[row + x][col + y])
                if numbers[row + x][col + y] == 0:
                    reveal_adjacent_cells(row + x, col + y)

# Step 2: Game loop
game_over = False
moves_made = 0
while not game_over:
    # Show the player the current state of the field
    print("  " + " ".join(Fore.RED + str(i + 1) + Style.RESET_ALL for i in range(cols)))  # column labels
    for i, row in enumerate(game_board):
        print(Fore.BLUE + str(i + 1) + Style.RESET_ALL + " " + ' '.join((Fore.YELLOW if cell == "M" else "") + cell + Style.RESET_ALL for cell in row))  # row labels
    
    # Show the player the number of mines left
    num_marked_mines = sum(cell == "M" for row in game_board for cell in row)
    print(text[language]["remaining_mines"].format(num_mines, num_marked_mines, num_mines - num_marked_mines))

    # Ask the player for a move
    action = input(text[language]["ask_action"])
    move_row = int(input(text[language]["ask_move_row"].format(rows))) - 1  # subtract 1 to convert to 0-indexing
    move_col = int(input(text[language]["ask_move_col"].format(cols))) - 1  # subtract 1 to convert to 0-indexing
    
    # Place the mines after the first move
    if moves_made == 0 and action.lower() == "c":
        # Make sure the first move is not a mine
        safe_cells = list(range(rows * cols))
        safe_cells.remove(cols * move_row + move_col)
        mines = random.sample(safe_cells, num_mines)
        for mine in mines:
            row = mine // cols
            col = mine % cols
            minefield[row][col] = 1

    # Calculate the numbers that represent the number of mines around a cell
    numbers = [[0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            for x in [-1, 0, 1]:
                for y in [-1, 0, 1]:
                    if 0 <= i + x < rows and 0 <= j + y < cols and minefield[i + x][j + y] == 1:
                        numbers[i][j] += 1

    # Perform the chosen action
    if action.lower() == "c":
        # Check if the move is on a mine
        if minefield[move_row][move_col] == 1:
            game_over = True
            print(text[language]["hit_mine"])
        else:
            game_board[move_row][move_col] = str(numbers[move_row][move_col])
            if numbers[move_row][move_col] == 0:
                reveal_adjacent_cells(move_row, move_col)
            if moves_made < 3:
                # Randomly reveal 5-10 cells around the move
                revealed_cells = 0
                max_revealed_cells = random.randint(5, 10)
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if 0 <= move_row + x < rows and 0 <= move_col + y < cols and game_board[move_row + x][move_col + y] == "_" and minefield[move_row + x][move_col + y] == 0:
                            game_board[move_row + x][move_col + y] = str(numbers[move_row + x][move_col + y])
                            revealed_cells += 1
                            if revealed_cells == max_revealed_cells:
                                break
                    if revealed_cells == max_revealed_cells:
                        break
                moves_made += 1
            print(text[language]["safe"])
            print(text[language]["num_mines"].format(num_mines))

    elif action.lower() == "m":
        if game_board[move_row][move_col] == "M":
            game_board[move_row][move_col] = "_"
            print(text[language]["unmark"])
        else:
            game_board[move_row][move_col] = "M"
            print(text[language]["mark"])

    # Check if the player has won
    if all(all(cell != "_" for cell in row) for row in game_board):
        game_over = True
        print(text[language]["win"])
