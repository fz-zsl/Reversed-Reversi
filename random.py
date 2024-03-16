import numpy as np
import random

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


MOVE_DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]


class ChessBoard(object):
	def __init__(self, chessboard_size):
		self.chessboard_size = (chessboard_size, chessboard_size)
		self.board = np.zeros(self.chessboard_size, dtype=np.int32)
		self.board[(self.chessboard_size[0] >> 1) - 1][(self.chessboard_size[1] >> 1) - 1] = COLOR_WHITE
		self.board[(self.chessboard_size[0] >> 1) - 1][self.chessboard_size[1] >> 1] = COLOR_BLACK
		self.board[self.chessboard_size[0] >> 1][(self.chessboard_size[1] >> 1) - 1] = COLOR_BLACK
		self.board[self.chessboard_size[0] >> 1][self.chessboard_size[1] >> 1] = COLOR_WHITE

	def get_flip_count(self, color):
		flip_count = np.zeros_like(self.board)
		for i in range(self.chessboard_size[0]):
			for j in range(self.chessboard_size[1]):
				if self.board[i][j] != COLOR_NONE:
					continue
				for direction in MOVE_DIRECTIONS:
					for step in range(1, self.chessboard_size[0]):
						x = i + step * direction[0]
						y = j + step * direction[1]
						if x < 0 or x >= self.chessboard_size[0] or y < 0 or y >= self.chessboard_size[1]:
							break
						if self.board[x][y] == COLOR_NONE:
							break
						if self.board[x][y] == color:
							flip_count[i][j] += step - 1
							break
		return flip_count


class AI(object):
	def __init__(self, chessboard_size, color, time_out):
		self.chessboard_size = chessboard_size
		self.color = color
		self.time_out = time_out
		self.candidate_list = []
		self.chessboard = ChessBoard(chessboard_size)

	def go(self, chessboard):
		self.candidate_list.clear()
		self.chessboard.board = chessboard
		flip_count = self.chessboard.get_flip_count(self.color)
		self.candidate_list = [(i, j)
			for i in range(self.chessboard.chessboard_size[0])
			for j in range(self.chessboard.chessboard_size[1])
			if flip_count[i][j] > 0
		]
		if len(self.candidate_list) > 0:
			self.candidate_list.append(random.choice(self.candidate_list))