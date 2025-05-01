import tkinter as tk
from tkinter import messagebox


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
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            print(board[row][col], end=" ")
        print("   \n")

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

window.mainloop()
