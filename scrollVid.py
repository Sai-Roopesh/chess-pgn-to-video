# packages
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from chessboard import display
import chess.pgn
import pygame
import cv2

# Get the frame size from the webcam
cap = cv2.VideoCapture(0)  # Change the index if you have multiple cameras
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
size = (width, height)
cap.release()

# create an output video stream
video = VideoWriter('game.avi', VideoWriter_fourcc('X', 'V', 'I', 'D'), 7, size)

# load PGN file
pgn = open('/Users/sairoopesh/projects/pgn_to_avi/pgn/Adams.pgn')

# get the first game
game = chess.pgn.read_game(pgn)

# create chess board instance
board = game.board()

# Initialize Pygame
pygame.init()

# Set up the display
DISPLAYSURF = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')

# list of positions from the game
fens = []

# extracts FEN strings from a game
for move in game.mainline_moves():
    fens.append(board.fen())
    board.push(move)

# Define the frame rate
frame_rate = 12  # Adjust as needed

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
        for _ in range(frame_rate):
            video.write(frame)

    # Handle Pygame events to prevent freezing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

# release the video stream
video.release()

# close window
pygame.quit()
