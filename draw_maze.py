import curses
from gen_maze import Maze

WIDTH = 10
HEIGHT = 8

CELL_W = 2
CELL_H = 1
WALL = '█'

def build_canvas(maze):
    canvas_height = HEIGHT * (CELL_H + 1) + 1
    canvas_width = WIDTH * (CELL_W + 1) + 1

    canvas = [[WALL for _ in range(canvas_width)] for _ in range(canvas_height)]

    for x in range(HEIGHT):
        for y in range(WIDTH):
            cell = maze.grid[x][y]

            top = x * (CELL_H + 1) + 1
            left = y * (CELL_W + 1) + 1

            for i in range(CELL_H):
                for j in range(CELL_W):
                    canvas[top + i][left + j] = ' '

            if not cell.walls['N']:
                for j in range(CELL_W):
                    canvas[top - 1][left + j] = ' '
            if not cell.walls['S']:
                for j in range(CELL_W):
                    canvas[top + CELL_H][left + j] = ' '
            if not cell.walls['W']:
                for i in range(CELL_H):
                    canvas[top + i][left - 1] = ' '
            if not cell.walls['E']:
                for i in range(CELL_H):
                    canvas[top + i][left + CELL_W] = ' '

    return canvas

def draw_maze(stdscr, canvas):
    stdscr.clear()
    for i, row in enumerate(canvas):
        stdscr.addstr(i, 0, ''.join(row))
    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)

    maze = Maze(HEIGHT, WIDTH)
    maze.generate(0, 0)

    canvas = build_canvas(maze)
    draw_maze(stdscr, canvas)

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break

if __name__ == "__main__":
    curses.wrapper(main)