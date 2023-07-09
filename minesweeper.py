import random

# Step 1: Initialize the game / minefield
minefield = [[0 for _ in range(10)] for _ in range(10)]
mines = random.sample(range(100), 20)
for mine in mines:
    row = mine // 10
    col = mine % 10
    minefield[row][col] = 1

# Calculate the numbers that represent the number of mines around a cell
numbers = [[0 for _ in range(10)] for _ in range(10)]
for i in range(10):
    for j in range(10):
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if 0 <= i + x < 10 and 0 <= j + y < 10 and minefield[i + x][j + y] == 1:
                    numbers[i][j] += 1

# The game board that the player sees
game_board = [["_" for _ in range(10)] for _ in range(10)]

# Step 2: Game loop
game_over = False
while not game_over:
    # Show the player the current state of the field
    for row in game_board:
        print(' '.join(row))
    
    # Ask the player for a move
    action = input("请选择一个操作（清除(c)或者标记(m)）：")
    move_row = int(input("请输入你的移动行（1-10）：")) - 1  # subtract 1 to convert to 0-indexing
    move_col = int(input("请输入你的移动列（1-10）：")) - 1  # subtract 1 to convert to 0-indexing
    
    # Perform the chosen action
    if action.lower() == "c":
        # Check if the move is on a mine
        if minefield[move_row][move_col] == 1:
            game_over = True
            print("游戏结束，你踩到了地雷！")
        else:
            game_board[move_row][move_col] = str(numbers[move_row][move_col])
            print("安全，继续游戏！")
    elif action.lower() == "m":
        game_board[move_row][move_col] = "M"
        print("格子已被标记。")

    # Check if the player has won
    if all(all(cell != "_" for cell in row) for row in game_board):
        game_over = True
        print("恭喜你，你赢了！")
