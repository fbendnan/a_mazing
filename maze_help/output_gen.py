from typing import List, Tuple, Dict, Any
from mazegen.maze_gen import MazeGenerator


class Output:
    def __init__(
        self,
        conf: Dict[str, Any],
        maze: MazeGenerator,
        path: List[Tuple[int, int]],
    ) -> None:
        self.conf: Dict[str, Any] = conf
        self.maze: MazeGenerator = maze
        self.path: List[Tuple[int, int]] = path

    # [1,1,1,1] -> Top, Right, Bottom, Left
    def cell_to_hex(self, cell_walls: List[int]) -> str:
        num: int = 0

        if cell_walls[0]:
            num += cell_walls[0] * 1
        if cell_walls[1]:
            num += cell_walls[1] * 2
        if cell_walls[2]:
            num += cell_walls[2] * 4
        if cell_walls[3]:
            num += cell_walls[3] * 8

        return format(num, "X")

    def ft_check_path(
        self,
        current: Tuple[int, int],
        previous: Tuple[int, int],
    ) -> str:
        i, j = previous
        x, y = current

        diff_r: int = i - x
        diff_c: int = j - y

        if diff_r < 0:
            return "S"
        elif diff_r > 0:
            return "N"
        if diff_c < 0:
            return "E"
        elif diff_c > 0:
            return "W"

        return ""

    def ft_write_the_path(self) -> None:
        with open(self.conf["OUTPUT_FILE"], "a") as file:
            for i in range(1, len(self.path)):
                current = self.path[i]
                previous = self.path[i - 1]
                direction = self.ft_check_path(current, previous)
                file.write(direction)

    def ft_write_entry_exit(self) -> None:
        with open(self.conf["OUTPUT_FILE"], "a") as file:
            x, y = self.conf["ENTRY"]
            file.write(f"{x},{y}\n")

            x, y = self.conf["EXIT"]
            file.write(f"{x},{y}\n")

    def process_maze(self) -> None:
        with open(self.conf["OUTPUT_FILE"], "w") as file:
            walls: List[List[List[int]]] = self.maze.get_solver_walls()

            for row in walls:
                for cell_walls in row:
                    hex_char = self.cell_to_hex(cell_walls)
                    file.write(hex_char)
                file.write("\n")

            file.write("\n")

        self.ft_write_entry_exit()
        self.ft_write_the_path()
