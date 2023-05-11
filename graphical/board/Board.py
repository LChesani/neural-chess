import chess
import pygame
from graphical.config import *
import os



class Board:
    def __init__(self, board):
        self.board = board

    

def drawPieces(b, display, x, y, square):
    piece = b.board.piece_at(square)

    if piece is not None:
        piece_name = chess.piece_name(piece.piece_type).lower()
        color = 'white' if piece.color == chess.WHITE else 'black'
        filename = f"{color}_{piece_name}.png"

        display.blit(pygame.transform.scale(pygame.image.load(os.path.join('graphical/pieces', filename)), (SIZE, SIZE)), (x, y))

def draw_board(b, screen):
    for row in range(8):
        for col in range(8):
            x = col * SIZE
            y = row * SIZE

            if (row + col) % 2 == 0:
                color = (255, 255, 255)
            else:
                color = (100, 100, 100)

            pygame.draw.rect(screen, color, pygame.Rect(x, y, SIZE, SIZE))

            square = chess.square(col, 7 - row)
            drawPieces(b, screen, x, y, square)

    pygame.display.flip()

    

