# packages
from cv2 import VideoWriter
from cv2 import VideoWriter_fourcc
from chessboard import display
import chess.pgn
import pygame
import cv2

# Define WINDOW WIDTH and WINDOW HEIGHT in the chessboard.display module or replace them with the correct attributes
size = (1000, 1000)

# create an output video stream
video = VideoWriter('game.avi', VideoWriter_fourcc('X', 'V', 'I', 'D'), 60, size)  # Increased frame rate to 30

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

# Initialize pygame
pygame.init()

# Load additional resources
font = pygame.font.Font(None, 36)  # Set font for text overlay

# loop over board positions
# loop over board positions
for fen in fens:
    # delay displaying position
    for delay in range(3):  # Reduced delay for faster display
        # update position
        display.start(fen)

        # Add dynamic text overlay
        text = font.render("Exciting Chess Game", True, (255, 255, 255))
        text_rect = text.get_rect(center=(size[0] // 2, size[1] // 10))  # Adjusted vertical position
        pygame.display.get_surface().blit(text, text_rect)

        # Add some visual effects or animations here
        # Example: Add a rotating effect to the board
        pygame.display.flip()
        pygame.time.wait(100)  # Wait for 100 milliseconds for visual effect

        # create a copy of the surface
        frame = pygame.surfarray.array3d(pygame.display.get_surface())

        # convert from (width, height, channel) to (height, width, channel)
        frame = frame.transpose([1, 0, 2])

        # convert from rgb to bgr
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # write video frame
        video.write(frame)

video.release()
cv2.destroyAllWindows()
print("Number of frames written:", len(fens))