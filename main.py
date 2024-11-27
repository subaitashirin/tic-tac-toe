import tkinter as tk

board = {
    "P1": "", "P2": "", "P3": "",
    "P4": "", "P5": "", "P6": "",
    "P7": "", "P8": "", "P9": ""
}

highlighted_position = None

def check_win(player):
    win_combinations = [
        ["P1", "P2", "P3"], ["P4", "P5", "P6"], ["P7", "P8", "P9"],
        ["P1", "P4", "P7"], ["P2", "P5", "P8"], ["P3", "P6", "P9"],
        ["P1", "P5", "P9"], ["P3", "P5", "P7"]
    ]
    for combination in win_combinations:
        values = [board[pos] for pos in combination]
        if values.count(player) == 2 and values.count("") == 1:
            return combination[values.index("")]
    return None

def is_board_full():
    return all(value != "" for value in board.values())

def reset_board():
    global highlighted_position
    for position in board:
        board[position] = ""
        buttons[position].config(text=board[position], bg="lightgray")
    result_label.config(text="Board reset! Start a new game.", fg="blue")
    highlighted_position = None

def place_X(position):
    global highlighted_position

    if highlighted_position:
        buttons[highlighted_position].config(bg="lightgray")
        highlighted_position = None

    if board[position] == "":
        board[position] = "X"
        buttons[position].config(text="X", bg="lightblue", fg="black")
        winning_position = check_win("X")

        if winning_position:
            highlighted_position = winning_position
            buttons[winning_position].config(bg="green")
            result_label.config(text="Winning move! Click the green box.", fg="green")
        elif is_board_full():
            result_label.config(text="The board is full! Resetting...", fg="red")
            window.after(2000, reset_board)
        else:
            result_label.config(text="Make your next move!", fg="blue")

window = tk.Tk()
window.title("Tic-Tac-Toe: AI Winning Move Detector")
window.geometry("500x550")
window.configure(bg="lightyellow")

buttons = {}
for i, position in enumerate(board.keys(), 1):
    button = tk.Button(
        window, text=board[position], font=("Arial", 24),
        width=6, height=3, bg="lightgray", fg="black",
        activebackground="lightblue", activeforeground="black",
        command=lambda pos=position: place_X(pos)
    )
    buttons[position] = button
    button.grid(row=(i - 1) // 3, column=(i - 1) % 3, padx=5, pady=5)

result_label = tk.Label(window, text="Click a square to start!", font=("Arial", 16), bg="lightyellow", fg="blue")
result_label.grid(row=3, column=0, columnspan=3, pady=20)

window.mainloop()
