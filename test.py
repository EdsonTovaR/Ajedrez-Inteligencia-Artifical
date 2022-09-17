import chess
import funciones as f

'''
board = chess.Board()
f.juego(board,"minimax_p",prueba=True)
'''

'''
board = chess.Board()
f.juego(board, "ab_minimax_p", prueba=True)
'''
board = chess.Board()
f.juego(board, "mcts", prueba=True)
