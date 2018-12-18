'''
The CS 1 final exam, Fall 2018.
Helper functions.  Supplied to students.
'''

import string

# ---------------------------------------------------------------------- 
# Global data.
# ---------------------------------------------------------------------- 

# A list of dissembler puzzles.
# Each puzzle is represented as a single string.
# Blank squares are indicated by '.' and colored squares
# are indicated by a single lowercase letter.
# The letters have no meaning (they aren't short for a specific color).
# The blanks in the string are used to separate different rows of the
# puzzle.

puzzles = [
  'aababb',
  'aa. b.. abb',
  'a.. aba bab ..b',
  'abba a..b b..a abba',
  '.aa. ..b. baab .b.. .aa.',

  'a...a babab a...a',
  '....a ababa b.... a.aba b.a.b a...a babab',
  'aabb .ba. .ac. .cd. ccdc',
  'ababc d...b ad.ec .f.e. fd.eg f...e hhghg',
  'aabaa bbcbb ccdcc ddedd eeaee',

  '.aabb. .c..c. ca..ba d....d cdccdc .cddc.',
  '..aab .ccda .b.cb db.db da.d. cbaa. dcc..',
  'abbcbc adaddc dccbcb dadaab',
  'ababb b.b.a a.a.a a.b.b bbaba',
  '.ab. .ba. .ab. abab a..b',

  # Harder puzzles:

  '...a... ..bac.. .bdbad. cca.dee .afbeb. ..afb.. ...f...',
  'aaaaab cbdcdb cbeadb cabfeb cafefb cddddd',
  'abcdded adb.ecd abcccad afggged agf.bad afbbgad',
  'abcacc daedfe dbgfef ccbhhi gjcijh gfjffi',
  'aabcbcb c.a.d.b cbcdcaa d.a.a.b adcabda d.b.d.b acadcdd'
]

# ---------------------------------------------------------------------- 
# Functions.
# ---------------------------------------------------------------------- 

def is_loc(loc):
    '''
    Arguments:
      loc -- a location

    Return value: True if `loc` is a valid (row, column) location,
      otherwise False.

    NOTE: This doesn't take into account board dimensions.
    '''

    if type(loc) is not tuple:
        return False
    if len(loc) != 2:
        return False
    if type(loc[0]) is int and type(loc[1]) is int:
        if loc[0] >= 0 and loc[1] >= 0:
            return True
    return False

def is_locset(locset):
    '''
    Arguments:
      locset -- a set of locations
    
    Return value: True if `locset` is a set and contains only `loc`s,
      otherwise False.
    '''

    if type(locset) is not set:
        return False

    for item in locset:
        if not is_loc(item):
            return False

    return True

def display_locset(locset, nrows, ncols):
    '''
    Print the contents of a locset.
    The set will be represented as a grid with `nrows` rows and `ncols` columns.
    Each element in the grid is either '.' if the location is not in `locset`
    or 'X' if it is.
    The row indices of the locset must be between 0 and (nrows - 1) and 
    the column indices must be between 0 and (ncols - 1).  
    The set `locset` is not altered.

    Arguments:
      locset -- a set of locations
      nrows -- the number of rows on the board
      ncols -- the number of columns on the board

    Return value: none
    '''

    assert is_locset(locset)
    for (r, c) in locset:
        assert 0 <= r and r < nrows  # OR: 0 <= r < nrows
        assert 0 <= c and c < ncols  # OR: 0 <= c < ncols

    s = ''
    for r in range(nrows):
        for c in range(ncols):
            if (r, c) in locset:
                s += 'X'
            else:
                s += '.'
        s += '\n'
    print(s, end='')

def disjoint_subsets(list_of_sets):
    '''
    Arguments:
      list_of_sets -- a list of sets

    Return value: 
        True if all sets are non-overlapping (disjoint) 
        i.e. if their pairwise intersections are all empty;
        otherwise False.

    The list of sets is not altered.
    '''

    assert type(list_of_sets) is list
    for item in list_of_sets:
        assert type(item) is set

    # If the subsets are disjoint, the union will have the same 
    # cardinality (AKA size, length) as the sum of the 
    # cardinalities of the component sets.

    union = set().union(*list_of_sets)
    return (len(union) == sum(map(len, list_of_sets)))

def is_rep(rep):
    '''
    Validate the internal representation of a puzzle.
    Puzzles are represented as a dictionary mapping
    locations to one-character strings, where the character
    is a lowercase letter.

    Arguments:
      rep -- the puzzle representation

    Return value:
      True if the representation is valid, otherwise False.
    '''

    for loc in rep:
        if not is_loc(loc):
            return False
        color = rep[loc]
        if type(color) is not str:
            return False
        if color not in string.ascii_lowercase:
            return False
    return True

def is_inverted_rep(rep):
    '''
    Arguments:
      rep -- the inverted puzzle representation

    Return value:
      True if the inverted representation is valid, otherwise False.
    '''

    for color in rep:
        if color not in string.ascii_lowercase:
            return False
        locs = rep[color]
        if type(locs) is not set:
            return False
        for loc in locs:
            if not is_loc(loc):
                return False
    return True

def is_move(move):
    '''
    Return `True` if `move` is a valid move i.e. a pair of
    valid locations.

    Arguments:
      move -- the move

    Return value:
      True if the move is valid, otherwise False.
    '''

    return (type(move) is tuple and len(move) == 2 and \
            is_loc(move[0]) and is_loc(move[1]))

