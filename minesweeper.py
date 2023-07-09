import random

# Ask the player for the size of the board
rows = int(input("请输入棋盘的行数："))
while rows <= 0:
    print("输入无效，请输入一个非零自然数。")
    rows = int(input("请输入棋盘的行数："))

cols = int(input("请输入棋盘的列数："))
while cols <= 0:
    print("输入无效，请输入一个非零自然数。")
    cols = int(input("请输入棋盘的列数："))

# Calculate the number of mines
num_mines = random.randint(int(0.20 * rows * cols), int(0.25 * rows * cols))
print("本局有%d颗地雷。" % num_mines)

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
    print("  " + " ".join(str(i + 1) for i in range(cols)))  # column labels
    for i, row in enumerate(game_board):
        print(str(i + 1) + " " + ' '.join(row))  # row labels
    
    # Ask the player for a move
    action = input("请选择一个操作（清除(c)或者标记(m)）：")
    move_row = int(input("请输入你的移动行（1-%d）：" % rows)) - 1  # subtract 1 to convert to 0-indexing
    move_col = int(input("请输入你的移动列（1-%d）：" % cols)) - 1  # subtract 1 to convert to 0-indexing
    
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
            print("游戏结束，你踩到了地雷！")
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
            print("安全，继续游戏！")
    elif action.lower() == "m":
        if game_board[move_row][move_col] == "M":
            game_board[move_row][move_col] = "_"
            print("格子已被取消标记。")
        else:
            game_board[move_row][move_col] = "M"
            print("格子已被标记。")

    # Check if the player has won
    if all(all(cell != "_" for cell in row) for row in game_board):
        game_over = True
        print("恭喜你，你赢了！")
