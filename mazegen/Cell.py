from typing import List, Dict

class Cell:
    def __init__(self, x, y) -> None:
        self.x: int = x
        self.y: int = y
        self.is_visited: bool = False
        self.walls: Dict = {'N': True, 'E': True, 'S': True, 'W': True}
        self.is_cell_42: bool = False
        self.solver_walls: List = []