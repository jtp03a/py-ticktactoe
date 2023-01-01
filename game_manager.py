from gametile import Tile
from tkinter import messagebox, Label
import socket
import threading

class GameManager:
  def __init__(self):
    self.current_player = 'X'
    self.board_size = 9
    self.board = [
      [Tile(text="1", game_state=self), Tile(text="2", game_state=self), Tile(text="3", game_state=self)],
      [Tile(text="4", game_state=self), Tile(text="5", game_state=self), Tile(text="6", game_state=self)],
      [Tile(text="7", game_state=self), Tile(text="8", game_state=self), Tile(text="9", game_state=self)]
    ]
    self.draw_board()
    self.game_over = False
    self.player1_score = 0
    self.player2_score = 0
    self.current_player_title = Label(text='Current Player: ')
    self.current_player_title.grid(row=3, column=0)
    self.current_player_lbl = Label(text='')
    self.current_player_lbl.grid(row=3, column=1)
    self.move_num = 0
    self.current_move = 0
    self.move_played = False
    self.received_move = False

  def host_game(self, host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(1)

    client, addr = server.accept()

    self.you = 'X'
    self.opponent = 'O'

    self.current_player_lbl['text'] = self.you

    threading.Thread(target=self.handle_connection, args=(client,)).start()
    server.close()

  def connect_to_server(self, host, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
    self.you = 'O'
    self.opponent = 'X'

    self.current_player_lbl['text'] = self.you

    threading.Thread(target=self.handle_connection, args=(client,)).start()

  def handle_connection(self, client):
    while not self.game_over:
      if self.current_player == self.you and not self.move_played:
        print('Im the current player and I am deciding my move')
        continue
      elif self.current_player == self.you and self.move_played:
        print('I am the current player and now sending my move')
        move = str(self.current_move)
        client.send(move.encode('utf-8'))
        self.current_player = self.opponent
        self.move_played = False
      elif self.current_player == self.opponent and not self.received_move:
        print('I am not the current player and I am waiting to receive a move')
        data = client.recv(1024)
        if not data:
          print('hit data break')
          break
        else:
          print('I am not the current player and I have received data')
          print(data)
          self.received_move = True
      elif self.current_player == self.opponent and self.received_move:
          print('I am not the current player and am updating my board')
          self.update_board(int(data.decode('utf-8')))
          self.current_player = self.you
          self.received_move = False
    client.close()

  def update_board(self, move):
    update_row = int((move // 3.1))
    if update_row == 0:
      update_col = move - 1
    elif update_row == 1:
      update_col = move - 4
    elif update_row == 2:
      update_col = move - 7
    
    self.board[update_row][update_col]['text'] = self.current_player
    self.check_win()

  def draw_board(self):
    for i, row in enumerate(self.board):
      for j, tile in enumerate(row): 
        tile.grid(column=j, row=i)

  def play_move(self, tile_num):
    self.current_move = tile_num
    self.move_num += 1
    self.move_played = True
    if self.move_num == 9:
      messagebox.showinfo('Game Over', 'The Game was a Tie')
      self.reset_game()
    else:
      self.check_win()

  def check_win(self):
      if self.board[0][0]['text'] == self.board[0][1]['text'] == self.board[0][2]['text']:
        print('horizontal win detected')
        self.game_over = True
      elif self.board[1][0]['text'] == self.board[1][1]['text'] == self.board[1][2]['text']:
        print('horizontal win detected')
        self.game_over = True
      elif self.board[2][0]['text'] == self.board[2][1]['text'] == self.board[2][2]['text']:
        print('horizontal win detected')
        self.game_over = True
      elif self.board[0][0]['text'] == self.board[1][0]['text'] == self.board[2][0]['text']:
        print('vertical win detected')
        self.game_over = True
      elif self.board[0][1]['text'] == self.board[1][1]['text'] == self.board[2][1]['text']:
        print('vertical win detected')
        self.game_over = True
      elif self.board[0][2]['text'] == self.board[1][2]['text'] == self.board[2][2]['text']:
        print('vertical win detected')
        self.game_over = True
      elif self.board[0][0]['text'] == self.board[1][1]['text'] == self.board[2][2]['text']:
        print('diagonal win detected')
        self.game_over = True
      elif self.board[0][2]['text'] == self.board[1][1]['text'] == self.board[2][0]['text']:
        print('diagonal win detected')
        self.game_over = True
      if self.game_over:
        messagebox.showinfo("Game Over", f"Player {self.current_player} Won the Game")
        self.reset_game()
  
  def reset_game(self):
    self.game_over = False

    self.board[0][0]['text'] = '1'
    self.board[0][1]['text'] = '2'
    self.board[0][2]['text'] = '3'
    self.board[1][0]['text'] = '4'
    self.board[1][1]['text'] = '5'
    self.board[1][2]['text'] = '6'
    self.board[2][0]['text'] = '7'
    self.board[2][1]['text'] = '8'
    self.board[2][2]['text'] = '9'

    for row in self.board:
      for tile in row: 
        tile.empty = True
    
    self.move_num = 0
