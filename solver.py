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
    # Helper function
    
    def position_tile(self, num_row, num_col):
        """
        Moves the tile that is supposed to be at (num_row, num_col) 
        to the zero tile position and moves the zero tile to the left of it
        """
        # Solution vars
        sol = ''
        temp = ''
        
        # Target 
        target_pos = self.current_position(0, 0)
        tile_pos = self.current_position(num_row, num_col)

        # Return if tile is in the right position
        if target_pos[0] == tile_pos[0] and target_pos[1] == tile_pos[1] - 1:
            return sol
        
        # Calculate the difference between traget_pos and current_pos
        diff_row = target_pos[0] - tile_pos[0]
        diff_col = target_pos[1] - tile_pos[1]                
            
        # Position indices
        right = int(diff_col < 0 and diff_row == 0)
        left = int(diff_col > 0 and diff_row == 0)
        up_tile = int(diff_col == 0 and diff_row > 0)
        up_right = int(diff_col < 0 and diff_row > 1)
        straight_up_right = int(diff_col < 0 and diff_row == 1 and tile_pos[0] != 0)
        tight_up_right = int(diff_col < 0 and diff_row == 1 and tile_pos[0] == 0)
        up_left = int(diff_col > 0 and diff_row > 1)
        straight_up_left = int(diff_col > 0 and diff_row == 1 and tile_pos[0] != 0)
        tight_up_left = int(diff_col > 0 and diff_row == 1 and tile_pos[0] == 0)
        
        # Move the zero tile to target tile
        temp = 'u' * int(diff_row != 0) + 'l' * diff_col + 'r' * (-diff_col) + 'u' * (diff_row - 1) 
        sol += temp
        self.update_puzzle(temp)            

        # Check if not to the UPPER LEFT of the zero tile and not in the first col
        if not (self.current_position(num_row, num_col)[1] == 0 and diff_row > 0):
            temp = (('lddru' * (diff_row - 1) + 'ld') * up_tile +					# Controls if tile is up
                   ('urrdl' * (diff_col - 1)) * left +								# Controls if tile is left
                   ('ulldr' * (-diff_col))[: -1] * right +							# Controls if tile is right
                   ('ld' + ('rulld' * (-diff_col))[: -2] +
                   ('lddru' * (diff_row))[: -3]) * up_right +						# Controls if tile is up right 
                   (('ulldr' * (-diff_col))[: -1] + 'druld') * straight_up_right + 	# Controls if tile is up right by one row
                   ('lddru' * (diff_row - 1) + 
                   ('urrdl' * (diff_col))[2:]) * up_left + 							# Controls if tile is up left
                   ('urrdl' * (diff_col - 1) + 'druld') * straight_up_left +		# Controls if tile is up left by one row
                   (('dllur' * (-diff_col))[: -3] + 'uld') * tight_up_right +		# Controls if tile is up right by one row in the first row
                   (('drrul' * (diff_col))[: -3] + 'uld') * tight_up_left)			# Controls if tile is up left by one row in the first row

            sol += temp
            self.update_puzzle(temp)
            
        # Controls if tile is to UPPER LEFT of the zero tile AND in the first coulmn
        else:
            temp = ('rddlu' * (diff_row - 1) + 'rd'
                    + 'lurrd' * (diff_col - 1) + 'l')

            sol += temp
            self.update_puzzle(temp)        

        return sol
    
    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # Check if zero tile is at the position mentioned
        if self.get_number(target_row, target_col) != 0:
            return False
        
        # Check that all tiles in rows i+1 or below are positioned at their solved location.
        for row in range(target_row + 1, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False
            
        # Check that all tiles in row i to the right of position (i, j) are positioned at their solved location.
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(target_row, col) != (target_row, col):
                return False
            
        return True

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # Solution var
        mov = ''
        
        # Check if the lower row invariant is true at the begining 
        assert self.lower_row_invariant(target_row, target_col)
        
        # Main logic
        mov = self.position_tile(target_row, target_col)
        
        # Check if the lower row invariant is true at the end
        #assert self.lower_row_invariant(target_row, target_col - 1)
        
        return mov

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # Solution vars
        mov = ''
        temp = ''
        
        # Check if the lower row invariant is true at the begining 
        assert self.lower_row_invariant(target_row, 0)
        
        # Main logic
        temp = 'ur'
        mov += temp 
        self.update_puzzle(temp)
        
        # Finish if solved
        if self.current_position(target_row, 0) == (target_row, 0):
            temp = ('r' *  (self.get_width() - 2))
            mov += temp 
            self.update_puzzle(temp)
        
        # Otherwise    
        else:
            # Make the desired placement
            temp = self.position_tile(target_row, 0)
            mov += temp
            
            # Make the standard move string
            temp = "ruldrdlurdluurddlur"
            mov += temp 
            self.update_puzzle(temp)
            
            # Move the zero tile to the end
            temp = ('r' *  (self.get_width() - 2))
            mov += temp 
            self.update_puzzle(temp)
            
        # Check if the lower row invariant is true at the end 
        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1)

        return mov

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Check if zero tile is at the position mentioned
        if self.get_number(0, target_col) != 0:
            return False
        
        # Check for the tiles in row 1 and row 0 but in col >= target_col
        for row in range(2):
            for col in range(target_col, self.get_width()):
                if (row, col) != (0, target_col):
                    if self.current_position(row, col) != (row, col):
                        return False
             
        # Check for remaining rows
        for row in range(2, self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row, col) != (row, col):
                    return False        
        
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # Check tiles in the same row or below
        if not self.lower_row_invariant(1, target_col):
            return False
        
        # Check tiles in upper row to the right
        for col in range(target_col + 1, self.get_width()):
            if self.current_position(1, col) != (1, col):
                return False
            
        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # Solution vars
        temp = ''
        mov = ''
        
        # Check if the first row invariant is true at the beginning
        assert self.row0_invariant(target_col)
        
        # Move the zero tile to lower left position
        temp = 'ld'
        mov += temp 
        self.update_puzzle(temp)
        
        # Check if not solved
        if self.current_position(0, target_col) != (0, target_col):
            # Maked the desired placement
            mov += self.position_tile(0, target_col)
 
            # Make the standard move string
            temp = "urdlurrdluldrruld"
            mov += temp
            self.update_puzzle(temp)
        
        # Check if the second row invariant is true at the end 
        assert self.row1_invariant(target_col - 1)
        
        return mov

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # Solution vars
        mov = ''
        temp = ''
        
        # Check if the second row invariant is true at the begining 
        assert self.row1_invariant(target_col)
        
        # Main logic 
        mov += self.position_tile(1, target_col)
        temp = 'ur'
        mov += temp 
        self.update_puzzle(temp)
        
        # Check if the first row invariant is true at the end
        assert self.row0_invariant(target_col)
        
        return mov

    ###########################################################
    # Phase 3 methods
    def is_2x2_solved(self):
        """
        A helper function that returns True
        if the the upper 2 x 2 corner of the puzzle is solved
        """
        for row in range(2):
            for col in range(2):
                if self.current_position(row, col) != (row, col):
                    return False
                
        return True        
    
    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # Solution vars
        temp = ''
        mov = ''
        
        # Check if second row invariant is True at the begging
        assert self.row1_invariant(1)
        
        # Move zero tile to its correct position
        temp = 'lu'
        mov += temp
        self.update_puzzle(temp)
        
        # Make the standard moves until it's solved
        while not self.is_2x2_solved():
            temp = 'rdlu'
            mov += temp 
            self.update_puzzle(temp)
           
        return mov

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # Solution vars
        temp = ''
        mov = ''
        
        # Zero position and limits
        pos = self.current_position(0, 0)
        limit = (self.get_height() - 1, self.get_width() - 1)
        
        # Move the zero tile to the last position
        temp = 'd' * (limit[0] - pos[0]) + 'r' * (limit[1] - pos[1])
        mov += temp
        self.update_puzzle(temp)
        
        # Solve all rows except top 2 rows
        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, 0, -1):
                temp = self.solve_interior_tile(row, col)
                mov += temp
            temp = self.solve_col0_tile(row)
            mov += temp
        
        # Solve top 2 rows execpt for the last 2x2 square
        for col in range(self.get_width() - 1, 1, -1):
            temp = self.solve_row1_tile(col) + self.solve_row0_tile(col)
            mov += temp
            
        # Solve last 2x2 square
        temp = self.solve_2x2()
        mov += temp
        
        return mov
    
# Start interactive simulation    
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))


