import math

EMPTY = '.'
HUMAN = 'X'
AI = 'O'
BOARD_SIZE = 15
WIN_LENGTH = 5
MAX_DEPTH = 2

class Gomoku:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def print_board(self):
        print("  " + " ".join(f"{i:2}" for i in range(BOARD_SIZE)))
        for i, row in enumerate(self.board):
            print(f"{i:2} " + "  ".join(row))

    def is_valid_move(self, x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == EMPTY

    def make_move(self, x, y, player):
        if self.is_valid_move(x, y):
            self.board[x][y] = player
            return True
        return False

    def undo_move(self, x, y):
        self.board[x][y] = EMPTY

    def check_win(self, player):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != player:
                    continue
                for dx, dy in directions:
                    if all(
                        0 <= x + i*dx < BOARD_SIZE and
                        0 <= y + i*dy < BOARD_SIZE and
                        self.board[x + i*dx][y + i*dy] == player
                        for i in range(WIN_LENGTH)
                    ):
                        return True
        return False

    def get_nearby_moves(self, radius=2):
        nearby = set()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != EMPTY:
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                                if self.board[nx][ny] == EMPTY:
                                    nearby.add((nx, ny))
        return list(nearby) if nearby else [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

    def evaluate(self):
        return self.evaluate_player(AI) - self.evaluate_player(HUMAN)

    def evaluate_player(self, player):
        patterns = {
            'five': (f'{player}'*5, 100000),
            'open_four': (f'.{player*4}.', 10000),
            'blocked_four': (f'{player*4}.', 1000),
            'open_three': (f'.{player*3}.', 500),
            'blocked_three': (f'{player*3}.', 100),
            'open_two': (f'.{player*2}.', 50),
        }

        score = 0
        lines = []

        # Get all rows, columns, diagonals
        for row in self.board:
            lines.append(''.join(row))
        for col in zip(*self.board):
            lines.append(''.join(col))
        for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
            lines.append(''.join(self.board[i][i - d] for i in range(max(d, 0), min(BOARD_SIZE + d, BOARD_SIZE)) if 0 <= i - d < BOARD_SIZE))
            lines.append(''.join(self.board[i][BOARD_SIZE - 1 - i + d] for i in range(max(-d, 0), min(BOARD_SIZE - d, BOARD_SIZE)) if 0 <= BOARD_SIZE - 1 - i + d < BOARD_SIZE))

        for line in lines:
            for pat, val in patterns.values():
                score += line.count(pat) * val

        return score
def alpha_beta(board, depth, alpha, beta, maximizing):
    score = board.evaluate()
    if abs(score) >= 100000 or depth == 0:
        return score, None

    best_move = None
    moves = board.get_nearby_moves()

    if maximizing:
        max_eval = -math.inf
        for move in moves:
            board.make_move(*move, AI)
            eval, _ = alpha_beta(board, depth - 1, alpha, beta, False)
            board.undo_move(*move)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in moves:
            board.make_move(*move, HUMAN)
            eval, _ = alpha_beta(board, depth - 1, alpha, beta, True)
            board.undo_move(*move)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move
def play_game():
    game = Gomoku()
    game.print_board()

    while True:
        try:
            x, y = map(int, input("Enter your move (row col): ").split())
        except:
            print("Invalid input. Use two numbers (e.g., 7 7).")
            continue

        if not game.make_move(x, y, HUMAN):
            print("Invalid move. Try again.")
            continue

        game.print_board()

        if game.check_win(HUMAN):
            print("You win!")
            break

        print("AI is thinking...")
        _, move = alpha_beta(game, MAX_DEPTH, -math.inf, math.inf, True)
        if move:
            game.make_move(*move, AI)
            print(f"AI played: {move[0]}, {move[1]}")
            game.print_board()
            if game.check_win(AI):
                print("AI wins!")
                break
        else:
            print("No valid moves left. It's a draw!")
            break

if __name__ == "__main__":
    play_game()
