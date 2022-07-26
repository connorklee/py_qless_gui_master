import re

class Board:
    def __init__(self):
        self.__prepare_board()

    def valid_range(self, word_range, word, direction):
        for i, square in enumerate(word_range):
            if i == 0:
                if direction == 'd':
                    if self.occupied(square, 'r', self.up_or_left):
                        return False
                else:
                    if self.occupied(square, 'd', self.up_or_left):
                        return False
                
            if i == len(word_range) - 1:
                if direction == 'd':
                    if self.occupied(square, 'r', self.down_or_right):
                        return False
                    else:
                        if self.occupied(square, 'd', self.down_or_right):
                            return False

            if self.board[square] != word[i] and re.fullmatch('[A-Z]', self.board[square]):
                return False

        return True

    def place(self, letters, word_range):
        for letter, square in zip(letters, word_range):
            self.board[square] = letter

    def up_or_left(self, square, direction):
        if direction == 'r':
            return self.__square_up(square)
        else: 
            return self.__square_left(square)

    def down_or_right(self, square, direction):
        if direction == 'r':
            return self.__square_down(square)
        else:
            return self.__square_right(square)
    
    def occupied(self, square, direction, func):
        # Find ascii value of letter
        letter_ascii = ord(self.board.get(func(square, direction)))

        return letter_ascii > 64 and letter_ascii < 91

    def square_occupied(self, square, direction):
        down_or_right_occupied = self.occupied(square, direction, self.down_or_right)
        up_or_left_occupied = self.occupied(square, direction, self.up_or_left)

        return down_or_right_occupied or up_or_left_occupied

    def __square_up(self, square):
        # Number part of a spot increases as it goes up
        if len(square == 2):
            return square[0] + str(int(square[1]) + 1)
        else: 
            return square[0] + str(int(square[1:]) + 1)

    def __square_down(self, square):
        # Number part of a sport decreases as it goes up
        if len(square == 2):
            return square[0] + str(int(square[1]) - 1)
        else: 
            return square[0] + str(int(square[1:]) - 1)   
            
    def __square_left(self, square):
        # Letter part of a spot increases as it goes left
        if len(square) == 2:
            return chr(ord(square[0]) - 1) + square[1]
        else:
            return chr(ord(square[0]) - 1) + square[1:]  

    def __square_right(self, square):
        # Letter part of a spot decreases as it goes right
        if len(square) == 2:
            return chr(ord(square[0]) + 1) + square[1]
        else:
            return chr(ord(square[0]) + 1) + square[1:]  

    def __prepare_board(self):
        self.board = {}

        for num_part in range(1,10):
            for let_part in range(ord('a'), ord('j')):
                self.board[chr(let_part) + str(num_part)] = ' '
