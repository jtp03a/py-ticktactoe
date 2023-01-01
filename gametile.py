from tkinter import Button, messagebox

FONT_NAME = "Courier"

class Tile(Button):
  def __init__(self, text, game_state):
    super().__init__(text=text, font=((FONT_NAME, 45)), width=3, command=self.click)
    self.game_state = game_state
    self.empty = True
    self.tile_num = int(text)

  def click(self):
    if self.empty:
      self['text'] = self.game_state.current_player
      self.empty = False
      self.game_state.play_move(self.tile_num)
    else:
      messagebox.showerror(title="Error", message="Tile already picked")