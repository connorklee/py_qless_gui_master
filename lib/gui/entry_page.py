# intro page to start game

import pickle, re, platform

from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showwarning

from lib.gui.game_page import GamePage
from lib.gui.start_page import StartPage

class EntryPage(Frame):
  def __init__(self, parent, dic='./dics/sowpods.txt'):
    self.parent = parent
    self.dict = dic

    Frame.__init__(self, parent, bg='azure')
    self.grid(row=0, column=0, sticky=S+N+E+W)

    self.parent.master.geometry("704x420")
    self.draw()

  def draw(self):
    Label(self, text='Welcome to PyQ-Less', font=('times', 40), bg='azure', pady=100).pack(side=TOP)

    f = Frame(self, bg='azure')
    f.pack(side=TOP)

    Button(f, text='Start Game', command=self.start_game).pack(side=LEFT, padx=10)
    # Button(f, text='QLess Solver', command=self.start_solver).pack(side=LEFT, padx=10)

    fb = Frame(self, bg='azure')
    fb.pack(side=TOP)

    # Button(self, text='Load Game', command=self.load_game).pack(side=TOP)

  def start_game(self):
    self.parent.master.geometry("704x550")
    self.parent.master.minsize(704, 550)

    GamePage(self.parent, self.dict)

#   def load_game(self):
#     filename = askopenfilename(initialdir='./saves', filetypes=(('Pickle Files', '*.pickle'),))

#     if filename:
#       file = open(filename, 'rb')
#       data = pickle.load(file)

#       options = {
#                   'chal_mode': data['chal_mode'],
#                   'comp_mode': data['comp_mode'],
#                   'normal_mode': data['norm_mode'],
#                   'time_limit': data['time_limit'],
#                   'point_limit': data['point_limit'],
#                   'play_num': data['play_num'],
#                   'loading': True
#                 }

#       self.parent.master.set_geometry()

#       game = GamePage(self.master, options)

#       game.cur_play_mark = data['cur_play_mark']
#       game.players = data['players']
#       game.bag = data['bag']
#       game.board = data['board']
#       game.op_score = data['op_score']
#       game.seconds = data['seconds']
#       game.minutes = data['minutes']
#       game.turns = data['turns']