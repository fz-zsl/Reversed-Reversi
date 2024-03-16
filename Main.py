import time

import Chessboard
import MCTS
import Minimax


MINIMAX_PARAMS = []


class AI(object):
	def __init__(self, chessboard_size, color, time_out, TP=0):
		self.time_out = time_out
		self.color = color
		self.chessboard = Chessboard.Chessboard(chessboard_size, color)
		self.candidate_list = []
		self.step = -1
		self.TP = TP

	def go(self, chessboard):
		start_time = time.time()
		self.step += 2
		self.candidate_list.clear()
		self.chessboard.set_board(chessboard, self.color)
		self.candidate_list = Chessboard.get_valid_moves(self.chessboard)
		if len(self.candidate_list) == 0:
			return self.candidate_list
		if self.step in range(self.TP):
			self.chessboard.load_params(MINIMAX_PARAMS)
			_, action = Minimax.go(self.chessboard, self.step)
		else:
			root = MCTS.MctsNode(state=self.chessboard)
			_, action = root.go(start_time=start_time, time_out=self.time_out)
		self.candidate_list.append(action)
