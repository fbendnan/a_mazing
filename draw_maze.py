from mlx.mlx import Mlx


CELL_SIZE = 40

RED_COLOR = 0x00FF0000

class Display_maze:
    def __init__(self, height, width, grid):
        self.height = height
        self.width = width
        self.grid = grid
        self.mlx
        self.mlx_ptr
        self.win_ptr


    def initialization(self):
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

    def windows(self):
        self.win_ptr = self.mlx.mlx_new_window(
            self.mlx_ptr, self.width, self.height, "maze"
            )
    
    def draw_walls(self, col, row):
        x = col * CELL_SIZE
        y = row * CELL_SIZE
        for cell in self.grid:
            if cell.walls['N']:
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, RED_COLOR)
            if cell.walls['S']:
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, RED_COLOR)
            if cell.walls['E']:
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, RED_COLOR)
            if cell.walls['W']:
                self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, RED_COLOR)
