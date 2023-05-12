from __future__ import print_function
import sys
sys.path.append('..')
from Game import Game

import numpy as np
import chess

square_idx = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7
        }

def square_to_index(square):
    letter = chess.square_name(square)
    return 8-int(letter[1]), square_idx[letter[0]]


def to_np(board):
  board3d = np.zeros((19, 8, 8), dtype=np.int8)

  
  ######## bitboard as pecas
  for piece in chess.PIECE_TYPES:
      for square in board.pieces(piece, chess.WHITE):
          idx = np.unravel_index(square, (8, 8))
          board3d[piece-1][7-idx[0]][idx[1]] = 1
      for square in board.pieces(piece, chess.BLACK):
          idx = np.unravel_index(square, (8, 8))
          board3d[piece+5][7-idx[0]][idx[1]] = 1

  ################## casas controladas / tensao / movimentos do rei
  aux = board.turn
  board.turn = chess.WHITE
  for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[12][i][j] += 1
      if board.piece_type_at(move.from_square) == chess.KING:
        board3d[15][i][j] = 1

  board.turn = chess.BLACK

  for move in board.legal_moves:
      i, j = square_to_index(move.to_square)
      board3d[13][i][j] += 1
      if board.piece_type_at(move.from_square) == chess.KING:
        board3d[16][i][j] = 1
        
  board.turn = aux
  
  ############## turno
  
  board3d[14].fill(board.turn)
  
  ############ pressao no centro

  center = [3, 4]
  for i in center:
    for j in center:
      board3d[17][i][j] = board3d[12][i][j]
      board3d[18][i][j] = board3d[13][i][j]

  return board3d

def from_move(move):
  return move.from_square*64+move.to_square

def to_move(action):
  to_sq = action % 64
  from_sq = int(action / 64)
  return chess.Move(from_sq, to_sq)

def who(turn):
  return 1 if turn else -1

def mirror_move(move):
  return chess.Move(chess.square_mirror(move.from_square), chess.square_mirror(move.to_square))

CHECKMATE =1
STALEMATE= 2
INSUFFICIENT_MATERIAL= 3
SEVENTYFIVE_MOVES= 4
FIVEFOLD_REPETITION= 5
FIFTY_MOVES= 6
THREEFOLD_REPETITION= 7

class ChessGame(Game):

    def __init__(self):
        pass

    def getInitBoard(self):
        # return initial board (numpy board)
        return chess.Board()

    def getBoardSize(self):
        # (a,b) tuple
        # 6 piece type
        return (19, 8, 8)

    def toArray(self, board):
        return to_np(board)

    def getActionSize(self):
        # return number of actions
        return 64*64
        # return self.n*self.n*16+1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        assert(who(board.turn) == player)
        move = to_move(action)
        if not board.turn:
          # assume the move comes from the canonical board...
          move = mirror_move(move)
        if move not in board.legal_moves:
          # could be a pawn promotion, which has an extra letter in UCI format
          move = chess.Move.from_uci(move.uci()+'q') # assume promotion to queen
          if move not in board.legal_moves:
            assert False, "%s not in %s" % (str(move), str(list(board.legal_moves)))
        board = board.copy()
        board.push(move)
        return (board, who(board.turn))

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        assert(who(board.turn) == player)
        acts = [0]*self.getActionSize()
        for move in board.legal_moves:
          acts[from_move(move)] = 1
        return np.array(acts)

    def getGameEnded(self, board, player):
      result = board.result()
      if result == "1/2-1/2":
          return 1e-4
      elif result == "1-0":
          return 1 if player == chess.WHITE else -1
      elif result == "0-1":
          return -1 if player == chess.WHITE else 1
      else:
          return 0


    def getCanonicalForm(self, board, player):
        # return state if player==1, else return -state if player==-1
        assert(who(board.turn) == player)
        if board.turn:
          return board
        else:
          return board.mirror()

    def getSymmetries(self, board, pi):
        # mirror, rotational
        return [(board,pi)]

    def stringRepresentation(self, board):
        return board.fen()

    @staticmethod
    def display(board):
        print(board)
