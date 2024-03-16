import time

import random

import Chessboard
import Main

if __name__ == "__main__":
	for black_player in [60, 50, 40, 30, 20, 10, 0]:
		for white_player in [60, 50, 40, 30, 20, 10, 0]:
			if black_player == white_player:
				continue
			print("Black: ", black_player, " White: ", white_player)
			for round in range(10):
				random.seed(int(time.time()))
				black = Main.AI(8, color=Chessboard.COLOR_BLACK, time_out=5, TP=black_player)
				white = Main.AI(8, color=Chessboard.COLOR_WHITE, time_out=5, TP=white_player)
				game = Chessboard.Chessboard(8)
				step = 0
				no_action = False
				while not Chessboard.is_terminal(game):
					step = step + 1
					if step % 2 == 1:
						black.go(game.board)
						actions = black.candidate_list
					else:
						white.go(game.board)
						actions = white.candidate_list
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
				cnt_black = game.board[game.board == Chessboard.COLOR_BLACK].size
				cnt_white = game.board[game.board == Chessboard.COLOR_WHITE].size
				if cnt_black < cnt_white:
					print("Black: ", black_player, " White: ", white_player, " Round: ", round, " Black wins!")
				elif cnt_black > cnt_white:
					print("Black: ", black_player, " White: ", white_player, " Round: ", round, " White wins!")
				else:
					print("Black: ", black_player, " White: ", white_player, " Round: ", round, " Draw.")
