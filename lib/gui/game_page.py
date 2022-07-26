# game page

from __future__ import print_function
import threading, re, os, pickle, queue, sys, platform

from tkinter import *
from tkinter.messagebox import askyesno, showwarning, showinfo
from tkinter.simpledialog import askstring
from tkinter.filedialog import asksaveasfilename

from pyparsing import col


from lib.dic import Dict
from lib.dice import Dice
from lib.word import Word
from lib.board import Board
from lib.player import Player
from lib.gui.tile import BoardTile, RackTile

class GamePage(Frame):
    def __init__(self, parent, dic='./dics/sowpods.txt'):
        Frame.__init__(self, parent, bg='azure')
        self.grid(row=0, column=0, sticky=S+N+E+W)

        self.dict = Dict(dic)
        self.dice = Dice()
        self.board = Board()

        self.set_variables()

        self.run()

    def run(self):
        self.draw_main_frame()
        self.initialize_player()

    def set_variables(self):
        self.word = None
        self.player = None
        self.start_tile = None

        self.gui_board = {}
        self.used_spots = {}
        self.placed_tiles = {}

        self.rack = []
        self.raw_word = []
        self.empty_rack_tiles = []
        self.word_list = []

        self.queue = queue.Queue()
        self.bag_info = StringVar()

    def draw_main_frame(self):
        out_f = Frame(self, padx=30, pady=30, bg='azure')
        out_f.pack(side=TOP)

        board_f = Frame(out_f)
        board_f.pack(side=TOP)

        row_num = 0
        row_name = 10

        while row_num < 10:
            col_num = 0
            col_name = 'a'

            while col_num < 10:
                tile = BoardTile(row_num, col_num, board_f)
                tile.bind('<1>', self.place_tile)
                tile.name = col_name + str(row_name)
                self.determine_tile_background(tile)

                self.gui_board[tile.name] = tile

                col_num += 1
                col_name = chr(ord(col_name) + 1)

            row_num += 1
            row_name -= 1

        rack = Frame(out_f, pady=15, bg='azure')
        rack.pack(side=TOP)

        for i in range(12):
            tile = RackTile(rack)
            tile.bind('<1>', self.place_tile)
            tile['bg'] = '#BE975B'

            self.rack.append(tile)

        button_f = Frame(out_f, bg='azure')
        button_f.pack(side=TOP)

        self.sub = Button(button_f, text='Submit Game')
        self.sub.config(command=self.submit_game)
        self.sub.pack(side=TOP, padx=5)

    def determine_tile_background(self, tile):
        tile['bg'] = '#ffd6cc'
    
    def place_tile(self, event):
        start_t_name = type(self.start_tile).__name__
        end_tile = event.widget
        end_t_name = type(end_tile).__name__
        end_t_letter = end_tile.letter

        if start_t_name == 'RackTile' and self.start_tile.letter.get() != '':
            if end_t_name == 'BoardTile' and end_tile.active:
                if end_t_letter.get() == '':
                    end_t_letter.set(self.start_tile.letter.get())
                    end_tile['bg'] = self.start_tile['bg']

                    self.placed_tiles[end_tile.name] = end_tile
                    self.empty_rack_tiles.append(self.start_tile)

                    self.start_tile['bg'] = '#cccccc'
                    self.start_tile.letter.set('')
                    self.start_tile = None
                else:
                    temp = end_t_letter.get()
                    end_t_letter.set(self.start_tile.letter.get())
                    self.start_tile.letter.set(temp)
                    self.start_tile = None
            elif end_t_name == 'RackTile':
                temp = end_t_letter.get()
                end_t_letter.set(self.start_tile.letter.get())

                if end_tile in self.empty_rack_tiles:
                    self.empty_rack_tiles.append(self.start_tile)
                    del self.empty_rack_tiles[self.empty_rack_tiles.index(end_tile)]

                    end_tile['bg'] = '#BE975B'
                    self.start_tile['bg'] = '#cccccc'

                self.start_tile.letter.set(temp)
                self.start_tile = None
            else:
                self.start_tile = None
        elif start_t_name == 'BoardTile' and self.start_tile.letter.get() != '' and self.start_tile.active:
            if end_t_name == 'RackTile' and end_t_letter.get() == '':
                del self.placed_tiles[self.start_tile.name]
                del self.empty_rack_tiles[self.empty_rack_tiles.index(end_tile)]

                end_t_letter.set(self.start_tile.letter.get())
                end_tile['bg'] = '#BE975B'

                self.determine_tile_background(self.start_tile)

                self.start_tile.letter.set('')
                self.start_tile = None
            elif end_t_name == 'BoardTile' and end_tile.active:
                if end_t_letter.get() == '':
                    end_t_letter.set(self.start_tile.letter.get())
                    end_tile['bg'] = self.start_tile['bg']

                    self.determine_tile_background(self.start_tile)

                    del self.placed_tiles[self.start_tile.name]

                    self.placed_tiles[end_tile.name] = end_tile

                    self.start_tile.letter.set('')
                    self.start_tile = None
                elif end_t_letter.get() == self.start_tile.letter.get():
                    self.start_tile = None
                else:
                    temp = end_t_letter.get()
                    end_t_letter.set(self.start_tile.letter.get())
                    self.start_tile.letter.set(temp)

                    self.placed_tiles[self.start_tile.name] = self.start_tile
                    self.placed_tiles[end_tile.name] = end_tile
                    self.start_tile = None
        else:
            self.start_tile = end_tile

    def determine_direction(self):
        # If there is only one letter in the list, find its direction
        if len(self.w_range) == 1:
            # Get the spots on the right and left side by changing letter value of the spot
            r = chr(ord(self.w_range[0][0]) + 1) + self.w_range[0][1:]
            l = chr(ord(self.w_range[0][0]) - 1) + self.w_range[0][1:]

            # Check the spots on the left and right side.
            # If they are occupied, the direction is r. If not, d.
            # Also check if they go over the board boundary.
            if self.board.board.get(r, False) and re.fullmatch('[A-Z@]', self.board.board[r]):
                self.direction = 'r'
            elif self.board.board.get(l, False) and re.fullmatch('[A-Z@]', self.board.board[l]):
                self.direction = 'r'
            else:
                self.direction = 'd'
        else:
            # use letter parts of the first and last spots for checking
            check1 = self.w_range[0][0]
            check2 = self.w_range[-1][0]

            # If letters are the same, direction is down
            if check1 == check2:
                # Need to sort number parts of the spots as digits for accuracy
                digits = sorted([int(x[1:]) for x in self.w_range])
                self.w_range = [check1 + str(x) for x in digits]
                self.w_range.reverse()

                self.direction = 'd'
            else:
                self.direction = 'r'

    def initialize_player(self):
        self.player = Player()
        self.player.roll_letters(self.dice)
        print('letters in hand: ', self.player.letters)
        self.decorate_rack()

    def decorate_rack(self):
        for letter, tile in zip(self.player.letters, self.rack):
            tile.letter.set(letter)

            tile['bg'] = '#BE975B'

    def get_norm_move(self):
        self.raw_word = []
        self.may_proceed = True
        
        # array for letters already on board
        self.aob_list = []

        self.w_range = sorted(self.placed_tiles)

        self.determine_direction()
        # self.set_raw_word()

        # Just the letters are necessary for word object
        aob_list = [x[2] for x in self.aob_list]

        self.word = Word(self.w_range[0], self.direction, self.raw_word, self.board, self.dict, aob_list)

        # Check if all the spots are on the same row or column
        if not self.valid_sorted_letters():
            self.may_proceed = False        

    # submit and validate words
    def submit_game(self):
        if self.placed_tiles:
            self.get_norm_move()

        if type(self.word) != type(None) and self.word.validate():
            print(self.word.word)
            self.player.word = self.word

    def valid_sorted_letters(self):
        if self.direction == 'd':
            # check1: the number part of spot
            check1 = int(self.w_range[0][1:])
            # check2: the letter part of spot
            check2 = self.w_range[0][0]

            # skip first spot because already checked
            for spot in self.w_range[1:]:
                # numbers should be consequent
                if int(spot[1:]) != check1 - 1:
                    return False

                # letters should be consequent
                if spot[0] != check2:
                    return False
                
                check1 -= 1
        
        else:
            # Check1 is the ascii value for the letter part of the spot
            check1 = ord(self.w_range[0][0])
            # Check2 is the number part of the spot
            check2 = self.w_range[0][1:]
            # Skip first spot because it is already used in checks
            for spot in self.w_range[1:]:
                # letters should be consequent
                if ord(spot[0]) != check1 + 1:
                    return False

                # Numbers should be the same
                if spot[1:] != check2:
                    return False

                check1 += 1

        return True           

    def determine_direction(self):
        print('determining direction')
        # use letter parts of first and last spots for checking
        check1 = self.w_range[0][0]
        check2 = self.w_range[-1][0]

        # if letters are the same, direction is down
        if check1 == check2:
            # Need to sort number parts of the spots as digits for accuracy
            digits = sorted([int(x[1:]) for x in self.w_range])
            self.w_range = [check1 + str(x) for x in digits]
            self.w_range.reverse()

            self.direction = 'd'
        else:
            self.direction = 'r'

        print(self.direction)

    def set_raw_word(self):
        print('raw word')
        for spot in self.w_range:
            self.raw_word.append(self.placed_tiles[spot].letter.get())
            self.set_aob_list(spot)

        # offset is necessary because array is mutable and it is dynamically
        # changed as the loop continues
        offset = 0
        length = len(self.w_range)

        for spot, index, letter in self.aob_list:
            if index < 0:
                index = 0
            elif index > length:
                index = length - 1

            self.raw_word.insert(index + offset, letter)
            self.w_range.insert(index + offset, spot)

            offset += 1

            self.raw_word = ''.join(self.raw_word)

