import tkinter as tk
from board import Board
from alg import Algorithm

WIDTH = 10
HEIGHT = 5
NUM_MINES = 5
num_non_mines = WIDTH * HEIGHT - NUM_MINES
tiles_revealed = 0
# "C": Covered, "U": Uncovered, "F": Flagged
current_state = [["C" for _ in range(WIDTH)] for _ in range(HEIGHT)]


def reveal_tile(event):
    global tiles_revealed
    tiles_revealed += 1
    x, y = map(int, event.widget.cget("text").split(":"))
    tile_value = game_board.board[y][x]
    current_state[y][x] = "U"
    event.widget.config(text=tile_value)
    if tile_value == 0:
        # Reveal all surrounding tiles
        for i in range(y - 1, y + 2):
            for j in range(x - 1, x + 2):
                if i >= 0 and j >= 0 and i < HEIGHT and j < WIDTH:
                    win.grid_slaves(i, j)[0].event_generate("<Button-1>", when="tail")
    
    if tile_value == "💣":
        event.widget.configure(bg="red", fg="red")
        game_over("You lose!")
    elif tiles_revealed == num_non_mines:
        game_over("YOU WIN!")
    else:
        event.widget.configure(bg="green", fg="black")
        event.widget.unbind("<Button-1>")
        event.widget.unbind("<Button-2>")
        event.widget.unbind("<Button-3>")


def flag_tile(event):
    x, y = map(int, event.widget.cget("text").split(":"))
    current_state[y][x] = "F"
    event.widget.configure(bg="red", fg="red")
    event.widget.bind("<Button-1>", unflag_tile)
    event.widget.unbind("<Button-2>")
    event.widget.unbind("<Button-3>")

def unflag_tile(event):
    x, y = map(int, event.widget.cget("text").split(":"))
    current_state[y][x] = "C"
    event.widget.configure(bg="gray", fg="gray")
    event.widget.bind("<Button-1>", reveal_tile)
    event.widget.bind("<Button-2>", flag_tile)
    event.widget.bind("<Button-3>", flag_tile)

def do_hint():
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if current_state[y][x] == "U":
                win.grid_slaves(y, x)[0].configure(bg="green", fg="black")
    mines, safe, wrong = hints.find_move(current_state)
    for x, y in mines:
        win.grid_slaves(y, x)[0].configure(bg="orange", fg="orange")
    for x, y in safe:
        win.grid_slaves(y, x)[0].configure(bg="aqua", fg="aqua")
    for x, y in wrong:
        win.grid_slaves(y, x)[0].configure(bg="purple", fg="yellow")

def game_over(message):
    print(message)
    for x in range(WIDTH):
        for y in range(HEIGHT):
            win.grid_slaves(y, x)[0].unbind("<Button-1>")
            win.grid_slaves(y, x)[0].unbind("<Button-2>")
            win.grid_slaves(y, x)[0].unbind("<Button-3>")
    hint_button.config(command=None)
    popup = tk.Toplevel(win)
    popup.title("Game over")
    label = tk.Label(popup, text=message)
    label.pack(padx=20, pady=20)


win = tk.Tk()
win.title("MineSweeper 💣")
game_board = Board(WIDTH, HEIGHT, NUM_MINES, num_non_mines)
hints = Algorithm(game_board.board, HEIGHT, WIDTH)


for y in range(HEIGHT):
    for x in range(WIDTH):
        button = tk.Label(
            win,
            width=4,
            height=2,
            background="gray",
            highlightbackground="black",
            highlightthickness=2,
            text=f"{x}:{y}",
            foreground="gray"
            )
        button.grid(column=x, row=y, padx=2, pady=2, )
        button.bind("<Button-1>", reveal_tile)
        button.bind("<Button-2>", flag_tile)
        button.bind("<Button-3>", flag_tile)
hint_button = tk.Button(win, text="HINT", command=do_hint)
hint_button.grid(column=0, columnspan=WIDTH, row=HEIGHT, padx=2, pady=2)

win.mainloop()