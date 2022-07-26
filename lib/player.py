import random

class Player():
    def __init__(self):
        self.letters = []
        self.word = None
    
    def roll_letters(self, dice):
        self.letters = dice.roll()


