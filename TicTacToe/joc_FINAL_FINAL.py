import tkinter as tk
import os
#print("Fișierul va fi salvat în:", os.getcwd())



def read_scores(file_name):
   
    scores = {"playerX_score": 0, "playerO_score": 0}
    try:
        with open(file_name, "r") as file:
            for line in file:
                key, value = line.strip().split("=")
                scores[key] = int(value)
    except FileNotFoundError:
        print(f"Fisierul'{file_name}' nu a fost gasit. Scorurile initiale vor fi 0.")
    except ValueError:
        print(f"Formatul fisierului '{file_name}' nu este valid.")
    return scores

def save_scores(file_name, scores):
   
    try:
        with open(file_name, "w") as file:
            for key, value in scores.items():
                file.write(f"{key}={value}\n")
    except Exception as e:
        print(f"Eroare: {e}")


def set_tile(row, column):
    global curr_player, game_over, turns

    if game_over or board[row][column]["text"] != "":
        return

    board[row][column]["text"] = curr_player

    if curr_player == playerO:
        curr_player = playerX
    else:
        curr_player = playerO

    label_turn["text"] = curr_player + "'s turn"
    check_winner()

def check_winner():
    global turns, game_over, scores

    turns += 1

    #orizontal
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] and board[row][0]["text"] != "":
            declare_winner(board[row][0]["text"])
            return

    #vertical
    for column in range(3):
        if board[0][column]["text"] == board[1][column]["text"] == board[2][column]["text"] and board[0][column]["text"] != "":
            declare_winner(board[0][column]["text"])
            return

    #diagonalele
    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] and board[0][0]["text"] != "":
        declare_winner(board[0][0]["text"])
        return

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] and board[0][2]["text"] != "":
        declare_winner(board[0][2]["text"])
        return

    #egal
    if turns == 9:
        label_turn["text"] = "It's a tie!"
        game_over = True

def declare_winner(winner):
    global game_over, scores
    game_over = True

    if winner == playerX:
        scores["playerX_score"] += 1
    else:
        scores["playerO_score"] += 1

    label_turn["text"] = winner + " is the winner!"
    label_score["text"] = f"Player X: {scores['playerX_score']} | Player O: {scores['playerO_score']}"

    
    save_scores(score_file, scores)

def new_game():
    global turns, game_over, curr_player
    turns = 0
    game_over = False
    curr_player = playerX

    label_turn["text"] = curr_player + "'s turn"

    for row in range(3):
        for column in range(3):
            board[row][column].config(text="")


playerX = "X"
playerO = "O"
curr_player = playerX
turns = 0
game_over = False


score_file = "fisier_scor"


scores = read_scores(score_file)
playerX_score = scores["playerX_score"]
playerO_score = scores["playerO_score"]


color_blue = "#4584b6"
color_light_gray = "#646464"


window = tk.Tk()
window.title("Tic Tac Toe")
window.resizable(False, False)

frame = tk.Frame(window)

label_turn = tk.Label(frame, text=curr_player + "'s turn", font=("Consolas", 20), foreground=color_blue)
label_turn.grid(row=0, column=0, columnspan=3)

label_score = tk.Label(frame, text=f"Player X: {playerX_score} | Player O: {playerO_score}", font=("Consolas", 16), foreground=color_blue)
label_score.grid(row=1, column=0, columnspan=3)

board = [[None for _ in range(3)] for _ in range(3)]

for row in range(3):
    for column in range(3):
        board[row][column] = tk.Button(frame, text="", font=("Consolas", 40), width=5, height=2,
                                       command=lambda r=row, c=column: set_tile(r, c), foreground=color_light_gray)
        board[row][column].grid(row=row + 2, column=column)

btn_restart = tk.Button(frame, text="Restart", font=("Consolas", 20), command=new_game, foreground=color_blue)
btn_restart.grid(row=5, column=0, columnspan=3)

frame.pack()


window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

window.mainloop()
