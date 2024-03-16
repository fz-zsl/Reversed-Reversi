import time

import numpy as np

import Chessboard
import Main

if __name__ == "__main__":
	np.random.seed(int(time.time()))
	swap_agent = np.random.choice([True, False])
	if swap_agent:
		print("Black: VAI, White: Random")
		vai = Main.AI(8, color=Chessboard.COLOR_BLACK, time_out=5, TP=70)
		# ra = RandomAgent.AI(8, color=Chessboard.COLOR_WHITE, time_out=5)
		mcts = Main.AI(8, color=Chessboard.COLOR_WHITE, time_out=5, TP=40)
	else:
		print("Black: Random, White: VAI")
		vai = Main.AI(8, color=Chessboard.COLOR_WHITE, time_out=5, TP=70)
		# ra = RandomAgent.AI(8, color=Chessboard.COLOR_BLACK, time_out=5)
		mcts = Main.AI(8, color=Chessboard.COLOR_BLACK, time_out=5, TP=40)
	game = Chessboard.Chessboard(8)
	step = 0
	no_action = False
	while not Chessboard.is_terminal(game):
		step = step + 1
		if step % 2 == swap_agent:
			vai.go(game.board)
			actions = vai.candidate_list
		else:
			mcts.go(game.board)
			actions = mcts.candidate_list
		if not actions:
			if no_action:
				break
			game = Chessboard.flip_chess(game, (-1, -1))
			no_action = True
			continue
		else:
			no_action = False
		action = actions[-1]
		game = Chessboard.flip_chess(game, action)
	if swap_agent:
		print("Black: VAI, White: Random")
	else:
		print("Black: Random, White: VAI")
	cnt_black = game.board[game.board == Chessboard.COLOR_BLACK].size
	cnt_white = game.board[game.board == Chessboard.COLOR_WHITE].size
	if cnt_black < cnt_white:
		print("Black wins!")
	elif cnt_black > cnt_white:
		print("White wins!")
	else:
		print("Draw!")
