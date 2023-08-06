# Solver 
# write an algo that picks a 100% safe box with given info, and store mines that 
# adding more bombs & grids makes it more difficult

# avoid bombs in the coordinate that the user chooses

# search for all zeros that are connected to ititial 0 (bfs or dfs)
 
from .game import MineSweeper
import random

class MineSweeperSolver:
    def __init__(self, width, height, num_mines):
        self.game = MineSweeper(width, height, num_mines) 
    
    def get_visible_numbers(self):
        """
        Returns a list of all visible
        numbers that are selected.
        """
        visible_nums = []

        for i in range(self.game.height):
            for j in range(self.game.width):
                if self.game.is_selected(i, j):
                    visible_nums.append((i, j))
        
        return visible_nums
    
    def get_adjacent_flags(self, i, j):
        """
        Returns a list of all adjacents that are
        flags from i & j.
        """
        flags = []

        for ni, nj in self.game.hidden_board.get_neighbours(i, j):
            if self.game.is_flagged(ni, nj):
                flags.append((ni, nj))
        
        return flags
    
    def get_hidden_neighbours(self, i, j):
        """
        Returns a list of all neighbours that are hidden
        from coord i & j.
        """
        hidden_neighbours = []

        for ni, nj in self.game.hidden_board.get_neighbours(i, j):
            if not self.game.is_selected(ni, nj):
                hidden_neighbours.append((ni, nj))
        
        return hidden_neighbours

    def is_satisfied(self, i, j):
        """
        If the number of flags next to a numbered tile is equal to the tiles number
        """
        flags = self.get_adjacent_flags(i, j)
        return len(flags) == self.game.hidden_board.board[i][j]
    
    def make_random_selection(self):
        """
        Select a random tile that has not yet been selected or flagged.
        """

        i = random.randint(0, self.game.height - 1)
        j = random.randint(0, self.game.width - 1)

        if self.game.hidden_board is None or not self.game.is_selected(i, j):
            self.game.select(i, j)
        else:
            self.make_random_selection()

    def identify_selections(self):
        """
        Find all selections with 100% certainty.
        """

        for i, j in self.get_visible_numbers():
            if self.is_satisfied(i,j):
                neighbours = self.game.hidden_board.get_neighbours(i, j)
                for ni, nj in neighbours:
                    if (not self.game.is_selected(ni, nj) and not self.game.is_flagged(ni, nj)):
                        yield ni, nj
    
    def identify_flags(self):
        """
        Finds all flags with 100% certainty.
        """

        for i, j in self.get_visible_numbers():
            hidden_neighbours = self.get_hidden_neighbours(i,j)
            if self.hidden_neighbours_are_mines(i, j, hidden_neighbours):
            # if len(hidden_neighbours) == self.game.hidden_board.board[i][j]:
                for ni, nj in hidden_neighbours:
                    if not self.game.is_flagged(ni, nj):
                        yield ni, nj
    
    def hidden_neighbours_are_mines(self, i, j, hidden_neighbours):
        return len(hidden_neighbours) == self.game.hidden_board.board[i][j]

    def solve(self):
        """
        Runs the solver.
        """
        self.make_random_selection()
        self.game.display_board()

        while not self.game.game_lost() and not self.game.game_won():
            change_made = False

            for i, j in self.identify_flags():
                change_made =  True
                self.game.flag(i, j)
            print('Flaggings')
            self.game.display_board()

            for i, j in self.identify_selections():
                change_made = True
                self.game.select(i, j)
            print('Selections')
            self.game.display_board()

            if not change_made:
                self.make_random_selection()
                print('Random selection !!!!')
                self.game.display_board()
        
        if self.game.game_won():
            print("You won!")
        else:
            print("You Lost")

        
