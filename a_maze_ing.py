import sys
from parssing import parsser
from Prim_algo import PrimeGenerator
from draw_maze import MazeDrawing
import curses


CONFIG_FILE = sys.argv[1]

configuration = parsser(CONFIG_FILE)

# print(configuration)

maze = PrimeGenerator(configuration)


draw = MazeDrawing(maze)
draw_maze = MazeDrawing(maze)
try:
    curses.wrapper(draw_maze.main)
except KeyboardInterrupt as e:
    print("Error: Wrapper is out")

