from copy import deepcopy
import numpy as np

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
MOVE_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
WEIGHT_DISTRIBUTION = np.array([
	[9, 8, 6, 3, 3, 6, 8, 9],
	[8, 7, 5, 2, 2, 5, 7, 8],
	[6, 5, 4, 1, 1, 4, 5, 6],
	[3, 2, 1, 0, 0, 1, 2, 3],
	[3, 2, 1, 0, 0, 1, 2, 3],
	[6, 5, 4, 1, 1, 4, 5, 6],
	[8, 7, 5, 2, 2, 5, 7, 8],
	[9, 8, 6, 3, 3, 6, 8, 9]
])


class Chessboard(object):
	def __init__(self, chessboard_size, cur_player=COLOR_BLACK, params=np.zeros(20)):  # chessboard_size = 8
		self.chessboard_size = (chessboard_size, chessboard_size)
		self.board = np.zeros(self.chessboard_size, dtype=np.int32)
		self.board[(self.chessboard_size[0] >> 1) - 1][(self.chessboard_size[1] >> 1) - 1] = COLOR_WHITE
		self.board[(self.chessboard_size[0] >> 1) - 1][self.chessboard_size[1] >> 1] = COLOR_BLACK
		self.board[self.chessboard_size[0] >> 1][(self.chessboard_size[1] >> 1) - 1] = COLOR_BLACK
		self.board[self.chessboard_size[0] >> 1][self.chessboard_size[1] >> 1] = COLOR_WHITE
		self.to_move = cur_player
		self.board_params = np.zeros(10)
		self.stability_params = 0
		self.mobility_params = np.zeros(6)
		self.frontier_params = np.zeros(3)
		self.pos_params = np.zeros_like(self.board)
		self.load_params(params)

	def set_board(self, board, cur_player):
		self.board = board
		self.to_move = cur_player

	def load_params(self, params):
		self.board_params = params[:10]
		self.stability_params = params[10]
		self.mobility_params = params[11:17]
		self.frontier_params = params[17:20]
		for i in range(self.chessboard_size[0]):
			for j in range(self.chessboard_size[1]):
				self.pos_params[i][j] = self.board_params[WEIGHT_DISTRIBUTION[i][j]]


def get_flip_count(state):
	flip_count = np.zeros_like(state.board)
	for i in range(state.chessboard_size[0]):
		for j in range(state.chessboard_size[1]):
			if state.board[i][j] != COLOR_NONE:
				continue
			for direction in MOVE_DIRECTIONS:
				for step in range(1, state.chessboard_size[0]):
					x = i + step * direction[0]
					y = j + step * direction[1]
					if x < 0 or x >= state.chessboard_size[0] or y < 0 or y >= state.chessboard_size[1]:
						break
					if state.board[x][y] == COLOR_NONE:
						break
					if state.board[x][y] == state.to_move:
						flip_count[i][j] += step - 1
						break
	return flip_count


def get_valid_moves(state):
	flip_count = get_flip_count(state)
	return [(i, j)
		for i in range(state.chessboard_size[0])
		for j in range(state.chessboard_size[1])
		if flip_count[i][j] > 0
	]


def flip_chess(state, move):  # move = (i, j), flips the chess while changing the player
	state = deepcopy(state)
	if move == (-1, -1):
		state.to_move = -state.to_move
		return state
	state.board[move[0]][move[1]] = state.to_move
	for direction in MOVE_DIRECTIONS:
		for step in range(1, state.chessboard_size[0]):
			x = move[0] + step * direction[0]
			y = move[1] + step * direction[1]
			if x < 0 or x >= state.chessboard_size[0] or y < 0 or y >= state.chessboard_size[1]:
				break
			if state.board[x][y] == COLOR_NONE:
				break
			if state.board[x][y] == state.to_move:
				for s in range(1, step):
					state.board[move[0] + s * direction[0]][move[1] + s * direction[1]] = state.to_move
				break
	state.to_move = -state.to_move
	return state


