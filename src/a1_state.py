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

class State():
    def __init__(self, grid):
        self.grid = copy.deepcopy(grid)
        
    def __str__(self):
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)
    
    def move(self, letter):
        valid_chars = "ABCDEFGHIJKLMNOPQRSTUVWXY" # List of all valid chars (A-Y - Capitalised)

        if isinstance(letter, str) and letter in valid_chars and len(letter) == 1: # Checks the letter is a string and if its a valid char
            index = ord(letter) - ord('A')
            coords = divmod(index, 5) 
            
            if self.grid[coords[0]][coords[1]] > 0: # Checks for an active cell
                self.grid[coords[0]][coords[1]] -= 1
                return True
            else:
                return False
        else:
            return False # INVALID CHARACTER ERROR 

    def successors(self): # successors needs to take each active cell and return a new board with each possible move
        for row, values in enumerate(self.grid):
            for col, cell in enumerate(values):
                if cell > 0:
                    successor_state = State(self.grid)
                    successor_state.move(chr(ord('A') + row * 5 + col))
                    yield successor_state     

        
def tester():
    grid = [
        [1,1,0,0,1],
        [1,1,0,0,0],
        [0,0,1,1,1],
        [0,0,0,1,1],
        [0,0,0,0,1]
    ]
  
    sa = State(grid)
    print(sa)
    # Test cases - regular interaction (returns True/False depending on cell state)
    print(sa.move("Y"))
    print(sa.move("A"))
    print(sa.move("H"))
    # Test cases - error interactions (expecting False returns)
    print(sa.move("e"))
    print(sa.move("AB"))
    print(sa.move(5))
    print(sa)
    # test game loop
    """
    user_input = input("Enter a letter [A-Z]: ")
    while user_input:
        print(sa.move(user_input))
        print(sa)

        user_input = input("Enter a letter [A-Z]: ")
    """
    neighbours_assert_msg = "Neighbours returned an incorrect number of adjacent cells"
    assert len(s1.neighbours((0,0))) == 3, neighbours_assert_msg
    assert len(s1.neighbours((0,2))) == 5, neighbours_assert_msg
    assert len(s1.neighbours((2,2))) == 8, neighbours_assert_msg 

    """
    Tests: successors()
    - Tests to check successors is returning the correct number of State instances
    """
    successors_list = []
    for i in s1.successors():
        successors_list.append(i)

    assert len(successors_list) == 11, "Successors returned an invalid amount of instances"

if __name__ == "__main__" :
    tester()