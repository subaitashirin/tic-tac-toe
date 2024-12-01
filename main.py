import pygame, sys, time
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 900, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BOARD = pygame.image.load("assets/Board.png")
X_IMG = pygame.image.load("assets/X.png")
O_IMG = pygame.image.load("assets/O.png")

BG_COLOR = (214, 201, 227)

board = [[None, None, None], [None, None, None], [None, None, None]]
graphical_board = [[[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]],
                   [[None, None], [None, None], [None, None]]]

FONT = pygame.font.Font(None, 100)
SMALL_FONT = pygame.font.Font(None, 60)

to_move = None  # Initially None until a player is chosen
winner_message = None
game_finished = False
reset_timer = 0
selection_done = False  # Flag to handle player selection

def render_board(board, ximg, oimg):
    global graphical_board
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                graphical_board[i][j][0] = ximg
                graphical_board[i][j][1] = ximg.get_rect(center=(j * 300 + 150, i * 300 + 150))
            elif board[i][j] == 'O':
                graphical_board[i][j][0] = oimg
                graphical_board[i][j][1] = oimg.get_rect(center=(j * 300 + 150, i * 300 + 150))

    for i in range(3):
        for j in range(3):
            if graphical_board[i][j][0] is not None:
                SCREEN.blit(graphical_board[i][j][0], graphical_board[i][j][1])

def display_message(message, y_offset=0):
    text = FONT.render(message, True, (255, 0, 0))  # Red color
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    SCREEN.blit(text, text_rect)

def add_X(board, to_move):
    current_pos = pygame.mouse.get_pos()
    col, row = current_pos[0] // 300, current_pos[1] // 300
    if board[row][col] is None:
        board[row][col] = to_move
    return board

def ai_move(board):
    # Check for a winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'
                if check_win(board) == 'O':
                    return board
                board[i][j] = None

    # Check to block player's winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'X'
                if check_win(board) == 'X':
                    board[i][j] = 'O'
                    return board
                board[i][j] = None

    # Pick the first available move
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'
                return board
    return board

def check_win(board):
    # Check rows, columns, diagonals
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]

    # Check for a draw
    for row in board:
        if None in row:
            return None
    return "DRAW"

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if not selection_done:
            # Handle player selection
            if event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 200 <= mouse_x <= 400 and 400 <= mouse_y <= 500:
                    to_move = 'X'
                    selection_done = True
                elif 500 <= mouse_x <= 700 and 400 <= mouse_y <= 500:
                    to_move = 'O'
                    selection_done = True
        else:
            if event.type == MOUSEBUTTONDOWN and to_move == 'X' and not game_finished:
                board = add_X(board, 'X')
                to_move = 'O'

    if selection_done and to_move == 'O' and not game_finished:
        time.sleep(0.5)  # Wait before AI moves
        board = ai_move(board)
        to_move = 'X'

    winner = check_win(board)
    if winner is not None and not game_finished:
        game_finished = True
        if winner == "DRAW":
            winner_message = "It's a Draw!"
        else:
            winner_message = f"{winner} Wins!"
        reset_timer = time.time()  # Start reset timer

    SCREEN.fill(BG_COLOR)

    if not selection_done:
        display_message("Who Goes First?")
        pygame.draw.rect(SCREEN, (0, 255, 0), (200, 400, 200, 100))  # X button
        pygame.draw.rect(SCREEN, (0, 0, 255), (500, 400, 200, 100))  # O button
        x_text = SMALL_FONT.render("X", True, (0, 0, 0))
        o_text = SMALL_FONT.render("O", True, (0, 0, 0))
        SCREEN.blit(x_text, (280, 425))
        SCREEN.blit(o_text, (580, 425))
    else:
        SCREEN.blit(BOARD, (64, 64))
        render_board(board, X_IMG, O_IMG)

        if game_finished:
            display_message(winner_message)

            # Reset the board after 2 seconds and ask who goes first
            if time.time() - reset_timer > 2:
                # Reset the game state for a new round
                board = [[None, None, None], [None, None, None], [None, None, None]]
                graphical_board = [[[None, None], [None, None], [None, None]],
                                   [[None, None], [None, None], [None, None]],
                                   [[None, None], [None, None], [None, None]]]
                to_move = None  # Reset the player choice
                game_finished = False
                winner_message = None
                selection_done = False  # Re-enable player selection

    pygame.display.update()
