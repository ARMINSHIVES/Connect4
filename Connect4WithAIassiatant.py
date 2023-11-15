import numpy as np
import sys
import math
import random
import matplotlib.pyplot as plt
WINDOW_LENGTH = 4
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

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

def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None, 100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -10000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def pick_best_move(board, piece):
	valid_locations = get_valid_locations(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		score = score_position(temp_board, piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col

x = []
p1 = []
p1Wins = 0
p2 = []
p2Wins = 0
numGames = 0

totGames = int(input("Enter the number games would you like to play: "))
ROW_COUNT = int(input("Enter the number of rows (must be greater then 4): "))
COLUMN_COUNT = int(input("Enter the number of columns (must be greater then 4): "))

for i in range(totGames):
	print("\nGame {} of {}\n".format(i + 1, totGames))
	board = create_board()
	print_board(board)
	game_over = False
	turn = 0
	winner = 0
	while not game_over:
		print("Best Current Move For Player 1: {} ".format(pick_best_move(board, 1)))
		print("Best Current Move For Player 2: {} ".format(pick_best_move(board, 2)))
		col = int(input("Player {} Turn: ".format(turn + 1)))
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