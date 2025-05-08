# gui.py
import tkinter as tk
from tkinter import messagebox
from game import GameEngine, RandomAgent, MinimaxAgent, AlphaBetaAgent
import time

# --- GUI Setup ---
window = tk.Tk()
window.title("Gomoku Game")

# Player indicator label
player_indicator = tk.Label(window, text="", font=("Arial", 14))
player_indicator.pack(pady=10)

# Center the window on the screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Initialize the game engine
engine = GameEngine()
BOARD_SIZE = engine.BOARD_SIZE
CELL_SIZE = engine.CELL_SIZE
WINDOW_SIZE = engine.WINDOW_SIZE

x = (screen_width // 2) - (WINDOW_SIZE // 2)
y = (screen_height // 2) - (WINDOW_SIZE // 2)
window.geometry(f"{WINDOW_SIZE}x{WINDOW_SIZE}+{x}+{y}")

canvas = tk.Canvas(window, width=WINDOW_SIZE, height=WINDOW_SIZE, bg="#997950")
canvas.pack()

# Draw the grid
for i in range(BOARD_SIZE):
    x = i * CELL_SIZE + CELL_SIZE // 2
    canvas.create_line(x, CELL_SIZE // 2, x, WINDOW_SIZE - CELL_SIZE // 2)
    y = i * CELL_SIZE + CELL_SIZE // 2
    canvas.create_line(CELL_SIZE // 2, y, WINDOW_SIZE - CELL_SIZE // 2, y)


def draw_piece(row, col, color):
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    radius = 17
    canvas.create_oval(
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius,
        fill=color,
    )


def update_board():
    canvas.delete("piece")
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            color = engine.board[row][col]
            if color:
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = row * CELL_SIZE + CELL_SIZE // 2
                radius = 17
                canvas.create_oval(
                    center_x - radius,
                    center_y - radius,
                    center_x + radius,
                    center_y + radius,
                    fill=color,
                    tags="piece",
                )


def handle_click(event):
    col = round((event.x - CELL_SIZE // 2) / CELL_SIZE)
    row = round((event.y - CELL_SIZE // 2) / CELL_SIZE)
    if not engine.play_move(row, col):
        return
    update_board()
    engine.printboard()
    if engine.is_game_over():
        winner = engine.get_winner()
        if winner:
            messagebox.showinfo("Game Over", f"{winner.capitalize()} wins!")
        else:
            messagebox.showinfo("Game Over", "Draw!")
        canvas.unbind("<Button-1>")


def handle_click_user_vs_ai(event):
    if engine.get_current_player() == "black":
        col = round((event.x - CELL_SIZE // 2) / CELL_SIZE)
        row = round((event.y - CELL_SIZE // 2) / CELL_SIZE)
        if not engine.play_move(row, col):
            return
        update_board()
        engine.printboard()
        if engine.is_game_over():
            winner = engine.get_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner.capitalize()} wins!")
            else:
                messagebox.showinfo("Game Over", "Draw!")
            canvas.unbind("<Button-1>")
            return
        canvas.after(500, ai_agent_move)


def ai_agent_move():
    if engine.get_current_player() == "white" and not engine.is_game_over():
        move = ai_agent.get_move()
        if move:
            row, col = move
            engine.play_move(row, col)
            update_board()
            engine.printboard()
            if engine.is_game_over():
                winner = engine.get_winner()
                if winner:
                    messagebox.showinfo("Game Over", f"{winner.capitalize()} wins!")
                else:
                    messagebox.showinfo("Game Over", "Draw!")
                canvas.unbind("<Button-1>")
                return


def set_player_indicator(mode, ai_strategy=None):
    if mode == "User vs AI":
        if ai_strategy == "Random":
            player_indicator.config(text="Black: Human  |  White: RandomAgent")
        elif ai_strategy == "Minimax":
            player_indicator.config(text="Black: Human  |  White: MinimaxAgent")
        elif ai_strategy == "Alpha-Beta Pruning":
            player_indicator.config(text="Black: Human  |  White: AlphaBetaAgent")
        else:
            player_indicator.config(text="Black: Human  |  White: AI")
    elif mode == "User vs User":
        player_indicator.config(text="Black: Player 1  |  White: Player 2")
    elif mode == "AI vs AI (Minimax vs AlphaBeta)":
        player_indicator.config(text="Black: MinimaxAgent  |  White: AlphaBetaAgent")
    else:
        player_indicator.config(text="")


def start_user_vs_ai(strategy, ai_strategy_window):
    ai_strategy_window.destroy()
    global ai_agent
    engine.reset()
    update_board()
    canvas.bind("<Button-1>", handle_click_user_vs_ai)
    set_player_indicator("User vs AI", strategy)
    if strategy == "Random":
        ai_agent = RandomAgent(engine, "white")
    elif strategy == "Minimax":
        ai_agent = MinimaxAgent(engine, "white")
    elif strategy == "Alpha-Beta Pruning":
        ai_agent = AlphaBetaAgent(engine, "white")
    window.deiconify()


def ai_vs_ai_minmax_alphabeta_gui():
    engine.reset()
    update_board()
    black_agent = MinimaxAgent(engine, "black")
    white_agent = AlphaBetaAgent(engine, "white")
    move_num = 1

    def play_next():
        nonlocal move_num
        if engine.is_game_over():
            winner = engine.get_winner()
            if winner:
                messagebox.showinfo("Game Over", f"{winner.capitalize()} wins!")
            else:
                messagebox.showinfo("Game Over", "Draw!")
            return
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
        update_board()
        engine.printboard()
        move_num += 1
        window.after(200, play_next)

    play_next()


def start_game(mode):
    welcome_window.destroy()
    engine.reset()
    update_board()
    if mode == "User vs AI":
        ai_strategy_window = tk.Toplevel()
        ai_strategy_window.title("Select AI Strategy")
        ai_strategy_window.geometry("300x200")
        x = (screen_width // 2) - (150)
        y = (screen_height // 2) - (100)
        ai_strategy_window.geometry(f"300x200+{x}+{y}")
        strategy_label = tk.Label(
            ai_strategy_window, text="Select AI Strategy", font=("Arial", 14)
        )
        strategy_label.pack(pady=20)
        random_button = tk.Button(
            ai_strategy_window,
            text="Random",
            command=lambda: start_user_vs_ai("Random", ai_strategy_window),
        )
        random_button.pack(pady=5)
        minimax_button = tk.Button(
            ai_strategy_window,
            text="Minimax",
            command=lambda: start_user_vs_ai("Minimax", ai_strategy_window),
        )
        minimax_button.pack(pady=5)
        alpha_beta_button = tk.Button(
            ai_strategy_window,
            text="Alpha-Beta Pruning",
            command=lambda: start_user_vs_ai("Alpha-Beta Pruning", ai_strategy_window),
        )
        alpha_beta_button.pack(pady=5)
    elif mode == "User vs User":
        canvas.bind("<Button-1>", handle_click)
        set_player_indicator("User vs User")
        window.deiconify()
    elif mode == "AI vs AI (Minimax vs AlphaBeta)":
        set_player_indicator("AI vs AI (Minimax vs AlphaBeta)")
        window.deiconify()
        ai_vs_ai_minmax_alphabeta_gui()


# --- Welcome Screen ---
welcome_window = tk.Toplevel()
welcome_window.title("Welcome to Gomoku")
x = (screen_width // 2) - (150)
y = (screen_height // 2) - (100)
welcome_window.geometry(f"300x200+{x}+{y}")

welcome_label = tk.Label(welcome_window, text="Select Game Mode", font=("Arial", 14))
welcome_label.pack(pady=20)
user_vs_ai_button = tk.Button(
    welcome_window, text="User vs AI", command=lambda: start_game("User vs AI")
)
user_vs_ai_button.pack(pady=5)
user_vs_user_button = tk.Button(
    welcome_window, text="User vs User", command=lambda: start_game("User vs User")
)
user_vs_user_button.pack(pady=5)
ai_vs_ai_button = tk.Button(
    welcome_window,
    text="AI vs AI (Minimax vs AlphaBeta)",
    command=lambda: start_game("AI vs AI (Minimax vs AlphaBeta)"),
)
ai_vs_ai_button.pack(pady=5)
window.withdraw()

window.mainloop()
