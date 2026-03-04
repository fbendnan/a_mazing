class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_visited = False
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.is_cell_42 = False
        self.solver_walls = []