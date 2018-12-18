from copy import copy
from collections import defaultdict

import locset as ls

class GameState:
    '''
    An instance represents a state of a dissembler game, i.e. stores the
    locations of the squares and their corresponding colors.
    '''
    def __init__(self, nrows, ncols, loc_to_color=defaultdict(list), 
        color_to_loc=defaultdict(set)):
        '''
        Arguments:
            nrows, ncols: number of rows, cols in board
            loc_to_color: a dict mapping locations ((x, y) tuples) to a list
            of colors (strings)
            color_to_loc: a dict mapping a color to a set of locations
        '''
        self.nrows, self.ncols = nrows, ncols
        self.loc_to_color = loc_to_color
        self.color_to_loc = color_to_loc

    def add(self, loc, color):
        '''
        Arguments:
            loc: a (x, y) tuple describing a location
            color: a string representing a valid tkinter color

        Associates 'loc' with 'color'. Note, a 'loc' can have
        multiple colors associated with it, so a 'loc' is really associated
        with a stack of color, with the topmost element being the current color.
        '''
        color_stack = self.loc_to_color[loc]

        try:
            old_color = color_stack[-1]
        except IndexError:
            pass
        else:
            self.color_to_loc[old_color].remove(loc)

        color_stack.append(color)
        self.color_to_loc[color].add(loc)

    def strip(self, loc):
        '''
        Arguments:
            loc: a (x, y) tuple describing a location

        Removes the topmost color on the stack of colors associated with loc.
        '''
        color_stack = self.loc_to_color[loc]

        if not color_stack:
            raise ValueError('Loc is empty!')

        color = color_stack.pop()
        self.color_to_loc[color].remove(loc)

        try:
            new_color = color_stack[-1]
        except IndexError:
            pass
        else:
            self.color_to_loc[new_color].add(loc)

    def swap(self, loc1, loc2):
        '''
        Arguments:
            loc1, loc2: two (x, y) tuples describing locations

        Swaps loc1 and loc2.
        '''
        assert ls.is_adjacent(loc1, loc2)

        if not self.loc_to_color[loc1] or not self.loc_to_color[loc2]:
            raise ValueError('Loc is empty!')

        color1 = self.loc_to_color[loc1][-1]
        color2 = self.loc_to_color[loc2][-1]

        self.color_to_loc[color2].remove(loc2)
        self.color_to_loc[color1].add(loc2)
        self.color_to_loc[color1].remove(loc1)
        self.color_to_loc[color2].add(loc1)

        temp = self.loc_to_color[loc1]
        self.loc_to_color[loc1] = self.loc_to_color[loc2]
        self.loc_to_color[loc2] = temp

    def any_to_remove(self):
        '''
        Returns a bool representing if there are any connected color groups.
        '''
        for color, locset in self.color_to_loc.items():
            smaller, larger = ls.filter_locset(loctset)

            if larger:
                return True

        return False

    def remove_connected_groups(self):
        '''
        Strips one color from all connected color groups covering at least 
        three squares from a board representation.
        '''

        for color, locset in self.color_to_loc.items():
            smaller, larger = ls.filter_locset(locset)

            for loc in larger:
                self.strip(loc)             

    def is_move_valid(self, loc1, loc2):
        '''
        Arguments:
            loc1, loc2: two locations

        Returns a bool representing whether swapping loc1 and loc2 is a valid 
        move.
        '''
        if not self.loc_to_color[loc1] or not self.loc_to_color[loc2]:
            return False

        if not ls.is_adjacent(loc1, loc2):
            return False

        self.swap(loc1, loc2)

        valid = new_game_state.any_to_remove()

        self.swap(loc1, loc2)

        return valid
