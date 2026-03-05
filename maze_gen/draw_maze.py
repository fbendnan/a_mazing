import curses
import random
from .Prim_algo import PrimeGenerator
from .maze_not_perfect import DFSGenerator
from .a_star import solver
import time

# add the path of the maze and try the algo in my maze

WALL = "█"
CELL_W = 2
CELL_H = 1

class MazeDrawing:
    def __init__(self, maze):
        self.canvas_height = maze.height * (CELL_H + 1) + 1
        self.canvas_width = maze.width * (CELL_W + 1) + 1
        self.maze_canvas = None
        self.maze = maze
        self.scr_height = 0
        self.scr_width = 0


    def build_maze_canvas(self):
        self.maze_canvas = [
            [WALL for _ in range(self.canvas_width)] for _ in range(self.canvas_height)
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

    def colorate_42_cells(self, stdscr):
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

    def print_choices(self, stdscr):
        stdscr.addstr(self.canvas_height, 1, "===A-Maze-ing===")
        stdscr.addstr(self.canvas_height + 1, 1, "1. Re-generate a new maze")
        stdscr.addstr(self.canvas_height + 2, 1, "2. Show/Hide path from entry to exit")
        stdscr.addstr(self.canvas_height + 3, 1, "3. Rotate maze colors")
        stdscr.addstr(self.canvas_height + 4, 1, "4. Quit")
        stdscr.addstr(self.canvas_height + 5, 2, "choice? (1-4):")

    def put_entry_and_exit(self, stdscr, entry, exit):
        x, y = entry
        i, j = exit
        row_pos_entry = x * (CELL_H + 1) + 1
        col_pos_entry = y * (CELL_W + 1) + 1
        row_pos_exit = i * (CELL_H + 1) + 1
        col_pos_exit = j * (CELL_W + 1) + 1

        stdscr.addstr(row_pos_entry, col_pos_entry, "🐀")
        stdscr.addstr(row_pos_exit, col_pos_exit, "🧀")

    def colorate_maze(self, stdscr, maze_color = 1):
        colors = [
        curses.init_pair(1, curses.COLOR_BLUE, -1),
        curses.init_pair(2, curses.COLOR_GREEN, -1),
        curses.init_pair(3, curses.COLOR_MAGENTA, -1),
        curses.init_pair(4, curses.COLOR_RED, -1),
        curses.init_pair(5, curses.COLOR_YELLOW, -1),
        curses.init_pair(6, curses.COLOR_WHITE, -1),
        curses.init_pair(7, curses.COLOR_BLACK, -1),
        curses.init_pair(8, curses.COLOR_CYAN, -1)
        ]
        
        for row_idx, row in enumerate(self.maze_canvas):
            for col_idx, char in enumerate(row):
                if char == WALL:
                    stdscr.addstr(row_idx, col_idx, char, curses.color_pair(maze_color))
                else:
                    stdscr.addstr(row_idx, col_idx, char)

    def show_path(self, stdscr):
        path = solver(self.maze)
        for cell in path[1:-1]:
            ##############check the row and col how they returned from path
            row, col = cell
            row_pos = row * (CELL_H + 1) + 1
            col_pos = col * (CELL_W + 1) + 1
            stdscr.addstr(row_pos, col_pos, "🐾")

    def draw(self, stdscr, maze_color):
        self.build_maze_canvas()
        self.colorate_maze(stdscr, maze_color)
        #############
        self.put_entry_and_exit(stdscr, self.maze.entry, self.maze.exit)
        self.colorate_42_cells(stdscr)
        self.print_choices(stdscr)
        stdscr.refresh()

    def main(self, stdscr):

        curses.curs_set(0)
        curses.start_color()
        curses.use_default_colors()
        stdscr.keypad(True)
        is_path = False
        color = 1

        while True:

            self.scr_height, self.scr_width = stdscr.getmaxyx()

            if (
                self.scr_height < self.canvas_height + 6
                or self.scr_width < self.canvas_width
            ):
                stdscr.clear()
                stdscr.addstr(
                    self.scr_height // 2,
                    max(0, self.scr_width // 2 - 10),
                    "Terminal too small!",
                )
                stdscr.addstr(
                    self.scr_height // 2 + 1,
                    max(0, self.scr_width // 2 - 8),
                    "Resize it please",
                )
                stdscr.addstr(
                    self.scr_height // 2 + 2,
                    max(0, self.scr_width // 2 - 9),
                    "or press q to Quit",
                )
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
                time.sleep(0.5)
            key = stdscr.getch()

            if key == ord("1"):
                if self.maze.seed is not None:
                    self.maze.configuration["SEED"] = None
                if 'ALGO' in self.maze.configuration and self.maze.configuration["ALGO"] == 'DFS':
                    self.maze = DFSGenerator(self.maze.configuration)
                else:
                    self.maze = PrimeGenerator(self.maze.configuration)
                self.maze.generate()

            elif key == ord("2"):
                is_path = not is_path

            elif key == ord("3"):
                color = random.randint(1, 8)

            elif key == ord("4"):
                break

            elif key == curses.KEY_RESIZE:
                continue
