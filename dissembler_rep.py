# Name: Kevin Huang
#CMS login: khuang
'''
The CS 1 final exam, Fall 2018, part 2.

The Dissembler puzzle game.
'''

from utils import *
from copy import copy
import locset as ls

# ---------------------------------------------------------------------- 
# Functions on board representations.
# ---------------------------------------------------------------------- 

def invert_rep(rep):
    '''
    Invert the board representation which maps locations to colors.
    The inverted representation will map colors to sets of locations.

    Arguments:
      rep -- a dictionary mapping locations to one-character strings
             representing colors

    Return value:
      a dictionary mapping one-character strings (representing colors)
      to sets of locations

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)

    inverse_rep = {}

    for loc, color in rep.items():
        try:
            inverse_rep[color].add(loc)
        except KeyError:
            inverse_rep[color] = {loc}

    return inverse_rep

def revert_rep(inverted):
    '''
    Invert the board representation which maps colors to sets of 
    locations.  The new representation will map locations to colors.

    Arguments:
      inverted -- a dictionary mapping one-character strings 
                  (representing colors) to sets of locations

    Return value:
      a dictionary mapping locations to one-character strings
      representing colors

    The input dictionary 'inverted' is not altered.
    '''

    assert is_inverted_rep(inverted)

    rep = {}

    for color, locset in inverted.items():
        for loc in locset:
            rep[loc] = color

    return rep

def swap_locations(rep, loc1, loc2):
    '''
    Exchange the contents of two locations.

    Arguments:
      rep -- a dictionary mapping locations to one-character strings
             representing colors
      loc1, loc2 -- adjacent locations which are in the board rep

    Return value:
      a new dictionary with the same structure of 'rep' with the
      specified locations having each others' contents

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)
    assert is_loc(loc1)
    assert is_loc(loc2)
    assert ls.is_adjacent(loc1, loc2)
    assert loc1 in rep
    assert loc2 in rep

    rep2 = copy(rep)

    temp = rep2[loc1]
    rep2[loc1] = rep2[loc2]
    rep2[loc2] = temp

    return rep2

def remove_connected_groups(rep):
    '''
    Remove all connected color groups covering at least three squares
    from a board representation.

    Arguments: 
      rep -- a dictionary mapping locations to one-character strings
             representing colors

    Return value:
      a tuple of two dictionaries of the same kind as the input
      (i.e. a mapping between locations and color strings);
      the first contains the remaining locations only, 
      and the second contains the removed locations only 

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)

    inverted = invert_rep(rep)
    remaining, removed = {}, {}

    for color, locset in inverted.items():
        smaller, larger = ls.filter_locset(locset)

        for loc in larger:
            removed[loc] = rep[loc]
        for loc in smaller:
            remaining[loc] = rep[loc]

    return remaining, removed

def adjacent_moves(nrows, ncols):
    '''
    Create and return a set of all moves on a board with 'nrows' rows and
    'ncols' columns.  The moves consist of two adjacent (row, column)
    locations.

    Arguments:
      nrows -- the number of rows on the board
      ncols -- the number of columns on the board

    Return value:
      the set of moves, where each move is a pair of adjacent locations
      and each location is a (row, column) pair; also the two locations
      are ordered in the tuple (the "smallest" comes first)

    Note that the moves are independent of the contents of any board
    representation; we aren't considering whether the moves would actually 
    change anything on a board or whether the locations of each move are 
    occupied by color squares.
    '''

    assert type(nrows) is int and type(ncols) is int
    assert nrows > 0 and ncols > 0

    adjacent = set()

    def in_board(row, col):
        return row < nrows and col < ncols and row >= 0 and col >= 0

    for r in range(nrows):
        for c in range(ncols):
            adj_loc = [(r, c + 1), (r + 1, c)]
            for loc in adj_loc:
                if in_board(*loc):
                    adjacent.add(((r, c), loc))

    return adjacent
            

def possible_moves(rep, nrows, ncols):
    '''
    Compute and return a set of all the possible moves.  A "possible move"
    is a move where:
    -- both locations of the move are adjacent
    -- both locations on the board rep are occupied by colors 
    -- making the move will cause some locations to be vacated

    Arguments: 
      rep -- a dictionary mapping locations to one-character strings
             representing colors
      nrows -- the number of rows on the board
      ncols -- the number of columns on the board

    Return value: 
      the set of possible moves

    The input dictionary 'rep' is not altered.
    '''

    assert is_rep(rep)
    assert type(nrows) is int and type(ncols) is int
    assert nrows > 0 and ncols > 0

    possible = set()
    adjacent = adjacent_moves(nrows, ncols)

    for loc1, loc2 in adjacent:
        if loc1 not in rep or loc2 not in rep:
            continue

        swap_rep = swap_locations(rep, loc1, loc2)
        remaining, removed = remove_connected_groups(swap_rep)

        if not removed:
            continue

        possible.add((loc1, loc2))

    return possible
