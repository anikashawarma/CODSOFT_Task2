import pygame
import math

pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-Tac-Toe')

clock = pygame.time.Clock()

board = ['-'] * 9

AI = 'O'
YOU = 'X'

font = pygame.font.Font(None, 75)

def draw_board():
    screen.fill(BLACK)
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, WHITE, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, WHITE, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for i in range(BOARD_ROWS * BOARD_COLS):
        if board[i] == YOU:
            row = i // BOARD_COLS
            col = i % BOARD_COLS
            pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
            pygame.draw.line(screen, BLUE, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE),
                             (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
        elif board[i] == AI:
            row = i // BOARD_COLS
            col = i % BOARD_COLS
            pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)

def check_winner(board, player):
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def is_board_full(board):
    return all(cell != '-' for cell in board)

def minimax_alpha_beta(board, depth, alpha, beta, maximizing_player):
    if check_winner(board, AI):
        return 1
    elif check_winner(board, YOU):
        return -1
    elif is_board_full(board):
        return 0
    if maximizing_player:
        max_eval = -math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = AI
                eval = minimax_alpha_beta(board, depth + 1, alpha, beta, False)
                board[i] = '-'
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(9):
            if board[i] == '-':
                board[i] = YOU
                eval = minimax_alpha_beta(board, depth + 1, alpha, beta, True)
                board[i] = '-'
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def find_best_move(board):
    best_move = -1
    best_eval = -math.inf
    for i in range(9):
        if board[i] == '-':
            board[i] = AI
            eval = minimax_alpha_beta(board, 0, -math.inf, math.inf, False)
            board[i] = '-'
            if eval > best_eval:
                best_eval = eval
                best_move = i
    return best_move

def main():
    run = True
    game_over = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouseX = event.pos[0]
                mouseY = event.pos[1]

                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE
                move = clicked_row * BOARD_COLS + clicked_col

                if board[move] == '-':
                    board[move] = YOU

                    if check_winner(board, YOU):
                        game_over = True
                    elif is_board_full(board):
                        game_over = True

                    if not game_over:
                        ai_move = find_best_move(board)
                        board[ai_move] = AI

                        if check_winner(board, AI):
                            game_over = True
                        elif is_board_full(board):
                            game_over = True

        draw_board()
        draw_figures()
        pygame.display.update()

        if game_over:
            pygame.time.wait(3000)
            run = False

    pygame.quit()

if __name__ == "__main__":
    main()
