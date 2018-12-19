from collections import defaultdict, deque

from utils import is_loc
import locset as ls

class GameState:
    '''
    An instance represents a state of a dissembler game, i.e. stores the
    locations of the squares and their corresponding colors.
    '''
    def __init__(self):
        '''
        Fields:
            loc_to_color: a dict mapping locations ((x, y) tuples) to a deque
            of colors (strings)
            color_to_loc: a dict mapping a color to a set of locations
            maxrow, maxcol: highest row and column indicies
            minrow, mincol: lowest row and column indicies
        '''
        self.maxrow, self.maxcol = 0, 0
        self.minrow, self.mincol = 4e9, 4e9
        self.loc_to_color = defaultdict(deque)
        self.color_to_loc = defaultdict(set)

    def add(self, loc, color):
        '''
        Arguments:
            loc: a (x, y) tuple describing a location
            color: a string representing a valid tkinter color

        Associates 'loc' with 'color'. Note, a 'loc' can have
        multiple colors associated with it, so a 'loc' is really associated
        with a stack of color, with the topmost element being the current color.
        '''
        assert is_loc(loc)
        assert type(color) is str

        color_queue = self.loc_to_color[loc]

        if not color_queue:
            self.color_to_loc[color].add(loc)

        color_queue.append(color)


        if loc[0] > self.maxrow:
            self.maxrow = loc[0]
        if loc[1] > self.maxcol:
            self.maxcol = loc[1]
        if loc[0] < self.minrow:
            self.minrow = loc[0]
        if loc[1] < self.mincol:
            self.mincol = loc[0]

    def strip(self, loc):
        '''
        Arguments:
            loc: a (x, y) tuple describing a location

        Removes the topmost color on the queue of colors associated with loc.
        '''
        color_queue = self.loc_to_color[loc]

        if not color_queue:
            raise ValueError('Loc is empty!')

        color = color_queue.popleft()
        self.color_to_loc[color].remove(loc)

        try:
            new_color = color_queue[0]
        except IndexError:
            # loc is now empty, may have to resize playing area
            pass
        else:
            self.color_to_loc[new_color].add(loc)

    def swap(self, loc1, loc2):
        '''
        Arguments:
            loc1, loc2: two (x, y) tuples describing locations. Must be adjacent

        Swaps loc1 and loc2.
        '''
        assert ls.is_adjacent(loc1, loc2)

        if not self.loc_to_color[loc1] or not self.loc_to_color[loc2]:
            raise ValueError('Loc is empty!')

        color1 = self.loc_to_color[loc1][0]
        color2 = self.loc_to_color[loc2][0]

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
            smaller, larger = ls.filter_locset(locset)

            if larger:
                return True

        return False

    def remove_connected_groups(self):
        '''
        Strips one color from all connected color groups covering at least 
        three squares from a board representation.

        Returns a set of affected locations.
        '''
        removed = set()

        for color, locset in self.color_to_loc.items():
            smaller, larger = ls.filter_locset(locset)

            for loc in larger:
                self.strip(loc)
                removed.add(loc)

        return removed             

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

        return self._removes_any(loc1, loc2)

    def _removes_any(self, loc1, loc2):
        '''
        Arguments:
            loc1, loc2: two locations

        Returns whether swapping loc1 or loc2 would result in any squares
        being removed. Assumes loc1 and loc2 are adjacent.
        '''

        self.swap(loc1, loc2)

        valid = self.any_to_remove()

        self.swap(loc1, loc2)

        return valid


    def make_move(self, loc1, loc2):
        '''
        Arguments:
            loc1, loc2: two locations

        Executes swapping loc1 and loc2 and resolves events that occur after.
        Returns a locset of locations that have been stripped.
        '''
        assert is_loc(loc1)
        assert is_loc(loc2)

        if not self.is_move_valid(loc1, loc2):
            raise ValueError('Invalid move!')

        self.swap(loc1, loc2)
        return self.remove_connected_groups()

    def nrows(self):
        '''
        Returns total number of rows containing non-empty locations.
        '''
        return self.maxrow - self.minrow + 1

    def ncols(self):
        '''
        Returns total number of cols containing non-empty locations.
        '''
        return self.maxcol - self.mincol + 1

    def __getitem__(self, key):
        if self.loc_to_color[key]:
            return self.loc_to_color[key]
        elif self.color_to_loc[key]:
            return self.color_to_loc[key]
        else:
            raise KeyError(f'{key} not found')

    def __iter__(self):
        return iter(self.loc_to_color)

    def __bool__(self):
        for color_queue in self.loc_to_color.values():
            if color_queue:
                return True
        return False

    def __str__(self):
        return str(self.loc_to_color)

class A:
    def __init__(self):
        self.game_state = GameState()

        self.game_state.add((0, 0), 'red')
        self.game_state.add((1, 1), 'red')
        self.game_state.add((1, 0), 'blue')
        self.game_state.add((4, 4), 'green')
        self.game_state.add((2, 3), 'blue')
        self.game_state.add((1, 1), 'blue')
        self.game_state.add((1, 1), 'green')
        self.game_state.add((2, 0), 'red')

if __name__ == '__main__':
    a = A()
    gs = a.game_state

    print(gs.loc_to_color)
    print(gs.color_to_loc)

    print(gs.is_move_valid((0, 0), (1, 0)))
