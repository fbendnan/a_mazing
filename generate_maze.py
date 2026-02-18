import random


class cell_info:
    def __init__(self, cell):
        self.cell = cell
        self.is_visited = False
        self.walls = {}

    def fill_cell_walls(self):
        self.walls['N'] = (((self.cell[0]), (self.cell[1] - 1)), (self.cell))
        self.walls['W'] = (((self.cell[0] - 1), (self.cell[1])), (self.cell))
        self.walls['E'] = (((self.cell[0] + 1), (self.cell[1])), self.cell)
        self.walls['S'] = (((self.cell[0]), (self.cell[1] + 1)), self.cell)


class maze_manager:
    def __init__(self):
        self.frontier_edges = set()
        self.grid = {}
        self.walls_to_remove = set()

    def initialise_grid(self, height, width):
        for x in range(height):
            for y in range(width):
                c = cell_info((x, y))
                c.fill_cell_walls()
                self.grid[(x, y)] = c

    def add_edge_from_cell(self, cell):
        for wall in cell.walls.values():
            neighbor_coord, current_coord = wall
            if neighbor_coord in self.grid:
                self.frontier_edges.add(wall)

    def mark_start_cell(self, start_x, start_y):
        start = self.grid[(start_x, start_y)]
        start.is_visited = True
        self.add_edge_from_cell(start)

    def remove_edge(self, edge):
        self.frontier_edges.remove(edge)


def generate_maze_with_prim_algo():
    start_point = (12, 15)
    maze = maze_manager()
    maze.initialise_grid(start_point[0], start_point[1])
    maze.mark_start_cell(2, 3)
    while maze.frontier_edges:
        edge = random.choice(list(maze.frontier_edges))
        maze.remove_edge(edge)

        neighbor_coord, current_coord = edge
        cell_a = maze.grid[neighbor_coord]
        cell_b = maze.grid[current_coord]

        if cell_a.is_visited != cell_b.is_visited:
            new_cell = cell_b if cell_a.is_visited else cell_a
            new_cell.is_visited = True
            maze.walls_to_remove.add(edge)
            maze.add_edge_from_cell(new_cell)

    print(maze.grid)

generate_maze_with_prim_algo()
