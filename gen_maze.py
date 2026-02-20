import random

DIRS = {
    'N': (0, -1),
    'S': (0, 1),
    'E': (1, 0),
    'W': (-1, 0)
}

OPPOSITE = {
    'N': 'S',
    'S': 'N',
    'E': 'W',
    'W': 'E'
}

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_visited = False
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}

class Maze:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[Cell(x, y) for y in range(width)] for x in range(height)]
        self.frontier = set()

    def in_bounds(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def add_frontier(self, cell):
        x, y = cell.x, cell.y
        for dir, (dx, dy) in DIRS.items():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                neighbor = self.grid[nx][ny]
                if not neighbor.is_visited:
                    self.frontier.add(neighbor)

    def remove_wall_between(self, cell_a, cell_b):
        dx = cell_b.x - cell_a.x
        dy = cell_b.y - cell_a.y
        if dx == 1:
            cell_a.walls['S'] = False
            cell_b.walls['N'] = False
        elif dx == -1:
            cell_a.walls['N'] = False
            cell_b.walls['S'] = False
        elif dy == 1:
            cell_a.walls['E'] = False
            cell_b.walls['W'] = False
        elif dy == -1:
            cell_a.walls['W'] = False
            cell_b.walls['E'] = False

    def generate(self, start_x=0, start_y=0):
        start = self.grid[start_x][start_y]
        start.is_visited = True
        self.add_frontier(start)

        while self.frontier:
            cell_b = random.choice(tuple(self.frontier))
            self.frontier.remove(cell_b)

            visited_neighbors = []
            for dir, (dx, dy) in DIRS.items():
                nx, ny = cell_b.x + dx, cell_b.y + dy
                if self.in_bounds(nx, ny):
                    neighbor = self.grid[nx][ny]
                    if neighbor.is_visited:
                        visited_neighbors.append(neighbor)

            if visited_neighbors:
                cell_a = random.choice(visited_neighbors)
                self.remove_wall_between(cell_a, cell_b)

            cell_b.is_visited = True
            self.add_frontier(cell_b)

        self.grid[0][0].walls['N'] = False
        self.grid[self.height - 1][self.width - 1].walls['S'] = False

    def print_maze(self):
        H, W = self.height, self.width
        grid = [['%' for _ in range(W*2 + 1)] for _ in range(H*2 + 1)]

        for x in range(H):
            for y in range(W):
                cx, cy = x*2 + 1, y*2 + 1
                grid[cx][cy] = ' '
                cell = self.grid[x][y]
                if not cell.walls['N']:
                    grid[cx-1][cy] = ' '
                if not cell.walls['S']:
                    grid[cx+1][cy] = ' '
                if not cell.walls['W']:
                    grid[cx][cy-1] = ' '
                if not cell.walls['E']:
                    grid[cx][cy+1] = ' '

        for row in grid:
            print(''.join(row))

maze = Maze(height=5, width=9)
print(maze.grid)
maze.generate(start_x=0, start_y=0)
# maze.print_maze()
