from Prim_algo import PrimeGenerator
import curses
import random


def regenerate_maze(configuration):
    new_maze = PrimeGenerator(configuration)
    from draw_maze import MazeDrawing

    draw_maze = MazeDrawing(new_maze)
    return new_maze
    # curses.wrapper(draw_maze.main)


def rotate_maze_color(stdscr, maze_canvas, WALL):
    colors = [
        curses.init_pair(1, curses.COLOR_CYAN, -1),
        curses.init_pair(2, curses.COLOR_GREEN, -1),
        curses.init_pair(3, curses.COLOR_MAGENTA, -1),
        curses.init_pair(4, curses.COLOR_RED, -1),
        curses.init_pair(5, curses.COLOR_YELLOW, -1),
        curses.init_pair(6, curses.COLOR_WHITE, -1),
        curses.init_pair(7, curses.COLOR_BLACK, -1),
    ]
    color = random.randint(1, 7)
    for row_idx, row in enumerate(maze_canvas):
        for col_idx, char in enumerate(row):
            if char == WALL:
                stdscr.addstr(row_idx, col_idx, char, curses.color_pair(color))
            else:
                stdscr.addstr(row_idx, col_idx, char)
