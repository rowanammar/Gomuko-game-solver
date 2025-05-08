import random
import math
import time


class GameEngine:
    def __init__(self, board_size=15):
        self.BOARD_SIZE = board_size
        self.CELL_SIZE = 45
        self.WINDOW_SIZE = self.CELL_SIZE * self.BOARD_SIZE
        self.board = [
            [None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]
        self.current_player = "black"
        self.winner = None
        self.game_over = False

    def reset(self):
        self.board = [
            [None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]
        self.current_player = "black"
        self.winner = None
        self.game_over = False

    def printboard(self):
        print("  " + " ".join(f"{i:2}" for i in range(self.BOARD_SIZE)))
        for row in range(self.BOARD_SIZE):
            row_str = f"{row:2} "
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == "black":
                    row_str += "B "
                elif self.board[row][col] == "white":
                    row_str += "W "
                else:
                    row_str += ". "
            print(row_str)

    def checkwin(self, color):
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if self.board[row][col] == color:
                    # horizontal
                    if col + 4 < self.BOARD_SIZE:
                        if all(self.board[row][col + i] == color for i in range(5)):
                            return True
                    # vertical
                    if row + 4 < self.BOARD_SIZE:
                        if all(self.board[row + i][col] == color for i in range(5)):
                            return True
                    # diagonal
                    if row + 4 < self.BOARD_SIZE and col + 4 < self.BOARD_SIZE:
                        if all(self.board[row + i][col + i] == color for i in range(5)):
                            return True
                    # diagonal bel3aks
                    if row + 4 < self.BOARD_SIZE and col - 4 >= 0:
                        if all(self.board[row + i][col - i] == color for i in range(5)):
                            return True
        return False

    def is_valid_move(self, row, col):  # boundries and empty
        return (
            0 <= row < self.BOARD_SIZE
            and 0 <= col < self.BOARD_SIZE
            and self.board[row][col] is None
        )

    def make_move(self, row, col, color):
        if self.is_valid_move(row, col):
            self.board[row][col] = color
            return True
        return False

    def available_moves(self):
        return [
            (row, col)
            for row in range(self.BOARD_SIZE)
            for col in range(self.BOARD_SIZE)
            if self.board[row][col] is None
        ]

    def play_move(self, row, col):
        if self.game_over or not self.is_valid_move(row, col):
            return False
        self.make_move(row, col, self.current_player)
        if self.checkwin(self.current_player):
            self.winner = self.current_player
            self.game_over = True
        elif not self.available_moves():
            self.game_over = True
        else:
            self.current_player = "white" if self.current_player == "black" else "black"
        return True

    def get_current_player(self):
        return self.current_player

    def is_game_over(self):
        return self.game_over

    def get_winner(self):
        return self.winner


class RandomAgent:
    def __init__(self, engine, color):
        self.engine = engine
        self.color = color

    def get_move(self):
        moves = self.engine.available_moves()
        if moves:
            return random.choice(moves)
        return None

    def make_move(self):
        move = self.get_move()
        if move:
            row, col = move
            self.engine.make_move(row, col, self.color)
            self.engine.printboard()


def main_menu():
    print("\n===== Gomoku Game =====")
    print("1. Human vs Random AI")
    print("2. Human vs AlphaBeta AI")
    print("3. Human vs Minimax AI")
    print("4. Minimax AI vs AlphaBeta AI")
    print("5. Random AI vs AlphaBeta AI")
    print("6. AI vs AI (Minimax vs AlphaBeta)")
    print("7. Exit")
    return input("Enter your choice: ")


def human_vs_random():
    engine = GameEngine()
    ai = RandomAgent(engine, "white")
    while not engine.is_game_over():
        engine.printboard()
        if engine.get_current_player() == "black":
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
            if not engine.play_move(row, col):
                print("Invalid move, try again.")
                continue
        else:
            print("AI (white) is thinking...")
            move = ai.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        if engine.is_game_over():
            engine.printboard()
            winner = engine.get_winner()
            if winner:
                print(f"{winner.capitalize()} wins!")
            else:
                print("Draw!")
            break


def human_vs_alphabeta():
    engine = GameEngine()
    ai = AlphaBetaAgent(engine, "white")
    while not engine.is_game_over():
        engine.printboard()
        if engine.get_current_player() == "black":
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
            if not engine.play_move(row, col):
                print("Invalid move, try again.")
                continue
        else:
            print("AI (white) is thinking...")
            move = ai.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        if engine.is_game_over():
            engine.printboard()
            winner = engine.get_winner()
            if winner:
                print(f"{winner.capitalize()} wins!")
            else:
                print("Draw!")
            break


def random_vs_alphabeta():
    engine = GameEngine()
    black_agent = RandomAgent(engine, "black")
    white_agent = AlphaBetaAgent(engine, "white")
    move_num = 1
    while not engine.is_game_over():
        print(f"Move {move_num}: {engine.get_current_player().capitalize()}'s turn")
        if engine.get_current_player() == "black":
            move = black_agent.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        else:
            move = white_agent.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        engine.printboard()
        move_num += 1
    winner = engine.get_winner()
    if winner:
        print(f"{winner.capitalize()} wins!")
    else:
        print("Draw!")


# Alpha Beta constants
EMPTY = "."
HUMAN = "X"
AI = "O"
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
                        0 <= x + i * dx < BOARD_SIZE
                        and 0 <= y + i * dy < BOARD_SIZE
                        and self.board[x + i * dx][y + i * dy] == player
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
            "five": (f"{player}" * 5, 100000),
            "open_four": (f".{player*4}.", 10000),
            "blocked_four": (f"{player*4}.", 1000),
            "open_three": (f".{player*3}.", 500),
            "blocked_three": (f"{player*3}.", 100),
            "open_two": (f".{player*2}.", 50),
        }

        score = 0
        lines = []

        # Get all rows, columns, diagonals
        for row in self.board:
            lines.append("".join(row))
        for col in zip(*self.board):
            lines.append("".join(col))
        for d in range(-BOARD_SIZE + 1, BOARD_SIZE):
            lines.append(
                "".join(
                    self.board[i][i - d]
                    for i in range(max(d, 0), min(BOARD_SIZE + d, BOARD_SIZE))
                    if 0 <= i - d < BOARD_SIZE
                )
            )
            lines.append(
                "".join(
                    self.board[i][BOARD_SIZE - 1 - i + d]
                    for i in range(max(-d, 0), min(BOARD_SIZE - d, BOARD_SIZE))
                    if 0 <= BOARD_SIZE - 1 - i + d < BOARD_SIZE
                )
            )

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


class AlphaBetaAgent:
    def __init__(self, engine, color, max_depth=2):
        self.engine = engine
        self.color = color  # 'black' or 'white'
        self.max_depth = max_depth

    def get_move(self):
        # Translate engine board to Gomoku board
        gomoku_board = Gomoku()
        for row in range(self.engine.BOARD_SIZE):
            for col in range(self.engine.BOARD_SIZE):
                val = self.engine.board[row][col]
                if val == "black":
                    gomoku_board.board[row][col] = HUMAN
                elif val == "white":
                    gomoku_board.board[row][col] = AI
                else:
                    gomoku_board.board[row][col] = EMPTY
        maximizing = self.color == "white"
        _, move = alpha_beta(
            gomoku_board, self.max_depth, -math.inf, math.inf, maximizing
        )
        return move

    def make_move(self):
        move = self.get_move()
        if move:
            row, col = move
            self.engine.make_move(row, col, self.color)
            self.engine.printboard()


def ai_vs_ai_minmax_alphabeta():
    engine = GameEngine()
    black_agent = MinimaxAgent(engine, "black")
    white_agent = AlphaBetaAgent(engine, "white")
    move_num = 1

    # Make first move random in the center region of the board
    center_range = range(5, engine.BOARD_SIZE - 5)
    random_row = random.choice(center_range)
    random_col = random.choice(center_range)
    print(f"Starting with a random move at position ({random_row}, {random_col})")
    engine.play_move(random_row, random_col)
    engine.printboard()
    move_num += 1

    while not engine.is_game_over():
        print(f"Move {move_num}: {engine.get_current_player().capitalize()}'s turn")
        if engine.get_current_player() == "black":
            move = black_agent.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        else:
            move = white_agent.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        engine.printboard()
        move_num += 1
        time.sleep(0.2)
    winner = engine.get_winner()
    if winner:
        print(f"{winner.capitalize()} wins!")
    else:
        print("Draw!")


class MinimaxAgent:
    def __init__(self, engine, color, depth=1):
        self.engine = engine
        self.color = color
        self.opponent = "black" if color == "white" else "white"
        self.depth = depth

    def get_move(self):
        # Check for immediate winning move
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.color
            if self.engine.checkwin(self.color):
                self.engine.board[row][col] = None
                return (row, col)
            self.engine.board[row][col] = None

        # Check for blocking opponent's winning move
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.opponent
            if self.engine.checkwin(self.opponent):
                self.engine.board[row][col] = None
                return (row, col)
            self.engine.board[row][col] = None

        # Count total pieces to handle early game moves
        total_pieces = sum(
            1
            for row in range(self.engine.BOARD_SIZE)
            for col in range(self.engine.BOARD_SIZE)
            if self.engine.board[row][col] is not None
        )

        # Special case for when there's only one piece on the board
        if total_pieces == 1:
            for r in range(self.engine.BOARD_SIZE):
                for c in range(self.engine.BOARD_SIZE):
                    if self.engine.board[r][c] == self.opponent:
                        opp_row, opp_col = r, c
                        break
                else:
                    continue
                break

            # Try to place near opponent
            neighbors = [
                (opp_row - 1, opp_col),
                (opp_row + 1, opp_col),
                (opp_row, opp_col - 1),
                (opp_row, opp_col + 1),
                (opp_row - 1, opp_col - 1),
                (opp_row - 1, opp_col + 1),
                (opp_row + 1, opp_col - 1),
                (opp_row + 1, opp_col + 1),
            ]

            for row, col in neighbors:
                if (
                    0 <= row < self.engine.BOARD_SIZE
                    and 0 <= col < self.engine.BOARD_SIZE
                    and self.engine.board[row][col] is None
                ):
                    return (row, col)

        # Special case for early game (3 pieces)
        elif total_pieces == 3:
            for r in range(self.engine.BOARD_SIZE):
                for c in range(self.engine.BOARD_SIZE):
                    if self.engine.board[r][c] == self.color:
                        neighbors = [
                            (r + 1, c),
                            (r - 1, c),
                            (r, c + 1),
                            (r, c - 1),
                        ]
                        for row, col in neighbors:
                            if (
                                0 <= row < self.engine.BOARD_SIZE
                                and 0 <= col < self.engine.BOARD_SIZE
                                and self.engine.board[row][col] is None
                            ):
                                return (row, col)

        # Use minimax for more complex positions
        else:
            score, move = self.minimax(self.depth, True)
        return move

        # Fallback to random move if no good move found
        return random.choice(self.engine.available_moves())

    def minimax(self, depth, is_maximizing):
        # Terminal conditions
        if depth == 0:
            return self.evaluate(self.engine.board, self.color), None

        for color in [self.color, self.opponent]:
            for row in range(self.engine.BOARD_SIZE):
                for col in range(self.engine.BOARD_SIZE):
                    if self.engine.board[row][col] == color:
                        if self.engine.checkwin(color):
                            if color == self.color:
                                return 1000000, None
                            else:
                                return -1000000, None

        best_score = -float("inf") if is_maximizing else float("inf")
        best_move = None

        for row, col in self.engine.available_moves():
            # Make the move
            self.engine.board[row][col] = self.color if is_maximizing else self.opponent

            # Recursive call
            score, _ = self.minimax(depth - 1, not is_maximizing)

            # Undo the move
            self.engine.board[row][col] = None

            # Update best score
            if is_maximizing:
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
            else:
                if score < best_score:
                    best_score = score
                    best_move = (row, col)

        return best_score, best_move

    def evaluate(self, board, player):
        score = 0
        score += self.count(board, self.color, 4) * 10000
        score += self.count(board, self.color, 3) * 1000
        score += self.count(board, self.color, 2) * 100
        score -= self.count(board, self.opponent, 4) * 10000
        score -= self.count(board, self.opponent, 3) * 1000
        score -= self.count(board, self.opponent, 2) * 100
        return score

    def count(self, board, color, length):
        count = 0
        for row in range(self.engine.BOARD_SIZE):
            for col in range(self.engine.BOARD_SIZE):
                # Horizontal
                if col + length - 1 < self.engine.BOARD_SIZE:
                    if all(board[row][col + i] == color for i in range(length)):
                        count += 1
                # Vertical
                if row + length - 1 < self.engine.BOARD_SIZE:
                    if all(board[row + i][col] == color for i in range(length)):
                        count += 1
                # Diagonal down-right
                if (
                    row + length - 1 < self.engine.BOARD_SIZE
                    and col + length - 1 < self.engine.BOARD_SIZE
                ):
                    if all(board[row + i][col + i] == color for i in range(length)):
                        count += 1
                # Diagonal down-left
                if row + length - 1 < self.engine.BOARD_SIZE and col - length + 1 >= 0:
                    if all(board[row + i][col - i] == color for i in range(length)):
                        count += 1
        return count

    def make_move(self):
        move = self.get_move()
        if move:
            row, col = move
            self.engine.make_move(row, col, self.color)
            self.engine.printboard()


def human_vs_minmax():
    engine = GameEngine()
    ai = MinimaxAgent(engine, "white")
    while not engine.is_game_over():
        engine.printboard()
        if engine.get_current_player() == "black":
            try:
                row = int(input("Enter row: "))
                col = int(input("Enter col: "))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue
            if not engine.play_move(row, col):
                print("Invalid move, try again.")
                continue
        else:
            print("AI (white) is thinking...")
            move = ai.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        if engine.is_game_over():
            engine.printboard()
            winner = engine.get_winner()
            if winner:
                print(f"{winner.capitalize()} wins!")
            else:
                print("Draw!")
            break


def minmax_vs_alphabeta():
    engine = GameEngine()
    black_agent = MinimaxAgent(engine, "black")
    white_agent = AlphaBetaAgent(engine, "white")
    move_num = 1
    while not engine.is_game_over():
        print(f"Move {move_num}: {engine.get_current_player().capitalize()}'s turn")
        if engine.get_current_player() == "black":
            move = black_agent.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        else:
            move = white_agent.get_move()
            if move:
                row, col = move
                engine.play_move(row, col)
        engine.printboard()
        move_num += 1
    winner = engine.get_winner()
    if winner:
        print(f"{winner.capitalize()} wins!")
    else:
        print("Draw!")


if __name__ == "__main__":
    while True:
        choice = main_menu()
        if choice == "1":
            human_vs_random()
        elif choice == "2":
            human_vs_alphabeta()
        elif choice == "3":
            human_vs_minmax()
        elif choice == "4":
            minmax_vs_alphabeta()
        elif choice == "5":
            random_vs_alphabeta()
        elif choice == "6":
            ai_vs_ai_minmax_alphabeta()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
