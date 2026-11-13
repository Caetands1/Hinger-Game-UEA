#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes a State class for Task 1

@author: {B26} (100464375, 100457714, 100500854, and 100501057)
@date:   27/10/2026

"""
import copy
from collections import deque

class State():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        
    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)
    
    def move(self, letter):
        VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXY" # List of all valid chars (A-Y - Capitalised)

        if isinstance(letter, str) and letter in VALID_CHARS and len(letter) == 1: # Checks the letter is a string and if its a valid char
            index = ord(letter) - ord('A')
            coords = divmod(index, 5) 
            
            if self.grid[coords[0]][coords[1]] > 0:
                self.grid[coords[0]][coords[1]] -= 1 
                return True
            else:
                return False
        else:
            return False # INVALID CHARACTER ERROR 

    def neighbours(self, cell_coords):
        r,c = cell_coords
        neighbours = []
        for row, values in enumerate(self.grid):
            for col, _ in enumerate(values):
                if max(abs(row - r), abs(col - c)) == 1:
                    neighbours.append((row, col))
        return neighbours

    def successors(self): # successors needs to take each active cell and return a new board with each possible move
        for row, values in enumerate(self.grid):
            for col, cell in enumerate(values):
                if cell > 0:
                    successor_state = State(self.grid)
                    successor_state.move(chr(ord('A') + row * 5 + col))
                    yield successor_state     

    def numRegions(self):
        region_count = 0
        CLOSED = set()
        for row, values in enumerate(self.grid):
            for col, cell in enumerate(values):
                if cell > 0 and (row,col) not in CLOSED:
                    OPEN = deque()
                    OPEN.append((row,col))
                    CLOSED.add((row,col))

                    region_count += 1
                    while OPEN:
                        u = OPEN.popleft()
                        for neighbour in self.neighbours(u):
                            if neighbour not in CLOSED and self.grid[neighbour[0]][neighbour[1]] > 0:
                                OPEN.append(neighbour)
                                CLOSED.add(neighbour)

        return region_count


    def numHingers(self):
        pass

def tester():
    sagrid = [
        [1,1,0,0,1],
        [1,1,0,0,0],
        [0,0,1,1,1],
        [0,0,0,1,1],
        [0,0,0,0,1]
    ]
    s2grid = [
        [1,1,0,0,1],
        [1,1,0,0,0],
        [0,0,1,1,1],
        [0,0,0,1,1],
        [0,0,0,0,0]
        ]
    s3grid= [
        [1,1,0,0,1],
        [1,1,0,0,0],
        [0,0,0,1,1],
        [0,0,0,1,1],
        [0,0,0,0,0]
        ]

    """
    Tests: State instance creation and tostring 
    """
    sa = State(sagrid)
    print(sa)

    """
    Tests: move() 
    - Tests to check the function is working as intended disallowing certain moves
    """
    testerState = State(sagrid)
    # Illegal Moves
    assert testerState.move("Z") is False, "Z is an illegal move"
    assert testerState.move("1") is False, "Integers are illegal moves"
    assert testerState.move("e") is False, "Lowercase chars are illegal moves"
    assert testerState.move("AE") is False, "Moves must be a single char"

    # Legal moves
    # First Y removes active cell
    assert testerState.move("Y") is True

    # Second Y should return False as the cell is now inactive
    assert testerState.move("Y") is False

    """ 
    Tests: neighbours()
    - Tests to check the function is correctly returning adjacent neighbours
    """
    testerState = State(sagrid)
    neighbours_assert_msg = "Neighbours returned an incorrect number of adjacent cells"
    assert len(testerState.neighbours((0,0))) == 3, neighbours_assert_msg
    assert len(testerState.neighbours((0,2))) == 5, neighbours_assert_msg
    assert len(testerState.neighbours((2,2))) == 8, neighbours_assert_msg 
    assert sorted(testerState.neighbours((0,0))) == [(0,1), (1,0), (1,1)], "Neighbours returned an incorrect result"

    """
    Tests: successors()
    - Tests to check successors is returning the correct number of State instances
    """
    testerState = State(sagrid)
    successors_list = list(testerState.successors())

    assert len(successors_list) == 11, "Successors returned an invalid amount of instances"
    assert testerState.grid == sagrid, "Successors manipulated the grid"

    """
    Tests: numRegions()
    - Tests to check numRegions is returning the correct amount of regions
    """

    testerState = State(sagrid)
    assert testerState.numRegions() == 2, "numRegions returned an incorrect number of regions"

    testerState = State(s2grid)
    assert testerState.numRegions() == 2, "numRegions returned an incorrect number of regions"

    testerState = State(s3grid)
    assert testerState.numRegions() == 3, "numRegions returned an incorrect number of regions"

if __name__ == "__main__" :
    tester()