def is_terminal(state):
	return state.board[state.board == COLOR_NONE].size == 0


def utility(state, player):
	_ = np.sum(state.board == player) - np.sum(state.board == -player)
	return -1 if _ > 0 else 1 if _ < 0 else 0


# Heuristic evaluation for Minimax

def get_stable_count(state):
	stable_black = np.zeros_like(state.board)
	stable_white = np.zeros_like(state.board)
	_size = state.chessboard_size[0]

	for ci, cj in [(0, 0), (0, -1), (-1, 0), (-1, -1)]:
		corner_player = state.board[ci][cj]  # TODO
		if corner_player == COLOR_NONE:
			continue
		j_bound = _size
		for i in range(0, _size):
			for j in range(0, j_bound):
				real_i = i if ci == 0 else _size - 1 - i
				real_j = j if cj == 0 else _size - 1 - j
				if state.board[real_i][real_j] == corner_player:
					if corner_player == COLOR_BLACK:
						stable_black[real_i][real_j] = True
					else:
						stable_white[real_i][real_j] = True
				else:
					j_bound = j - 1
					break
		i_bound = _size
		for j in range(0, _size):
			for i in range(0, i_bound):
				real_i = i if ci == 0 else _size - 1 - i
				real_j = j if cj == 0 else _size - 1 - j
				if state.board[real_i][real_j] == corner_player:
					if corner_player == COLOR_BLACK:
						stable_black[real_i][real_j] = True
					else:
						stable_white[real_i][real_j] = True
				else:
					i_bound = i - 1
					break

	stable_count = {
		COLOR_BLACK: np.sum(stable_black),
		COLOR_WHITE: np.sum(stable_white)
	}
	return stable_count


def get_frontier_count(state):
	around_blank = np.zeros_like(state.board)
	_size = state.chessboard_size[0]
	for i in range(_size):
		for j in range(_size):
			if state.board[i][j] != COLOR_NONE:
				continue
			for di, dj in MOVE_DIRECTIONS:
				if (i + di in range(_size)) and (j + dj in range(_size)):
					around_blank[i + di][j + dj] = True
	frontier_count = {
		COLOR_BLACK: np.sum(around_blank & (state.board == COLOR_BLACK)),
		COLOR_WHITE: np.sum(around_blank & (state.board == COLOR_WHITE))
	}
	return frontier_count


def eval_state(state, color, step):
	_to_move = state.to_move
	state.to_move = color
	self_mobility = len(get_valid_moves(state))
	state.to_move = -color
	oppo_mobility = len(get_valid_moves(state))
	state.to_move = _to_move
	if (not self_mobility) and (not oppo_mobility):
		score = np.sum(state.board) * -color
		return 100000 if score > 0 else -100000 if score < 0 else 50000

	pos_score = np.sum(np.multiply(state.board, state.pos_params)) * (-color)

	stable_count = get_stable_count(state)
	self_stable = stable_count[color]
	oppo_stable = stable_count[-color]
	stability_score = state.stability_params * (oppo_stable - self_stable)

	frontier_count = get_frontier_count(state)
	self_frontier = frontier_count[color]
	oppo_frontier = frontier_count[-color]

	if step < 20:
		mobility_score = state.mobility_params[0] * self_mobility - state.mobility_params[1] * oppo_mobility
		frontier_score = state.frontier_params[0] * (oppo_frontier - self_frontier)
	elif step < 40:
		mobility_score = state.mobility_params[2] * self_mobility - state.mobility_params[3] * oppo_mobility
		frontier_score = state.frontier_params[1] * (oppo_frontier - self_frontier)
	else:
		mobility_score = state.mobility_params[4] * self_mobility - state.mobility_params[5] * oppo_mobility
		frontier_score = state.frontier_params[2] * (oppo_frontier - self_frontier)

	score = pos_score + stability_score + mobility_score + frontier_score
	return score
