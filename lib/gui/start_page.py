# start game

import random, platform

from tkinter import *

from lib.gui.game_page import GamePage

class StartPage(Frame):
    def __init__(self, parent, dic='./dics/sowpods.txt'):
        self.parent = parent
        self.dict = dic

        Frame.__init__(self, parent, bg='azure')
        self.grid(row=0, column=0, sticky=S+N+E+W)

        self.chal_var = IntVar()
        self.time_var = IntVar()
        self.point_var = IntVar()
        self.but_var = StringVar()

        self.but_var.set('Start Game')

        self.play_ents = []

        self.draw_heading()
        self.draw_player_name()

        self.opt_cont = Frame(self, bg='azure')
        self.opt_cont.pack(side=TOP, padx=96)

        self.draw_player_options()
        self.draw_secondary_options()

    def draw_heading(self):
        Label(self, text='OPTIONS', font=('times', 35, 'italic'), bg='azure', pady=40).pack(side=TOP)

    def draw_secondary_options(self):
        cb = Checkbutton(self, bg="azure", text='Challenge Mode', variable=self.chal_var)
        cb.pack(pady=15)
        cb.deselect()

        f1 = Frame(self, bg='azure')
        f1.pack()

        Label(f1, bg='azure', text='Time Limit:').pack(side=LEFT)

        Entry(f1, textvariable=self.time_var, width=3).pack(side=LEFT)
        self.time_var.set(0)

        f2 = Frame(self, bg='azure')
        f2.pack(pady=5)

        Label(f2, bg='azure', text='Point Limit:').pack(side=LEFT)

        Entry(f2, textvariable=self.point_var, width=3).pack(side=LEFT)
        self.point_var.set(0)

        f3 = Frame(self, bg='azure')
        f3.pack(pady=10)

        Button(f3, text="Back", command=self.destroy).pack(side=LEFT, padx=10)
        Button(f3, textvariable=self.but_var, command=self.construct_options).pack(side=LEFT)