import sys
from mazegen.maze_gen import MazeGenerator
from mazegen.parssing import parsser
from mazegen.draw_maze import MazeDrawing
from mazegen.output_gen import Output

import curses


# try:
if len(sys.argv) != 2:
    raise ValueError("You should enter: python3 a_maze_ing.py config.txt")
CONFIG_FILE = sys.argv[1]
configuration = parsser(CONFIG_FILE)
print(configuration)
maze = MazeGenerator(configuration)
maze.generate()

draw_maze = MazeDrawing(maze)
curses.wrapper(draw_maze.main)

output = Output(configuration, maze, draw_maze.path)


# except (Exception, KeyboardInterrupt) as e:
#     print(e)
