import random


class GameEngine:
    def __init__(self, board_size=15):
        self.BOARD_SIZE = board_size
        self.CELL_SIZE = 45
        self.WINDOW_SIZE = self.CELL_SIZE * self.BOARD_SIZE
        self.board = [
            [None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]

    def reset(self):
        self.board = [
            [None for _ in range(self.BOARD_SIZE)] for _ in range(self.BOARD_SIZE)
        ]

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
                    # anti-diagonal
                    if row + 4 < self.BOARD_SIZE and col - 4 >= 0:
                        if all(self.board[row + i][col - i] == color for i in range(5)):
                            return True
        return False

    def is_valid_move(self, row, col):
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


class MinimaxAgent(RandomAgent):
    def __init__(self, engine, color, depth=1):
        super().__init__(engine, color)
        self.depth = depth
        self.opponent = "black" if color == "white" else "white"

    def get_move(self):
        # Try to win immediately
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.color
            if self.engine.checkwin(self.color):
                self.engine.board[row][col] = None
                return (row, col)
            self.engine.board[row][col] = None
        # Try to block opponent's win
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.opponent
            if self.engine.checkwin(self.opponent):
                self.engine.board[row][col] = None
                return (row, col)
            self.engine.board[row][col] = None
        # Otherwise, use minimax
        _, move = self.minimax(self.depth, True)
        return move

    def make_move(self):
        move = self.get_move()
        if move:
            row, col = move
            self.engine.make_move(row, col, self.color)
            self.engine.printboard()

    def minimax(self, depth, is_maximizing):
        if (
            depth == 0
            or self.engine.checkwin(self.color)
            or self.engine.checkwin(self.opponent)
        ):
            player = self.color if is_maximizing else self.opponent
            return self.evaluate(player), None
        best_score = float("-inf") if is_maximizing else float("inf")
        best_move = None
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.color if is_maximizing else self.opponent
            score, _ = self.minimax(depth - 1, not is_maximizing)
            self.engine.board[row][col] = None
            if is_maximizing:
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
            else:
                if score < best_score:
                    best_score = score
                    best_move = (row, col)
        return best_score, best_move

    def evaluate(self, player):
        opponent = self.opponent if player == self.color else self.color
        score = 0
        score += self.count(player, 4) * 10000
        score += self.count(player, 3) * 1000
        score += self.count(player, 2) * 100
        score -= self.count(opponent, 4) * 10000
        score -= self.count(opponent, 3) * 1000
        score -= self.count(opponent, 2) * 100
        return score

    def count(self, color, length):
        count = 0
        board = self.engine.board
        size = self.engine.BOARD_SIZE
        for row in range(size):
            for col in range(size):
                # horizontal
                if col + length - 1 < size:
                    if all(board[row][col + i] == color for i in range(length)):
                        count += 1
                # vertical
                if row + length - 1 < size:
                    if all(board[row + i][col] == color for i in range(length)):
                        count += 1
                # diagonal
                if row + length - 1 < size and col + length - 1 < size:
                    if all(board[row + i][col + i] == color for i in range(length)):
                        count += 1
                # anti-diagonal
                if row + length - 1 < size and col - length + 1 >= 0:
                    if all(board[row + i][col - i] == color for i in range(length)):
                        count += 1
        return count


class AlphaBetaAgent(MinimaxAgent):
    def get_move(self):
        # Try to win immediately
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.color
            if self.engine.checkwin(self.color):
                self.engine.board[row][col] = None
                return (row, col)
            self.engine.board[row][col] = None
        # Try to block opponent's win
        for row, col in self.engine.available_moves():
            self.engine.board[row][col] = self.opponent
            if self.engine.checkwin(self.opponent):
                self.engine.board[row][col] = None
                return (row, col)
            self.engine.board[row][col] = None
        # Otherwise, use alpha-beta
        _, move = self.alphabeta(self.depth, True, float("-inf"), float("inf"))
        return move

    def make_move(self):
        move = self.get_move()
        if move:
            row, col = move
            self.engine.make_move(row, col, self.color)
            self.engine.printboard()

    def alphabeta(self, depth, is_maximizing, alpha, beta):
        if (
            depth == 0
            or self.engine.checkwin(self.color)
            or self.engine.checkwin(self.opponent)
        ):
            player = self.color if is_maximizing else self.opponent
            return self.evaluate(player), None
        best_move = None
        if is_maximizing:
            max_eval = float("-inf")
            for row, col in self.engine.available_moves():
                self.engine.board[row][col] = self.color
                eval, _ = self.alphabeta(depth - 1, False, alpha, beta)
                self.engine.board[row][col] = None
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float("inf")
            for row, col in self.engine.available_moves():
                self.engine.board[row][col] = self.opponent
                eval, _ = self.alphabeta(depth - 1, True, alpha, beta)
                self.engine.board[row][col] = None
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def evaluate(self, player):
        opponent = self.opponent if player == self.color else self.color
        score = 0
        score += self.count(player, 4) * 10000
        score += self.count(player, 3) * 1000
        score += self.count(player, 2) * 100
        score -= self.count(opponent, 4) * 10000
        score -= self.count(opponent, 3) * 1000
        score -= self.count(opponent, 2) * 100
        return score

    def count(self, color, length):
        count = 0
        board = self.engine.board
        size = self.engine.BOARD_SIZE
        for row in range(size):
            for col in range(size):
                # horizontal
                if col + length - 1 < size:
                    if all(board[row][col + i] == color for i in range(length)):
                        count += 1
                # vertical
                if row + length - 1 < size:
                    if all(board[row + i][col] == color for i in range(length)):
                        count += 1
                # diagonal
                if row + length - 1 < size and col + length - 1 < size:
                    if all(board[row + i][col + i] == color for i in range(length)):
                        count += 1
                # anti-diagonal
                if row + length - 1 < size and col - length + 1 >= 0:
                    if all(board[row + i][col - i] == color for i in range(length)):
                        count += 1
        return count
