import pygame, sys, time
from pygame.locals import *

pygame.init()

WIDTH, HEIGHT = 900, 900
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe!")

BG_COLOR = (214, 201, 227)
LINE_COLOR = (0, 0, 0)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)

board = [[None, None, None], [None, None, None], [None, None, None]]

FONT = pygame.font.Font(None, 100)
SMALL_FONT = pygame.font.Font(None, 60)

to_move = None  # Initially None until a player is chosen
winner_message = None
game_finished = False
selection_done = False  # Flag to handle player selection


def draw_custom_grid():
    for x in range(1, 3):
        # Draw vertical lines
        pygame.draw.line(SCREEN, LINE_COLOR, (x * 300, 0), (x * 300, HEIGHT), 5)
        # Draw horizontal lines
        pygame.draw.line(SCREEN, LINE_COLOR, (0, x * 300), (WIDTH, x * 300), 5)


def render_board(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                start_pos1 = (j * 300 + 50, i * 300 + 50)
                end_pos1 = (j * 300 + 250, i * 300 + 250)
                start_pos2 = (j * 300 + 50, i * 300 + 250)
                end_pos2 = (j * 300 + 250, i * 300 + 50)
                pygame.draw.line(SCREEN, X_COLOR, start_pos1, end_pos1, 10)
                pygame.draw.line(SCREEN, X_COLOR, start_pos2, end_pos2, 10)
            elif board[i][j] == 'O':
                center = (j * 300 + 150, i * 300 + 150)
                pygame.draw.circle(SCREEN, O_COLOR, center, 100, 10)


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
    # Check for a winning move for AI
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

    # Pick the first available move if no one is winning
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'
                return board
    return board


def check_win(board):
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

    # If there are no empty spaces, it's a draw
    for row in board:
        if None in row:
            return None
    return "DRAW"


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if not selection_done:
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
                winner = check_win(board)
                if winner == 'X':
                    winner_message = "X Wins!"
                    game_finished = True
                elif winner == 'DRAW':
                    winner_message = "It's a Draw!"
                    game_finished = True
                else:
                    to_move = 'O'

    if selection_done and to_move == 'O' and not game_finished:
        time.sleep(0.5)  # AI delay
        board = ai_move(board)
        winner = check_win(board)
        if winner == 'O':
            winner_message = "O Wins!"
            game_finished = True
        elif winner == 'DRAW':
            winner_message = "It's a Draw!"
            game_finished = True
        else:
            to_move = 'X'

    SCREEN.fill(BG_COLOR)
    if not selection_done:
        pygame.draw.rect(SCREEN, (0, 255, 0), (200, 400, 200, 100))  # X button
        pygame.draw.rect(SCREEN, (0, 0, 255), (500, 400, 200, 100))  # O button
        x_text = SMALL_FONT.render("X", True, (0, 0, 0))
        o_text = SMALL_FONT.render("O", True, (0, 0, 0))
        SCREEN.blit(x_text, (280, 425))
        SCREEN.blit(o_text, (580, 425))
    else:
        draw_custom_grid()
        render_board(board)

        if game_finished:
            display_message(winner_message)

            # Give the user time to see the winner before resetting
            pygame.display.update()
            time.sleep(2)  # Wait 2 seconds before resetting the game

            # Reset the game when user presses a key after a game ends
            if event.type == KEYDOWN:
                # Reset the board and relevant variables
                board = [[None, None, None], [None, None, None], [None, None, None]]
                to_move = None
                game_finished = False
                winner_message = None
                selection_done = False

    pygame.display.update()
