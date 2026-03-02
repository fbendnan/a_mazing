import sys
from parssing import parsser
from Prim_algo import PrimeGenerator
from draw_maze import MazeDrawing
from maze_not_perfect import DFSGenerator
from a_star import solver

import curses


CONFIG_FILE = sys.argv[1]
try:

    configuration = parsser(CONFIG_FILE)

    # print(configuration)
    # maze = DFSGenerator(configuration)
    # maze.generate()

    maze = PrimeGenerator(configuration)
    maze.generate()
    print(maze.generate_grid_walls_for_solver())
    # walls =

    path = solver(maze.generate_grid_walls_for_solver())
    print(path)
    # draw = MazeDrawing(maze)
    # draw_maze = MazeDrawing(maze)
    # curses.wrapper(draw_maze.main)
except Exception as e:
    print(e)
