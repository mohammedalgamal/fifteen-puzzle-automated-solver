"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value
      
    def get_index(self, number):
        """
        returns the index of a specific number
        """
        index = (-1, -1)
        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == number:
                    index = (row, col)
        return index
    
    def is_solved(self):
        """
        returns true when the puzzle is solved
        """
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if self.get_number(row, col) != (col + self.get_width() * row):
                    return False
        return True
    
    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods
    def position_tile(self, puzzle, target_row, target_col, r_string, pos):
        """
        function that returns the target tile after one move
        """
        string = ''
        target_tile = puzzle.current_position(target_row, target_col) 
        target_tuple = (target_row - target_tile[0], abs(target_col - target_tile[1]))
        string += ((target_tuple[0] * pos[2]) + (target_tuple[1] * pos[3]))      
        puzzle.update_puzzle(string)
        target_tile = puzzle.current_position(target_row, target_col)
        if pos[0] == 'u' or pos[0] == 'd':
            target = abs(target_row - target_tile[0])
        else:
            target = abs(target_col - target_tile[1]) 
        if r_string != '':
            while target != 0:
                string += r_string
                puzzle.update_puzzle(r_string)
                target_tile = puzzle.current_position(target_row, target_col)
                if pos[0] == 'u':
                    target = abs(target_row - target_tile[0])
                else:
                    target = abs(target_col - target_tile[1])
            if pos[0] == 'u':
                string += 'ld'
                puzzle.update_puzzle('ld')
                target_tile = puzzle.current_position(target_row, target_col)
        return string
    
    def position_tile2(self, puzzle, target_row, target_tile):
        """
        returns the right string for sol_col0
        """
        string = ''
        string += ('u' * abs((target_row - 1) - target_tile[0]))
        puzzle.update_puzzle('u' * abs((target_row - 1) - target_tile[0]))
        target_tile = puzzle.current_position(target_row, 0)
        while target_tile[0] != target_row - 1:
            string += 'lddru'
            puzzle.update_puzzle('lddru')
            target_tile = puzzle.current_position(target_row, 0)
        string += 'ld'
        puzzle.update_puzzle('ld')
        target_tile = puzzle.current_position(target_row, 0)
        return string        

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(target_row, target_col) != 0:
            return False
        for row in range(target_row + 1, self.get_height()):
            for col in range(self.get_width()):
                if self.get_number(row, col) != (col + self.get_width() * row):
                    return False
        for col in range(target_col + 1, self.get_width()):
            if self.get_number(target_row, col) != (col + self.get_width() * target_row):
                return False
        return True
                

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        string = ''
        puzzle = self.clone()
        assert puzzle.lower_row_invariant(target_row, target_col)
        target_tile = puzzle.current_position(target_row, target_col)
        if target_col - target_tile[1] == 0:
             string = self.position_tile(puzzle, target_row, target_col, 'lddru', ('u', 'l', 'u', 'l'))
        elif target_row - target_tile[0] == 0:
            string = self.position_tile(puzzle, target_row, target_col, 'urrdl', ('l', 'u', 'u', 'l'))
        elif target_row > target_tile[0] and target_col > target_tile[1]:
            mul1 = abs(self.get_index(0)[0] - target_tile[0])
            mul2 = abs(self.get_index(0)[1] - target_tile[1])
            string += (mul1 * 'u' + mul2 * 'l')
            puzzle.update_puzzle(mul1 * 'u' + mul2 * 'l')
            target_tile = puzzle.current_position(target_row, target_col)
            while target_tile[1] != target_col:
                string += 'drrul'
                puzzle.update_puzzle('drrul')
                target_tile = puzzle.current_position(target_row, target_col)
            string += (mul1 * 'd' + 'r')
            puzzle.update_puzzle(mul1 * 'd' + 'r')
            target_tile = puzzle.current_position(target_row, target_col)                
            string += self.position_tile(puzzle, target_row, target_col, 'lddru', ('u', 'l', 'u', 'l'))
        else:
            mul1 = abs(self.get_index(0)[0] - target_tile[0])
            mul2 = abs(self.get_index(0)[1] - target_tile[1])
            string += (mul1 * 'u' + mul2 * 'r')
            puzzle.update_puzzle(mul1 * 'u' + mul2 * 'r')
            target_tile = puzzle.current_position(target_row, target_col)
            while target_tile[1] != target_col:
                string += 'ulldr'
                puzzle.update_puzzle('ulldr')
                target_tile = puzzle.current_position(target_row, target_col)  
            string += ('dl' + (mul1 - 1) * 'd')
            puzzle.update_puzzle('dl' + (mul1 - 1) * 'd')            
            target_tile = puzzle.current_position(target_row, target_col)  
            string += self.position_tile(puzzle, target_row, target_col, 'lddru', ('u', 'l', 'u', 'l'))
        self.update_puzzle(string)
        #assert self.lower_row_invariant(target_row, target_col - 1)        
        return string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        puzzle = self.clone()
        string = ''
        target_tile = self.current_position(target_row, 0) 
        assert self.lower_row_invariant(target_row, 0)
        string += 'ur'
        puzzle.update_puzzle('ur')
        target_tile = puzzle.current_position(target_row, 0) 
        if target_tile != (target_row, 0):
            if target_tile[0] == puzzle.get_index(0)[0]:
                if target_tile[1] == 0:
                    string += 'l'
                    puzzle.update_puzzle('l')
                else:
                    itr = abs(target_tile[1] - puzzle.get_index(0)[1])
                    string += ('r' * (abs(target_tile[1] - puzzle.get_index(0)[1])))
                    puzzle.update_puzzle('r' * (abs(target_tile[1] - puzzle.get_index(0)[1])))
                    target_tile = puzzle.current_position(target_row, 0)
                    for dummy in range(itr):
                        string += "ulldr"
                        puzzle.update_puzzle('ulldr')
                        target_tile = puzzle.current_position(target_row, 0)
                    string += "l"
                    puzzle.update_puzzle('l')
            elif target_tile[1] == 1:
                string += self.position_tile2(puzzle, target_row, target_tile)
            elif target_tile[1] < 1:
                string += ('u' * abs(target_tile[0] - (target_row - 1)) + 'l' + 'd' * abs(target_tile[0] - (target_row - 1)) + 'r')
                puzzle.update_puzzle('u' * abs(target_tile[0] - (target_row - 1)) + 'l' + 'd' * abs(target_tile[0] - (target_row - 1)) + 'r')
                target_tile = puzzle.current_position(target_row, 0)
                string += self.position_tile2(puzzle, target_row, target_tile)
            else:
                string += ('u' * abs(target_tile[0] - (target_row - 1)) + 'r' * abs(target_tile[1] - 1))
                puzzle.update_puzzle('u' * abs(target_tile[0] - (target_row - 1)) + 'r' * abs(target_tile[1] - 1))
                target_tile = puzzle.current_position(target_row, 0)
                while target_tile[1] != 1:
                    string += 'dllur'
                    puzzle.update_puzzle('dllur')
                    target_tile = puzzle.current_position(target_row, 0)
                string += ('d' * abs(target_tile[0] - (target_row - 1)) + 'l')
                puzzle.update_puzzle('d' * abs(target_tile[0] - (target_row - 1)) + 'l')
                target_tile = puzzle.current_position(target_row, 0)
                added =  self.position_tile2(puzzle, target_row, target_tile)
                string += added
            string += "ruldrdlurdluurddlur"
            puzzle.update_puzzle("ruldrdlurdluurddlur")
        string += ('r' * abs(self.get_width() - 2))
        puzzle.update_puzzle('r' * abs(self.get_width() - 2))
        self.update_puzzle(string)
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)
        return string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 0
        if self.get_number(target_row, target_col) != 0:
            return False
        for row in range(target_row + 2, self.get_height()):
            for col in range(self.get_width()):
                if self.get_number(row, col) != (col + self.get_width() * row):
                    return False
        for col in range(target_col, self.get_width()):
            if self.get_number(target_row + 1, col) != (col + self.get_width()):
                return False
            if col != target_col:
                if self.get_number(target_row, col) != (col + self.get_width() * target_row):
                    return False
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 1
        if self.lower_row_invariant(target_row, target_col) == False:
            return False
        for idx in range(target_col + 1, self.get_width()):
            if self.current_position(0, idx) !=  self.get_index(idx):
                return False
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        string = ''
        puzzle = self.clone()
        string += 'ld'
        puzzle.update_puzzle('ld')
        target_tile = puzzle.current_position(0, target_col)
        if target_tile != (0, target_col):
            if target_tile[0] == 1:
                mul = abs(target_tile[1] - puzzle.get_index(0)[1])
                string += (mul * 'l')
                puzzle.update_puzzle(mul * 'l')
                target_tile = puzzle.current_position(0, target_col)
                while puzzle.get_index(target_col) != (1, target_col - 1):
                    string += 'urrdl'
                    puzzle.update_puzzle('urrdl')
                    target_tile = puzzle.current_position(0, target_col)
            elif target_tile[1] == puzzle.get_index(0)[1]:
                string += 'uld'
                puzzle.update_puzzle('uld')
                target_tile = puzzle.current_position(0, target_col)                
            else:
                mul = abs(target_tile[1] - puzzle.get_index(0)[1])
                string += ('l' * mul + 'urdl')
                puzzle.update_puzzle('l' * mul + 'urdl')
                target_tile = puzzle.current_position(0, target_col)
                while puzzle.get_index(target_col) != (1, target_col - 1):
                    string += 'urrdl'
                    puzzle.update_puzzle('urrdl')
                    target_tile = puzzle.current_position(0, target_col)
            string += "urdlurrdluldrruld"
            puzzle.update_puzzle("urdlurrdluldrruld")
        self.update_puzzle(string)
        assert self.row1_invariant(target_col - 1)
        return string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        string = ''
        puzzle = self.clone()
        target_tile = self.current_position(1, target_col)
        assert self.row1_invariant(target_col)
        if target_tile[1] == target_col:
            string += 'u'
            puzzle.update_puzzle('u')
        elif target_tile[0] == 1:
            mul = abs(self.get_index(0)[1] - self.current_position(1, target_col)[1])
            string += ('l' * mul)
            puzzle.update_puzzle('l' * mul)
            target_tile = puzzle.current_position(1, target_col)
            while target_tile[1] != target_col:
                string += 'urrdl'
                puzzle.update_puzzle('urrdl')
                target_tile = puzzle.current_position(1, target_col)
            string += 'ur'
            puzzle.update_puzzle('ur')
        else:
            mul1 = abs(self.get_index(0)[1] - self.current_position(1, target_col)[1])
            string += (mul1 * 'l' + 'u' + mul1 * 'r' + 'd')
            puzzle.update_puzzle(mul1 * 'l' + 'u' + mul1 * 'r' + 'd')
            string += ('l' * mul1)
            puzzle.update_puzzle('l' * mul1)
            target_tile = puzzle.current_position(1, target_col)
            while target_tile[1] != target_col:
                string += 'urrdl'
                puzzle.update_puzzle('urrdl')
                target_tile = puzzle.current_position(1, target_col)
            string += 'ur'
            puzzle.update_puzzle('ur')
        self.update_puzzle(string)    
        assert self.row0_invariant(target_col)    
        return string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        puzzle = self.clone()
        string = ''
        mul = puzzle.get_index(0)
        string += ('l' * mul[0] + 'u' * mul [1])
        puzzle.update_puzzle('l' * mul[0] + 'u' * mul [1])
        for dummy in range(4):
            string += 'rdlu'
            puzzle.update_puzzle('rdlu')
            if puzzle.is_solved():
                self.update_puzzle(string)
                return string
        for dummy in range(4):
            string += 'drul'
            puzzle.update_puzzle('drul')
            if puzzle.is_solved():
                self.update_puzzle(string)
                return string              
        return string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        string = ''
        puzzle = self.clone()
        mul1 = abs((self.get_height() - 1) - self.get_index(0)[0])
        mul2 = abs((self.get_width() - 1) - self.get_index(0)[1])
        string += ('r' * mul2 + 'd' * mul1)
        puzzle.update_puzzle(string)
        row_num = self.get_height() - 1
        col_num = self.get_width() - 1
        while row_num > 1:
            if col_num > 0:
                temp_str = puzzle.solve_interior_tile(row_num, col_num)
                string += temp_str
                col_num -= 1
            else:
                temp_str = puzzle.solve_col0_tile(row_num)
                string += temp_str
                col_num =  self.get_width() - 1
                row_num -= 1
        col_num1 = self.get_width() - 1
        while col_num1 > 1:
            temp_str = puzzle.solve_row1_tile(col_num1)
            string += temp_str
            temp_str1 = puzzle.solve_row0_tile(col_num1)
            string += temp_str1
            col_num1 -= 1
        temp_str = puzzle.solve_2x2()
        string += temp_str
        self.update_puzzle(string)
        return string

# Start interactive simulation
#puzzle_1 = Puzzle(4, 4)
#poc_fifteen_gui.FifteenGUI(puzzle_1)


