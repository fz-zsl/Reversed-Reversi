import time
from copy import deepcopy

import numpy as np
import random

import Chessboard

INF = np.inf


def uct(node, C=1.414):
	return INF if node.N == 0 else node.U / node.N + C * np.sqrt(np.log(node.parent.N) / node.N)


class MctsNode(object):
	def __init__(self, parent=None, state=None, U=0, N=0):
		self.parent = parent
		self.children = {}
		self.state = state
		self.U = U
		self.N = N

	def select(self):
		if self.children:
			return max(self.children.keys(), key=uct)
		else:
			return self

	def expand(self):
		if not self.children and not Chessboard.is_terminal(self.state):
			self.children = {
				MctsNode(parent=self, state=Chessboard.flip_chess(self.state, action)): action
				for action in Chessboard.get_valid_moves(self.state)
			}
		return self.select()

	def simulate(self):
		player = self.state.to_move
		_state = deepcopy(self.state)
		no_action = False
		while not Chessboard.is_terminal(_state):
			actions = Chessboard.get_valid_moves(_state)
			if not actions:
				if no_action:
					break
				_state = Chessboard.flip_chess(_state, (-1, -1))
				no_action = True
				continue
			else:
				no_action = False
			action = random.choice(actions)
			_state = Chessboard.flip_chess(_state, action)
		_util = Chessboard.utility(_state, player)
		return -_util

	def back_prop(self, value):
		self.N += 1
		if value > 0:
			self.U += value
		if self.parent:
			self.parent.back_prop(-value)

	def go(self, start_time, time_out):
		while True:
			leaf = self.select()
			child = leaf.expand()
			res = child.simulate()
			child.back_prop(res)
			if time.time() - start_time > time_out * 0.95:
				break
		node, action = max(self.children.items(), key=lambda x: x[0].N)
		return node.N, action
