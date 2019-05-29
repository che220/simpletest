"""
Question:

board (tens of letters):

# D O G
# A B C
# E E Z

Note: letters can repeat

billions of words:
Test words against the board:

1. no position can be repeated (letters can be repeated)
2. letters must be adjcent to each other
"""
import copy

rows = 3
cols = 3
board_letters = {'D' : [0],
                 'O' : [1],
                 'G' : [2],
                 'A' : [3],
                 'B' : [4],
                 'C' : [5],
                 'E' : [6, 7],
                 'Z' : [8]
                 }

class CharList:
    def __init__(self, pos):
        self.occupied = {pos}
        self.last_pos = get_coodinates(pos)

    def add(self, pos):
        self.occupied.add(pos)
        self.last_pos = get_coodinates(pos)

    def is_valid_pos(self, new_pos):
        if new_pos in self.occupied:
            return False

        r, c = get_coodinates(new_pos)
        r_diff = abs(self.last_pos[0] - r)
        c_diff = abs(self.last_pos[1] - c)
        return not (r_diff > 1 or c_diff > 1)


def get_coodinates(num):
    # convert number to coodinates in the board
    r = num // rows
    c = num % rows
    return r, c


def valid_word(word):
    # check if any letter does not exist in board
    chars = set(word)
    for c in chars:
        if c not in board_letters:
            return False

    # all letters in word are in the board
    char_lists = []
    first_letter = True
    for c in word:
        positions = board_letters[c]
        updated_idxs = []
        for pos in positions:
            if first_letter:
                char_lists.append(CharList(pos))
                updated_idxs.append(len(char_lists) - 1)
            else:
                # do not have to include newly created trees here
                # we will use them for the next letter
                for i in range(len(char_lists)):
                    cs = char_lists[i]
                    if cs.is_valid_pos(pos):
                        if i in updated_idxs:
                            # if multiple positions are adjacent to last letter
                            # we need a new tree to keep track of the word
                            new_cs = copy.copy(cs)
                            new_cs.add(pos)
                            char_lists.append(new_cs)
                            updated_idxs.append(len(char_lists)-1)
                        else:
                            cs.add(pos)
                            updated_idxs.append(i)

        # remove char trees that are not updated. Those trees are invalid
        if not first_letter:
            char_lists = [char_lists[i] for i in updated_idxs]
            if not char_lists:
                break
        else:
            first_letter = False

    # if char_lists is not empty, it is a valid word
    return bool(char_lists)


if __name__ == '__main__':
    words = ['APPLE', 'DBZE', 'DBZEB', 'DBZEEE', 'GATE', 'DAEBG']
    for w in words:
        if valid_word(w):
            print(w)
