# initialize dice
# roll a starting hand

import random

class Dice:
    def __init__(self):
        self.dice = {}
        self.__fill_dice()
        self.hand = []

    def __fill_dice(self):
        self.dice['dice1'] = ['O', 'O', 'A', 'A', 'E', 'E']
        self.dice['dice2'] = ['A', 'I', 'O', 'U', 'U', 'E']
        self.dice['dice3'] = ['S', 'T', 'T', 'C', 'C', 'M']
        self.dice['dice4'] = ['W', 'F', 'L', 'L', 'D', 'R']
        self.dice['dice5'] = ['W', 'T', 'T', 'H', 'H', 'P']
        self.dice['dice6'] = ['C', 'C', 'D', 'B', 'J', 'T']
        self.dice['dice7'] = ['K', 'P', 'P', 'G', 'V', 'F']
        self.dice['dice8'] = ['Y', 'M', 'M', 'B', 'L', 'L']
        self.dice['dice9'] = ['N', 'N', 'I', 'I', 'O', 'Y']
        self.dice['dice10'] = ['D', 'R', 'R', 'G', 'G', 'L']
        self.dice['dice11'] = ['Z', 'X', 'S', 'B', 'K', 'N']
        self.dice['dice12'] = ['N', 'N', 'R', 'R', 'H', 'H']

    def roll(self):
        for dice in self.dice.keys():
            letter = random.choice(self.dice[dice])
            self.hand.extend(letter)
            


        return self.hand