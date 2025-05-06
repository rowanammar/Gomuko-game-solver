import tkinter as tk
from tkinter import messagebox
import random
import copy # 3shan lama el ai bygrb moves fel actual board eldonya btbooz



BOARD_SIZE = 15
CELL_SIZE = 45  # pixels between grid lines
WINDOW_SIZE = CELL_SIZE * BOARD_SIZE


window = tk.Tk()
window.title("Gomoku Game")
canvas = tk.Canvas(window, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="#997950")  
canvas.pack()

# hn3ml el board 2d list 3shan n-save el moves
board = []
for row in range(BOARD_SIZE):
    row_list = []
    for col in range(BOARD_SIZE):
        row_list.append(None)
    board.append(row_list)

# hnrsem ellines
for i in range(BOARD_SIZE):
    # tool
    x = i * CELL_SIZE + CELL_SIZE // 2
    canvas.create_line(x, CELL_SIZE // 2, x, WINDOW_SIZE - CELL_SIZE // 2)
    # 3ard
    y = i * CELL_SIZE + CELL_SIZE // 2
    canvas.create_line(CELL_SIZE // 2, y, WINDOW_SIZE - CELL_SIZE // 2, y)


turn = "black"

def draw_piece(row, col, color):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    radius = 17 #hagm el piece
    canvas.create_oval(center_x - radius, center_y - radius,
                       center_x + radius, center_y + radius,
                       fill=color)


def handle_click(event):
    global turn
    # bngyb makan eldosa
    col = round((event.x - CELL_SIZE // 2) / CELL_SIZE)
    row = round((event.y - CELL_SIZE // 2) / CELL_SIZE)

    # maynf3sh move bara el board aw fy makan already mta5ed
    if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
        return
    if board[row][col] is not None:
        return
    #save el move fel 2d array bta3na
    board[row][col] = turn
    draw_piece(row, col, turn)

    printboard()
    if checkwin(turn):
        messagebox.showinfo("Game Over", f"{turn.capitalize()} wins!")
        # 3shan el game yo2af        
        canvas.unbind("<Button-1>")

    
    if turn == "black":
        turn = "white"
    else:
        turn = "black"


def printboard():
    print("  " + " ".join(f"{i:2}" for i in range(BOARD_SIZE)))  # Print column indices
    for row in range(BOARD_SIZE):
        row_str = f"{row:2} "  # Print row index
        for col in range(BOARD_SIZE):
            if board[row][col] == "black":
                row_str += "B "
            elif board[row][col] == "white":
                row_str += "W "
            else:
                row_str += ". "
        print(row_str)

def checkwin(color):
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] == color:
                # horizontal 
                if col + 4 < BOARD_SIZE:
                    if board[row][col + 1] == color and \
                       board[row][col + 2] == color and \
                       board[row][col + 3] == color and \
                       board[row][col + 4] == color:
                        return True
                # vertical
                if row + 4 < BOARD_SIZE:
                    if board[row + 1][col] == color and \
                       board[row + 2][col] == color and \
                       board[row + 3][col] == color and \
                       board[row + 4][col] == color:
                        return True

                # diagonal
                if row + 4 < BOARD_SIZE and col + 4 < BOARD_SIZE:
                    if board[row + 1][col + 1] == color and \
                       board[row + 2][col + 2] == color and \
                       board[row + 3][col + 3] == color and \
                       board[row + 4][col + 4] == color:
                        return True

                # diagonal eltany
                if row + 4 < BOARD_SIZE and col - 4 >= 0:
                    if board[row + 1][col - 1] == color and \
                       board[row + 2][col - 2] == color and \
                       board[row + 3][col - 3] == color and \
                       board[row + 4][col - 4] == color:
                        return True

    return False

canvas.bind("<Button-1>", handle_click)

# Adding a welcome screen with game mode selection

def start_game(mode):
    welcome_window.destroy()
    if mode == "AI vs AI":
        print("Starting AI vs AI mode...")
        # Initialize AI vs AI logic here
    elif mode == "User vs AI":
        # Show another window for AI strategy selection
        ai_strategy_window = tk.Toplevel()
        ai_strategy_window.title("Select AI Strategy")
        ai_strategy_window.geometry("300x200")

        strategy_label = tk.Label(ai_strategy_window, text="Select AI Strategy", font=("Arial", 14))
        strategy_label.pack(pady=20)

        random_button = tk.Button(ai_strategy_window, text="Random", command=lambda: start_user_vs_ai("Random", ai_strategy_window))
        random_button.pack(pady=5)

        minimax_button = tk.Button(ai_strategy_window, text="Minimax", command=lambda: start_user_vs_ai("Minimax", ai_strategy_window))
        minimax_button.pack(pady=5)

        alpha_beta_button = tk.Button(ai_strategy_window, text="Alpha-Beta Pruning", command=lambda: start_user_vs_ai("Alpha-Beta Pruning", ai_strategy_window))
        alpha_beta_button.pack(pady=5)
    elif mode == "User vs User":
        print("Starting User vs User mode...")
        # Proceed with the existing game logic
        window.deiconify()

def handle_click_user_vs_ai(event):
    global turn, random_agent

    # Ensure it's the user's turn
    if turn == "black":
        col = round((event.x - CELL_SIZE // 2) / CELL_SIZE)
        row = round((event.y - CELL_SIZE // 2) / CELL_SIZE)

        if row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
            return
        if board[row][col] is not None:
            return

        # User's move
        board[row][col] = "black"
        draw_piece(row, col, "black")

        printboard()
        if checkwin("black"):
            messagebox.showinfo("Game Over", "Black wins!")
            canvas.unbind("<Button-1>")
            return

        # Switch turn to AI
        turn = "white"

        # Trigger AI's move after user's move
        canvas.after(500, random_agent_move)


def start_user_vs_ai(strategy, ai_strategy_window):
    ai_strategy_window.destroy()
    print(f"Starting User vs AI mode with {strategy} strategy...")

    global ai_agent
    canvas.bind("<Button-1>", handle_click_user_vs_ai)

    if strategy == "Random":
        ai_agent = RandomAgent(board, "white")
    elif strategy == "Minimax":
        ai_agent = MinimaxAgent(board, "white")

    window.deiconify()

# Create a welcome screen
welcome_window = tk.Toplevel()
welcome_window.title("Welcome to Gomoku")
welcome_window.geometry("300x200")

welcome_label = tk.Label(welcome_window, text="Select Game Mode", font=("Arial", 14))
welcome_label.pack(pady=20)

ai_vs_ai_button = tk.Button(welcome_window, text="AI vs AI", command=lambda: start_game("AI vs AI"))
ai_vs_ai_button.pack(pady=5)

user_vs_ai_button = tk.Button(welcome_window, text="User vs AI", command=lambda: start_game("User vs AI"))
user_vs_ai_button.pack(pady=5)

user_vs_user_button = tk.Button(welcome_window, text="User vs User", command=lambda: start_game("User vs User"))
user_vs_user_button.pack(pady=5)

# Hide the main game window until a mode is selected
window.withdraw()
def random_agent_move():
    global turn, ai_agent

    if turn == "white":
        ai_agent.make_move()

        if checkwin("white"):
            messagebox.showinfo("Game Over", "White wins!")
            canvas.unbind("<Button-1>")
            return

        turn = "black"

class RandomAgent:
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn

    def get_random_move(self):
        free_spots = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if self.board[row][col] is None]
        if free_spots:
            return random.choice(free_spots)
        return None

    def make_move(self):
        move = self.get_random_move()
        if move:
            row, col = move
            self.board[row][col] = self.turn
            draw_piece(row, col, self.turn)

            printboard()
#-------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------MINIMAX--------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------
class MinimaxAgent:
    def __init__(self, board, turn, depth=1):
        self.board = board
        self.turn = turn
        self.opponent = "black" if turn == "white" else "white"
        self.depth = depth

    def make_move(self):
        # hanshoof law mommken aksab fel move elgaya , if so hal3bha
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is None: #law elmakan fady garab hot el piece hena
                    self.board[row][col] = self.turn
                    if checkwin(self.turn):
                        draw_piece(row, col, self.turn)
                        printboard()
                        return
                    self.board[row][col] = None 

        # lw el opponenet howa ell hayksab block el move
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] is None:
                    self.board[row][col] = self.opponent
                    if checkwin(self.opponent):
                        self.board[row][col] = self.turn  
                        draw_piece(row, col, self.turn)
                        printboard()
                        return
                    self.board[row][col] = None

        #bn3ed el pieces ely fel board 3shan awll 2 moves yb2o fixed
        total_pieces = sum(1 for row in range(BOARD_SIZE) for col in range(BOARD_SIZE) if self.board[row][col] is not None)

        # awl move tb2a fel center
        if total_pieces == 1:
            center = BOARD_SIZE // 2
            if self.board[center][center] is None:
                row, col = center, center
            else:
                #law el center mmta5ed 5od ay cell gambo fadya 
                if center + 1 < BOARD_SIZE and self.board[center][center + 1] is None:
                    row, col = center, center + 1
                elif center - 1 >= 0 and self.board[center][center - 1] is None:
                    row, col = center, center - 1
                elif center + 1 < BOARD_SIZE and self.board[center + 1][center] is None:
                    row, col = center + 1, center
                elif center - 1 >= 0 and self.board[center - 1][center] is None:
                    row, col = center - 1, center
                
        # 3l move eltanya tb2a ay haga gamb el ola
        elif total_pieces == 3:
            # dawar 3la my piece el ola
            for r in range(BOARD_SIZE):
                for c in range(BOARD_SIZE):
                    if self.board[r][c] == self.turn:
                        if r + 1 < BOARD_SIZE and self.board[r + 1][c] is None:
                            row, col = r + 1, c
                            break
                        elif r - 1 >= 0 and self.board[r - 1][c] is None:
                            row, col = r - 1, c
                            break
                        elif c + 1 < BOARD_SIZE and self.board[r][c + 1] is None:
                            row, col = r, c + 1
                            break
                        elif c - 1 >= 0 and self.board[r][c - 1] is None:
                            row, col = r, c - 1
                            break
        else:
            score, move = self.minimax(copy.deepcopy(self.board), self.depth, True)
            row, col = move

        self.board[row][col] = self.turn
        draw_piece(row, col, self.turn)
        printboard()


    def minimax(self, board, depth, is_maximizing):
        if depth == 0 or checkwin(self.turn) or checkwin(self.opponent):
            return self.evaluate(board), None #5lsna tadweer bel depth elmatloob aw had keseb

        best_score = -1000000000000000 if is_maximizing else 100000000000000
        best_move = None

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board[row][col] is None:
                     #bnlef 3la koll el cells elfadya w bngarab nhot our piec law max aw opponent's law mini
                    board[row][col] = self.turn if is_maximizing else self.opponent
                    score, _ = self.minimax(board, depth - 1, not is_maximizing) 
                    board[row][col] = None

                    if is_maximizing:
                        if score > best_score:
                            best_score = score
                            best_move = (row, col)
                    else:
                        if score < best_score:
                            best_score = score
                            best_move = (row, col)

        return best_score, best_move

    def evaluate(self, board):
        score = 0

        # bndy heuristic score , kol ma el pieces ely wara b3d b nfs ellon aktar kol ma ba2a ahsan
        score += self.count(board, self.turn, 4) * 10000
        score += self.count(board, self.turn, 3) * 1000
        score += self.count(board, self.turn, 2) * 100

      
        score -= self.count(board, self.opponent, 4) * 10000
        score -= self.count(board, self.opponent, 3) * 1000
        score -= self.count(board, self.opponent, 2) * 100

        return score

    def count(self, board, color, length):
        #function bt3d 3dd el pieces ely wara b3d nfs elllon
        count = 0
        

        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):

                # 3ard
                if col + length - 1 < BOARD_SIZE:
                    if all(board[row][col + i] == color for i in range(length)):
                        count += 1

                # tool
                if row + length - 1 < BOARD_SIZE:
                    if all(board[row + i][col] == color for i in range(length)):
                        count += 1

                # Diagonal 
                if row + length - 1 < BOARD_SIZE and col + length - 1 < BOARD_SIZE:
                    if all(board[row + i][col + i] == color for i in range(length)):
                        count += 1

                # Diagonal (tany
                if row + length - 1 < BOARD_SIZE and col - length + 1 >= 0:
                    if all(board[row + i][col - i] == color for i in range(length)):
                        count += 1

        return count

window.mainloop()
