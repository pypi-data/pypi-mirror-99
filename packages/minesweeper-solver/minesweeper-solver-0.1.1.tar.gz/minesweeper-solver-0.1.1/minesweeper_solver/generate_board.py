# utilise the yeetcode problems for the reveal

import random
import numpy as np

class Board:
    def __init__(self, width, height):
        self.board = [[0] * width for _ in range(height)]
        self.width = width
        self.height = height
    
    def add_mines(self, num_mines, i, j):
        """
        Randomly add the number of mines to the board.
        """

        ignore_coords = set(self.get_neighbours(i, j))
        ignore_coords.add((i, j))

        while num_mines != 0:
            ri = random.randint(0, self.height - 1)
            rj = random.randint(0, self.width - 1)
            # dont place a mine in the same spot twice
            if self._is_mine(ri, rj) or (ri, rj) in ignore_coords:
                continue
            self.board[ri][rj] = "M"
            self.increment_adjacents(ri, rj)
            num_mines -= 1

    def _is_inbounds(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width
    
    def _is_mine(self, i, j):
        return self.board[i][j] == "M"

    def increment_adjacents(self, i, j):
        """
        increments all adjacents of mines by 1 that are not mines
        """

        for ni, nj in self.get_neighbours(i, j):
            if not self._is_mine(ni, nj):
                self.board[ni][nj] += 1
    
    def get_neighbours(self, i, j):
        """
        Returns a list of all inbounds coorinates of the given
        i & j. 
        """

        directions = [
            (i - 1, j), # up
            (i + 1, j), # down
            (i, j - 1), # left
            (i, j + 1), # right
            (i - 1, j - 1), # top_left
            (i - 1, j + 1), # top_right
            (i + 1, j - 1), # bottom_left
            (i + 1, j + 1), # bottom_right
        ]

        for ni, nj in directions:
            if self._is_inbounds(ni, nj):
                yield ni, nj

if __name__ == '__main__':
    board = Board(5, 5)
    board.add_mines(5, 1, 1)
    print(np.matrix(board.board))

    
