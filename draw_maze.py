import curses
from gen_maze import Maze


MAZE_WIDTH = 10
MAZE_HEIGHT = 8


WALL = '█'
CELL_W = 2
CELL_H = 1

class MazeDrawing:
    def __init__(self):
        self.canvas_height = MAZE_HEIGHT * (CELL_H + 1) + 1
        self.canvas_width = MAZE_WIDTH * (CELL_W + 1) + 1
        self.maze_canvas = [[WALL for _ in range(self.canvas_width)] for _ in range(self.canvas_height)]
        self.maze = Maze(MAZE_HEIGHT, MAZE_WIDTH)
        
    def build_maze_canvas(self):
        for x in range(MAZE_HEIGHT):
            for y in range(MAZE_WIDTH):
                cell = self.maze.grid[x][y]

                row_pos = x * (CELL_H + 1) + 1
                col_pos = y * (CELL_W + 1) + 1

                for i in range(CELL_H):
                    for j in range(CELL_W):
                        self.maze_canvas[row_pos + i][col_pos + j] = ' '

                if not cell.walls['N']:
                    for j in range(CELL_W):
                        self.maze_canvas[row_pos - 1][col_pos + j] = ' '
                if not cell.walls['S']:
                    for j in range(CELL_W):
                        self.maze_canvas[row_pos + CELL_H][col_pos + j] = ' '
                if not cell.walls['W']:
                    for i in range(CELL_H):
                        self.maze_canvas[row_pos + i][col_pos - 1] = ' '
                if not cell.walls['E']:
                    for i in range(CELL_H):
                        self.maze_canvas[row_pos + i][col_pos + CELL_W] = ' '


    def choices(self, stdscr):
        stdscr.addstr(self.canvas_height, 1, "===A-Maze-ing===")
        stdscr.addstr(self.canvas_height + 1, 1, "1. Re-generate a new maze")
        stdscr.addstr(self.canvas_height + 2, 1, "2. Show/Hide path from entry to exit")
        stdscr.addstr(self.canvas_height + 3, 1, "3. Rotate maze colors")
        stdscr.addstr(self.canvas_height + 4, 1, "4. Quit")
        stdscr.addstr(self.canvas_height + 5, 2, "choice? (1-4):")


    def draw(self, stdscr):
        try:
            curses.curs_set(0)
            stdscr.keypad(True)
            self.maze.generate(2,4)
            self.build_maze_canvas()
            curses.use_default_colors()
            curses.start_color()
            curses.init_pair(1, curses.COLOR_CYAN, -1)
            for row_idx, row in enumerate(self.maze_canvas):
                for col_idx, char in enumerate(row):
                    if char == WALL:
                        stdscr.addstr(row_idx, col_idx, char, curses.color_pair(1))
                    else:
                        stdscr.addstr(row_idx, col_idx, char)
            self.choices(stdscr)
            stdscr.refresh()
            while True:
                key = stdscr.getch()
                if key == ord('1'):
                    ...
                elif key == ord('2'):
                    ...
                elif key == ord('3'):
                    ...
                elif key == ord('4'):
                    break
        except Exception:
            stdscr.addstr()
            

if __name__ == "__main__":
    d = MazeDrawing()
    curses.wrapper(d.draw)
