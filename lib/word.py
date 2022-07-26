import re

class Word:
    def __init__(self, start, direction, word, board, dic, aob=[]):
        self.dict = dic
        self.word = word
        self.start = start
        self.board = board
        self.aob_list = aob
        self.direction = direction

        self.words = []
        self.new = True
        self.valid = False
        self.extra_words = []
        
        self.range = self.__set_range()

   # Builds extra words by making a word. Populates the extra words
   # array and return True if all words are valid     
    def process_extra_words(self):
        check_list = []
        aob_list = self.aob_list.copy()

    def valid_move(self):
        if not self.range:
            return False

        # For a word to be valid, either it should make use of an already
        # on board letter or one of its letters should be connected to
        # a word already on the board
        for square in self.range:
            if self.aob_list:
                return True
            elif self.board.square_occupied(square, self.direction):
                return True

        # # If it is not connected to any words, it might mean it is the
        # # first turn. In that case, it should start from 'h5', that is,
        # # from the middle square.
        # if self.start == 'h5':
        #     return True

        # return False

    def validate(self):
        if self.valid:
            return True
        else:
            if not self.valid_move():
                return False
            
            if not self.process_extra_words():
                return False
            
            # Dont't process words twice
            self.new = False
            self.valid = True

            return True

    # Return range if valid or False
    def __set_range(self):
        if self.direction == "r":
            squares = self.__set_range_to_right()
        else:
            squares = self.__set_range_to_down()

        # Check if the squares returned are in the range of 'a' to 'i' and 1 to 15
        for s in squares:
            if not re.fullmatch('[a-i]1[0-5]|[a-i][1-9]', s):
                return False

        if not self.board.valid_range(squares, self.word, self.direction):
            return False

        return squares

    def __set_range_to_right(self):
        # Determine the letter part of the last square of the word.
        # Because it is to the right, modify the letter part
        last = chr((ord(self.start[0]) + len(self.word)))

        # Check if the number part is 1 digit or 2 digits
        if len(self.start) == 2:
            # Make a list of letters by making use of ascii numbers
            letter_range = range(ord(self.start[0]), ord(last))

            # Map the number part of the spot with letters in the range
            return list(map(lambda x: chr(x) + self.start[1], letter_range))
        else:
            letter_range = range(ord(self.start[0]), ord(last))

            return list(map(lambda x: chr(x) + self.start[1:], letter_range))

    def __set_range_to_down(self):
        # Check if the number part is 1 digit or 2 digits
        if len(self.start) == 2:
            # Determine the number part of the last square of the word.
            # Because it is to the down, modify the number part.
            # Numbers decrease as it goes down. This one is 1 digit.
            last = int(self.start[1]) - len(self.word)
            # Make a list of numbers in reverse order
            number_range = range(int(self.start[1]), last, -1)

            # Map the letter part of the spot with numbers in the range
            return list(map(lambda x: self.start[0] + str(x), number_range))
        else:
            last = int(self.start[1:]) - len(self.word)
            number_range = range(int(self.start[1:]), last, -1)

            return list(map(lambda x: self.start[0] + str(x), number_range))
   