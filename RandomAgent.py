import time
import random

import Chessboard

random.seed(int(time.time()))


class AI(object):
	def __init__(self, chessboard_size, color, time_out):
		self.chessboard_size = chessboard_size
		self.color = color
		self.time_out = time_out
		self.candidate_list = []
		self.chessboard = Chessboard.Chessboard(chessboard_size, cur_player=color)

	def go(self, chessboard):
		self.candidate_list.clear()
		self.chessboard.board = chessboard
		self.candidate_list = Chessboard.get_valid_moves(self.chessboard)
		if len(self.candidate_list) > 0:
			self.candidate_list.append(random.choice(self.candidate_list))
