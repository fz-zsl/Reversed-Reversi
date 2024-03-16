import numpy as np

import Chessboard

INF = np.inf


def max_value(state, alpha, beta, depth_limit, step):
	if Chessboard.is_terminal(state) or depth_limit == 0:
		return Chessboard.eval_state(state, state.to_move, step), None
	v, move = -INF, None
	for a in Chessboard.get_valid_moves(state):
		v2, _ = min_value(Chessboard.flip_chess(state, a), alpha, beta, depth_limit - 1, step)
		if v2 > v:
			v, move = v2, a
			if v >= beta:
				return v, None
		alpha = max(alpha, v)
	if move is None:
		return min_value(Chessboard.flip_chess(state, (-1, -1)), alpha, beta, depth_limit - 1, step)
	return v, move


def min_value(state, alpha, beta, depth_limit, step):
	if Chessboard.is_terminal(state) or depth_limit == 0:
		return Chessboard.eval_state(state, state.to_move, step), None
	v, move = INF, None
	for a in Chessboard.get_valid_moves(state):
		v2, _ = max_value(Chessboard.flip_chess(state, a), alpha, beta, depth_limit - 1, step)
		if v2 < v:
			v, move = v2, a
			if v <= alpha:
				return v, None
		beta = min(beta, v)
	if move is None:
		return max_value(Chessboard.flip_chess(state, (-1, -1)), alpha, beta, depth_limit - 1, step)
	return v, move


def go(state, step):
	score, action = max_value(state, -INF, INF, 4, step)
	return score, action
