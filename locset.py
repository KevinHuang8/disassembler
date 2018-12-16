# Name: Kevin Huang
#CMS login: khuang
'''
The CS 1 final exam, Fall 2018, part 1.

Functions on locations and sets of locations.
'''

import string
from copy import copy
from functools import reduce
from utils import *

def is_adjacent(loc1, loc2):
    '''
    Arguments:
      loc1, loc2 -- (row, column) locations

    Return value: 
      True if two locations are orthogonally adjacent, otherwise False.
    '''

    assert is_loc(loc1)
    assert is_loc(loc2)

    if loc1[0] == loc2[0]:
        return abs(loc1[1] - loc2[1]) == 1
    elif loc1[1] == loc2[1]:
        return abs(loc1[0] - loc2[0]) == 1
    return False

def adjacent_to_any(loc, locset):
    '''
    Arguments:
      loc -- a (row, column) location
      locset -- a set of locations

    Return value:
      True if `loc` is not in `locset` and at least one location 
      in `locset` is adjacent to `loc`, otherwise False.

    The set `locset` is not altered.
    '''

    assert is_loc(loc)
    assert is_locset(locset)

    if loc in locset:
        return False

    for l in locset:
        if is_adjacent(loc, l):
            return True

    return False

def collect_adjacent(locset, target_set):
    '''
    Arguments:
      locset -- a set of (row, column) locations
      target_set -- another set of (row, column) locations

    Return value: 
      A set of all the locations in `locset` that are adjacent 
      to any location in `target_set`.

    The sets `locset` and `target_set` are not altered.
    '''

    assert is_locset(locset)
    assert is_locset(target_set)

    s = set()

    for loc in locset:
        if adjacent_to_any(loc, target_set) and loc not in target_set:
            s.add(loc)

    return s

def collect_connected(loc, locset):
    '''
    Arguments:
      loc -- a (row, column) location
      locset -- a set of locations

    Return value: 
      A set of all the locations in `locset` which are connected to `loc` 
      via a chain of adjacent locations. Include `loc` in the resulting set.

    The set `locset` is not altered.
    '''

    assert is_loc(loc)
    assert is_locset(locset)

    s = {loc}
    adj = collect_adjacent(locset, s)

    for l in adj:
        if l not in s:
            s = s.union(collect_connected(l, locset - s))

    return s

def partition_connected(locset):
    '''
    Partition a set of locations based on being connected via a chain of
    adjacent locations.  The original locset is not altered.
    Return a list of subsets.  The subsets must all be disjoint i.e.
    the intersection of any two subsets must be the empty set.

    Arguments:
      locset -- a set of (row, column) locations

    Return value: 
      The list of partitioned subsets.

    The set `locset` is not altered.
    '''

    assert is_locset(locset)

    partition = []
    locset2 = copy(locset)

    while locset2:
        loc = locset2.pop()
        connected = collect_connected(loc, locset)
        partition.append(connected)
        locset2 -= connected

    return partition

def filter_locset(locset):
    '''
    Given a locset, partition it into subsets which are connected via a
    chain of adjacent locations.  Compute two sets:
      -- the union of all partitions whose length is < 3 
      -- the union of all partitions whose length is >= 3 
    and return them as a tuple of two sets (in that order).  

    Arguments:
      locset -- a set of (row, column) locations

    Return value:
      The two sets as described above.

    The set `locset` is not altered.
    '''

    assert is_locset(locset)

    partition = partition_connected(locset)

    larger = list(filter(lambda connected: len(connected) >= 3, partition))
    if larger:
        larger = set.union(*larger)
    else:
        larger = set()
    smaller = locset - larger

    return smaller, larger


