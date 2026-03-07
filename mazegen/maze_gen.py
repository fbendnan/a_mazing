from typing import Dict, List, Any
from .DFS_algo import DFSGenerator
from .Prim_algo import PrimeGenerator


class MazeGenerator:
    """
    Main interface for maze generation.

    This class selects the maze generation algorithm (Prim or DFS)
    based on the configuration and exposes the generated grid
    and solver wall representation.
    """

    def __init__(self, configuration: Dict) -> None:
        """
        Initialize the maze generator.

        Args:
            configuration: Dictionary containing maze settings such as:
                HEIGHT, WIDTH, ENTRY, EXIT, ALGO, SEED, and PERFECT.
        """

        self.configuration: Dict = configuration
        self.algo: str = configuration.get("ALGO", "PRIM")

        self.height: int = configuration["HEIGHT"]
        self.width: int = configuration["WIDTH"]

        self.entry: tuple[int, int] = configuration["ENTRY"]
        self.exit: tuple[int, int] = configuration["EXIT"]

        self.seed: int | None = configuration.get("SEED", None)
        self.perfect: bool = configuration.get("PERFECT", True)

        self.maze: Any= []
        self.grid: Any= []

    def generate(self) -> None:
        """
        Generate the maze using the selected algorithm.

        Supported algorithms:
            - PRIM
            - DFS
        """

        if self.algo.upper() == "PRIM":
            self.maze = PrimeGenerator(self.configuration)

        elif self.algo.upper() == "DFS":
            self.maze = DFSGenerator(self.configuration)

        else:
            raise ValueError(f"Unknown algorithm: {self.algo}")

        self.maze.generate()
        self.grid = self.maze.grid

    def get_solver_walls(self) -> List:
        """
        Return the maze walls formatted for the pathfinding solver.

        Returns:
            A grid representation where each cell contains
            the wall configuration [N, E, S, W].
        """
        return self.maze.generate_grid_walls_for_solver()
