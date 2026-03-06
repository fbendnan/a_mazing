import sys
from mazegen import MazeGenerator
from maze_help.parssing import parse_config
from maze_help.draw_maze import MazeDrawing
from maze_help.output_gen import Output

import curses


try:
    if len(sys.argv) != 2:
        raise ValueError("You should enter: python3 a_maze_ing.py config.txt")
    CONFIG_FILE = sys.argv[1]
    configuration = parse_config(CONFIG_FILE)
    # print(configuration)
    maze = MazeGenerator(configuration)
    maze.generate()

    draw_maze = MazeDrawing(maze)
    curses.wrapper(draw_maze.main)

    output = Output(configuration, maze, draw_maze.path)


except (Exception, KeyboardInterrupt) as e:
    print(e)
