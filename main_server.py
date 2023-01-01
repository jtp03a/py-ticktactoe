from tkinter import *
from game_manager import GameManager

FONT_NAME = "Courier"

window = Tk()
window.title('Tic Tac Toe')
window.config(padx=25, pady=25)

game = GameManager()
game.host_game('localhost', 9999)

window.mainloop()
