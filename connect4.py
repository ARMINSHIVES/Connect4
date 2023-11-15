import numpy as np
import sys
import math
import matplotlib.pyplot as plt

ROW_COUNT = 10
COLUMN_COUNT = 10

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece, num_rows, num_columns):
    for c in range(num_columns - 3):
        for r in range(num_rows):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True
    for c in range(num_columns):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True
    for c in range(num_columns - 3):
        for r in range(num_rows - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True
    for c in range(num_columns - 3):
        for r in range(3, num_rows):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True
    return False


x = []
p1 = []
p1Wins = 0
p2 = []
p2Wins = 0
numGames = 0

totGames = col = int(input("Enter the number games would you like to play: "))

for i in range(totGames):
	print("\nGame {} of {}\n".format(i + 1, totGames))
	board = create_board()
	print_board(board)
	game_over = False
	turn = 0
	winner = 0
	while not game_over:
		col = int(input("Player Turn: "))
		if turn == 0:
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, 1)
				if winning_move(board, 1, ROW_COUNT, COLUMN_COUNT):
					game_over = True
					winner = 1
					p1Wins += 1
					numGames += 1
					x.append(numGames)
					p1.append(p1Wins/numGames)
					p2.append(p2Wins/numGames)
		else:
			if is_valid_location(board, col):
				row = get_next_open_row(board, col)
				drop_piece(board, row, col, 2)
				if winning_move(board, 1, ROW_COUNT, COLUMN_COUNT):
					game_over = True
					winner = 2
					p2Wins += 1
					numGames += 1
					x.append(numGames)
					p1.append(p1Wins/numGames)
					p2.append(p2Wins/numGames)
		print_board(board)
		turn += 1
		turn = turn % 2
	print("Player {} wins game {}".format(winner, i))


xpoints = np.array(x)
ypoints = np.array(p1)
y2points = np.array(p2)
plt.plot(xpoints, ypoints)
plt.plot(xpoints, y2points)
plt.show()