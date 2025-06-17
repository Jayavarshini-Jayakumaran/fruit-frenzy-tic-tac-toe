import os
from tkinter import *
import random
import pygame
import time

# Get the absolute path of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up from 'src' to access 'assets'
ASSETS_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "assets"))

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sounds using correct path
click_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sounds", "click.wav"))
win_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sounds", "win.wav"))
tie_sound = pygame.mixer.Sound(os.path.join(ASSETS_DIR, "sounds", "tie.wav"))

def play_sound(s):
    pygame.mixer.Sound.play(s)

def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == "" and check_winner() is False:
        buttons[row][column]['text'] = player
        play_sound(click_sound)

        if check_winner() is False:
            player = players[1] if player == players[0] else players[0]
            label.config(text=emoji_names[player] + " turn")
        elif check_winner() is True:
            label.config(text=emoji_names[player] + " wins 🎉")
            play_sound(win_sound)
            blink_winner()
        elif check_winner() == "Tie":
            label.config(text="It's a Tie! 🤝")
            play_sound(tie_sound)

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            for col in range(3):
                winner_buttons.append(buttons[row][col])
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != "":
            for row in range(3):
                winner_buttons.append(buttons[row][column])
            return True

    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        for i in range(3):
            winner_buttons.append(buttons[i][i])
        return True

    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        winner_buttons.extend([buttons[0][2], buttons[1][1], buttons[2][0]])
        return True

    if all(buttons[row][col]['text'] != "" for row in range(3) for col in range(3)):
        for row in range(3):
            for column in range(3):
                buttons[row][column].config(bg="#FFD580")
        return "Tie"
    return False

def new_game():
    global player, winner_buttons, blink_state, players, emoji_names
    player1, player2 = random.choice(fruit_pairs)
    players = [player1, player2]
    emoji_names = {
        player1: f"Player 1 {player1}",
        player2: f"Player 2 {player2}"
    }
    player = random.choice(players)
    winner_buttons = []
    blink_state = False
    label.config(text=emoji_names[player] + " turn")
    for row in range(3):
        for column in range(3):
            buttons[row][column].config(text="", bg="#FAF0E6")

def blink_winner():
    global blink_state
    color1 = "#FF69B4"
    color2 = "#90EE90"
    for btn in winner_buttons:
        btn.config(bg=color1 if blink_state else color2)
    blink_state = not blink_state
    window.after(400, blink_winner)

def start_animation():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(bg="#FFE4E1")
            window.update()
            time.sleep(0.1)
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(bg="#FAF0E6")
            window.update()
            time.sleep(0.05)

# Setup window
window = Tk()
window.title("Tic-Tac-Toe")
icon = PhotoImage(file='assets/images/TIC-TAC-TOE-Icon.png')
window.iconphoto(True, icon)
window.geometry("420x690")
window.configure(bg="#FCE4EC")

# Load background image using correct path
bg_image = PhotoImage(file=os.path.join(ASSETS_DIR, "images", "pixel_background.png"))
bg_label = Label(window, image=bg_image)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Fruit emoji combinations
fruit_pairs = [
    ("🍓", "🍇"),
    ("🍎", "🍑"),
    ("🍍", "🍒"),
    ("🍉", "🥭"),
    ("🥝", "🍏"),
    ("🍊", "🍈"),
    ("🥥", "🍐"),
    ("🍋", "🍉"),
    ("🍑", "🍓"),
    ("🍇", "🥝")
]

# Initial random fruits
player1, player2 = random.choice(fruit_pairs)
players = [player1, player2]
emoji_names = {
    player1: f"Player 1 {player1}",
    player2: f"Player 2 {player2}"
}
player = random.choice(players)

# GUI components
buttons = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
winner_buttons = []
blink_state = False

label = Label(window, text=emoji_names[player] + " turn", font=('Pixel Emulator', 28), bg="#FCE4EC", fg="#333")
label.pack(pady=20)

reset_button = Button(window, text="Restart 🔄", font=('Pixel Emulator', 16), bg="#FFB6C1", fg="#333", relief=FLAT, command=new_game)
reset_button.pack(pady=10)

frame = Frame(window, bg="#FCE4EC")
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text="", font=('Arial', 40), width=4, height=2, bg="#FAF0E6", fg="#333",
                                      relief=FLAT, activebackground="#FFDDC1",
                                      command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column, padx=5, pady=5)

# Play startup animation
window.after(500, start_animation)

window.mainloop()
