import sys
from maze_gen.parssing import parsser
from maze_gen.Prim_algo import PrimeGenerator
from maze_gen.draw_maze import MazeDrawing
from maze_gen.maze_not_perfect import DFSGenerator
# from maze_gen.a_star import solver
import curses


try:
    if len(sys.argv) != 2:
        raise ValueError("You should enter: python3 a_maze_ing.py config.txt")
    CONFIG_FILE = sys.argv[1]
    configuration = parsser(CONFIG_FILE)

    if 'ALGO' in configuration:
        if configuration["ALGO"] == 'DFS':
            maze = DFSGenerator(configuration)
        elif configuration['ALGO'] != 'PRIM':
            maze = PrimeGenerator(configuration)
        else:
            raise ValueError("ALGO='PRIM' or ALGO='DFS'")
    else:
        maze = PrimeGenerator(configuration)
    maze.generate()

    draw = MazeDrawing(maze)
    draw_maze = MazeDrawing(maze)
    curses.wrapper(draw_maze.main)


except Exception as e:
    print(e)
