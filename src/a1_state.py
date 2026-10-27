"""



"""
import string

class State():
    def __init__(self, grid):
        self.grid = grid

    def __str__(self):
        return "\n".join(str(row) for row in self.grid)

    def move(self, letter):
        valid_chars = [i for i in string.ascii_uppercase] # List of all valid chars (A-Z - Capitalised)

        if type(letter) == str and letter in valid_chars: # Checks the letter is a string and if its a valid char
            index = ord(letter) - ord('A')
            coords = divmod(index, 5) 
            
            if self.grid[coords[0]][coords[1]] == 1: # Checks for an active cell
                return "valid"
            else:
                return "invalid"
        else:
            print("invalid char must be [A-Z]")
        
grid = [
    [1,1,0,0,1],
    [1,1,0,0,0],
    [0,0,1,1,1],
    [0,0,0,1,1],
    [0,0,0,0,1]
]

st = State(grid)
print(st)

print(st.move('E'))