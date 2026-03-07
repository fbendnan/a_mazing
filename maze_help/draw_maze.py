import curses
import random
# import time
from typing import List, Tuple, Optional
from .output_gen import Output
from mazegen.maze_gen import MazeGenerator
from .a_star import solver

WALL = "█"
CELL_W = 2
CELL_H = 1


class MazeDrawing:
    """
    Handle the visualization and interaction of the maze using curses.

    This class is responsible for:
    - Converting the maze structure into a drawable canvas
    - Displaying the maze in the terminal
    - Coloring special cells
    - Showing the solution path
    - Handling user interaction (menu and keyboard)
    """

    def __init__(self, maze: MazeGenerator) -> None:
        """
        Initialize the drawing system for a maze.

        Args:
            maze: A generated MazeGenerator instance containing
                  the maze structure, grid, entry, and exit.
        """
        self.canvas_height: int = maze.height * (CELL_H + 1) + 1
        self.canvas_width: int = maze.width * (CELL_W + 1) + 1
        self.maze_canvas: Optional[List[List[str]]] = None
        self.maze: MazeGenerator = maze
        self.scr_height: int = 0
        self.scr_width: int = 0
        self.path: Optional[List[Tuple[int, int]]] = []

    def build_maze_canvas(self) -> None:
        """
        Convert the maze grid into a 2D canvas representation.

        The canvas is composed of characters where:
        - WALL represents walls
        - spaces represent open paths
        """
        self.maze_canvas = [
            [WALL for _ in range(self.canvas_width)]
            for _ in range(self.canvas_height)
        ]

        for x in range(self.maze.height):
            for y in range(self.maze.width):
                cell = self.maze.grid[x][y]

                row_pos = x * (CELL_H + 1) + 1
                col_pos = y * (CELL_W + 1) + 1

                for i in range(CELL_H):
                    for j in range(CELL_W):
                        self.maze_canvas[row_pos + i][col_pos + j] = " "

                if not cell.walls["N"]:
                    for j in range(CELL_W):
                        self.maze_canvas[row_pos - 1][col_pos + j] = " "

                if not cell.walls["S"]:
                    for j in range(CELL_W):
                        self.maze_canvas[row_pos + CELL_H][col_pos + j] = " "

                if not cell.walls["W"]:
                    for i in range(CELL_H):
                        self.maze_canvas[row_pos + i][col_pos - 1] = " "

                if not cell.walls["E"]:
                    for i in range(CELL_H):
                        self.maze_canvas[row_pos + i][col_pos + CELL_W] = " "

    def colorate_42_cells(self, stdscr: curses.window) -> None:
        """
        Highlight special '42 cells' inside the maze.

        Args:
            stdscr: The curses window used for drawing.
        """
        curses.init_pair(2, curses.COLOR_WHITE, -1)

        for x in range(self.maze.height):
            for y in range(self.maze.width):
                cell = self.maze.grid[x][y]

                if cell.is_cell_42:
                    row_pos = x * (CELL_H + 1) + 1
                    col_pos = y * (CELL_W + 1) + 1

                    for i in range(CELL_H):
                        for j in range(CELL_W):
                            stdscr.addstr(
                                row_pos + i,
                                col_pos + j,
                                " ",
                                curses.color_pair(2) | curses.A_REVERSE,
                            )

    def print_choices(self, stdscr: curses.window) -> None:
        """
        Display the menu options below the maze.

        Args:
            stdscr: The curses window used for drawing.
        """
        stdscr.addstr(self.canvas_height, 1, "===A-Maze-ing===")
        stdscr.addstr(self.canvas_height + 1, 1, "1. Re-generate a new maze")
        stdscr.addstr(self.canvas_height + 2, 1, "2. Show/Hide path from "
                                                 "entry to exit")
        stdscr.addstr(self.canvas_height + 3, 1, "3. Rotate maze colors")
        stdscr.addstr(self.canvas_height + 4, 1, "4. Quit")
        stdscr.addstr(self.canvas_height + 5, 2, "choice? (1-4):")

    def put_entry_and_exit(
        self,
        stdscr: curses.window,
        entry: Tuple[int, int],
        exit: Tuple[int, int],
    ) -> None:
        """
        Draw the entry and exit points of the maze.

        Args:
            stdscr: The curses window used for drawing.
            entry: Coordinates of the maze entry (row, column).
            exit: Coordinates of the maze exit (row, column).
        """
        x, y = entry
        i, j = exit

        row_pos_entry = x * (CELL_H + 1) + 1
        col_pos_entry = y * (CELL_W + 1) + 1
        row_pos_exit = i * (CELL_H + 1) + 1
        col_pos_exit = j * (CELL_W + 1) + 1

        stdscr.addstr(row_pos_entry, col_pos_entry, "🐀")
        stdscr.addstr(row_pos_exit, col_pos_exit, "🧀")

    def colorate_maze(
            self, stdscr: curses.window, maze_color: int = 1) -> None:
        """
        Draw the maze walls using the selected color.

        Args:
            stdscr: The curses window used for drawing.
            maze_color: The color pair index used for maze walls.
        """
        curses.init_pair(1, curses.COLOR_BLUE, -1),
        curses.init_pair(2, curses.COLOR_GREEN, -1),
        curses.init_pair(3, curses.COLOR_MAGENTA, -1),
        curses.init_pair(4, curses.COLOR_RED, -1),
        curses.init_pair(5, curses.COLOR_YELLOW, -1),
        curses.init_pair(6, curses.COLOR_WHITE, -1),
        curses.init_pair(7, curses.COLOR_BLACK, -1),
        curses.init_pair(8, curses.COLOR_CYAN, -1),

        for row_idx, row in enumerate(self.maze_canvas):
            for col_idx, char in enumerate(row):
                if char == WALL:
                    stdscr.addstr(
                        row_idx,
                        col_idx,
                        char,
                        curses.color_pair(maze_color),
                    )
                else:
                    stdscr.addstr(row_idx, col_idx, char)

    def show_path(self, stdscr: curses.window) -> None:
        """
        Display the solution path from entry to exit.

        Args:
            stdscr: The curses window used for drawing.
        """
        self.path = solver(self.maze)
        output = Output(self.maze.configuration, self.maze, self.path)
        output.process_maze()
        for cell in self.path[1:-1]:
            row, col = cell
            row_pos = row * (CELL_H + 1) + 1
            col_pos = col * (CELL_W + 1) + 1
            stdscr.addstr(row_pos, col_pos, "🐾")

    def draw(self, stdscr: curses.window, maze_color: int) -> None:
        """
        Render the complete maze interface.

        Args:
            stdscr: The curses window used for drawing.
            maze_color: The color used for maze walls.
        """

        self.build_maze_canvas()
        self.colorate_maze(stdscr, maze_color)
        self.put_entry_and_exit(stdscr, self.maze.entry, self.maze.exit)
        self.colorate_42_cells(stdscr)
        self.print_choices(stdscr)
        stdscr.refresh()

    def main(self, stdscr: curses.window) -> None:
        """
        Main curses loop that controls the maze application.

        Handles:
        - keyboard input
        - maze regeneration
        - path visualization
        - color rotation
        - window resizing
        """
        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        stdscr.keypad(True)

        is_path: bool = False
        color: int = 1

        while True:
            output = Output(self.maze.configuration, self.maze, self.path)
            output.process_maze()
            self.scr_height, self.scr_width = stdscr.getmaxyx()

            if (
                self.scr_height < self.canvas_height + 6
                or self.scr_width < self.canvas_width
            ):
                stdscr.clear()

                try:
                    y = max(0, self.scr_height // 2)
                    x = max(0, self.scr_width // 2 - 10)

                    stdscr.addstr(y, x, "Terminal too small!")
                    stdscr.addstr(y + 1, max(0, x + 2), "Resize it please")
                    stdscr.addstr(y + 2, max(0, x + 1), "or press q to Quit")

                except curses.error:
                    pass

                stdscr.refresh()

                key = stdscr.getch()
                if key == ord("q"):
                    break

                continue

            stdscr.clear()
            self.draw(stdscr, color)

            if is_path:
                self.show_path(stdscr)

            stdscr.refresh()
            key = stdscr.getch()

            if key == ord("1"):
                if self.maze.seed is not None:
                    self.maze.configuration["SEED"] = None

                self.maze = MazeGenerator(self.maze.configuration)
                self.maze.generate()

            elif key == ord("2"):
                is_path = not is_path

            elif key == ord("3"):
                color = random.randint(1, 8)

            elif key == ord("4"):
                break

            elif key == curses.KEY_RESIZE:
                continue
