# gui.py
import tkinter as tk
from tkinter import messagebox
from game import GameEngine, RandomAgent, MinimaxAgent, AlphaBetaAgent

# --- GUI Setup ---
window = tk.Tk()
window.title("Gomoku Game")

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

turn = "black"
ai_agent = None


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


def handle_click(event):
    global turn
    col = round((event.x - CELL_SIZE // 2) / CELL_SIZE)
    row = round((event.y - CELL_SIZE // 2) / CELL_SIZE)
    if not engine.is_valid_move(row, col):
        return
    engine.make_move(row, col, turn)
    draw_piece(row, col, turn)
    engine.printboard()
    if engine.checkwin(turn):
        messagebox.showinfo("Game Over", f"{turn.capitalize()} wins!")
        canvas.unbind("<Button-1>")
        return
    turn = "white" if turn == "black" else "black"


def handle_click_user_vs_ai(event):
    global turn, ai_agent
    if turn == "black":
        col = round((event.x - CELL_SIZE // 2) / CELL_SIZE)
        row = round((event.y - CELL_SIZE // 2) / CELL_SIZE)
        if not engine.is_valid_move(row, col):
            return
        engine.make_move(row, col, "black")
        draw_piece(row, col, "black")
        engine.printboard()
        if engine.checkwin("black"):
            messagebox.showinfo("Game Over", "Black wins!")
            canvas.unbind("<Button-1>")
            return
        turn = "white"
        canvas.after(500, ai_agent_move)


def ai_agent_move():
    global turn, ai_agent
    if turn == "white":
        move = ai_agent.get_move()
        if move:
            row, col = move
            engine.make_move(row, col, "white")
            draw_piece(row, col, "white")
            engine.printboard()
            if engine.checkwin("white"):
                messagebox.showinfo("Game Over", "White wins!")
                canvas.unbind("<Button-1>")
                return
            turn = "black"


def start_user_vs_ai(strategy, ai_strategy_window):
    ai_strategy_window.destroy()
    global ai_agent
    canvas.bind("<Button-1>", handle_click_user_vs_ai)
    if strategy == "Random":
        ai_agent = RandomAgent(engine, "white")
    elif strategy == "Minimax":
        ai_agent = MinimaxAgent(engine, "white")
    elif strategy == "Alpha-Beta Pruning":
        ai_agent = AlphaBetaAgent(engine, "white")
    window.deiconify()


def start_game(mode):
    welcome_window.destroy()
    if mode == "AI vs AI":
        window.deiconify()
        start_ai_vs_ai()
    elif mode == "User vs AI":
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
        window.deiconify()
        canvas.bind("<Button-1>", handle_click)


def start_ai_vs_ai():
    global ai1, ai2, turn
    ai1 = MinimaxAgent(engine, "black")
    ai2 = AlphaBetaAgent(engine, "white")
    turn = "black"
    ai_vs_ai_move()


def ai_vs_ai_move():
    global turn, ai1, ai2
    if turn == "black":
        move = ai1.get_move()
        if move:
            row, col = move
            engine.make_move(row, col, "black")
            draw_piece(row, col, "black")
            engine.printboard()
            if engine.checkwin("black"):
                messagebox.showinfo("Game Over", "Black wins!")
                return
            turn = "white"
    else:
        move = ai2.get_move()
        if move:
            row, col = move
            engine.make_move(row, col, "white")
            draw_piece(row, col, "white")
            engine.printboard()
            if engine.checkwin("white"):
                messagebox.showinfo("Game Over", "White wins!")
                return
            turn = "black"
    window.after(300, ai_vs_ai_move)


# --- Welcome Screen ---
welcome_window = tk.Toplevel()
welcome_window.title("Welcome to Gomoku")
x = (screen_width // 2) - (150)
y = (screen_height // 2) - (100)
welcome_window.geometry(f"300x200+{x}+{y}")

welcome_label = tk.Label(welcome_window, text="Select Game Mode", font=("Arial", 14))
welcome_label.pack(pady=20)
ai_vs_ai_button = tk.Button(
    welcome_window, text="AI vs AI", command=lambda: start_game("AI vs AI")
)
ai_vs_ai_button.pack(pady=5)
user_vs_ai_button = tk.Button(
    welcome_window, text="User vs AI", command=lambda: start_game("User vs AI")
)
user_vs_ai_button.pack(pady=5)
user_vs_user_button = tk.Button(
    welcome_window, text="User vs User", command=lambda: start_game("User vs User")
)
user_vs_user_button.pack(pady=5)
window.withdraw()

window.mainloop()
