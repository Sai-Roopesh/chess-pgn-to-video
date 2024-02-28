# packages
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from chessboard import display
import chess.pgn
import pygame
import cv2

# Define WINDOW WIDTH and WINDOW HEIGHT in the chessboard.display module or replace them with the correct attributes
size = (1000,1000)

# create an output video stream
video = VideoWriter('game.avi', VideoWriter_fourcc('X', 'V', 'I', 'D'), 1, size)

# load PGN file
pgn = open('/Users/sairoopesh/projects/pgn_to_avi/pgn/Adams.pgn')

# get the first game
game = chess.pgn.read_game(pgn)

# create chess board instance
board = game.board()

# list of positions from the game
fens = []

# extracts FEN strings from a game
for move in game.mainline_moves():
    fens.append(board.fen())
    board.push(move)

# loop over board positions
for fen in fens:
    # delay displaying position
    for delay in range(7):
        # update position
        display.start(fen)

        # create a copy of the surface
        frame = pygame.surfarray.array3d(pygame.display.get_surface())

        # convert from (width, height, channel) to (height, width, channel)
        frame = frame.transpose([1, 0, 2])

        # convert from rgb to bgr
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # write video frame
        video.write(frame)

# release the video stream
VideoWriter.release()

# close window
