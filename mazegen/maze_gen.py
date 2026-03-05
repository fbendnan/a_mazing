from .DFS_algo import DFSGenerator
from .Prim_algo import PrimeGenerator


class MazeGenerator:
    def __init__(self, configuration):
        self.configuration = configuration
        self.algo = configuration.get("ALGO", 'PRIM')
        self.height = configuration["HEIGHT"]
        self.width = configuration["WIDTH"]
        self.entry = configuration["ENTRY"]
        self.exit = configuration["EXIT"]
        self.seed = configuration.get("SEED", None)
        self.perfect = configuration.get("PERFECT", True)
        self.maze = None
        self.grid = None

    def generate(self):
        if self.algo.upper() == 'PRIM':
            self.maze = PrimeGenerator(self.configuration)
        elif self.algo.upper() == 'DFS':
            self.maze = DFSGenerator(self.configuration)
        self.maze.generate()
        self.grid = self.maze.grid
    
    def get_solver_walls(self):
        return self.maze.generate_grid_walls_for_solver()
