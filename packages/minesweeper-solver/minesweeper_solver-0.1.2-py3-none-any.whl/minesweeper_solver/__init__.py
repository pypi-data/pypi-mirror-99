from .solver import MineSweeperSolver

def main():
    s = MineSweeperSolver(10, 10, 10)
    s.solve()