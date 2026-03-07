class Output():
    def __init__(self, conf, maze, path):
        self.conf = conf
        self.maze = maze
        self.path = path

##[1,1,1,1] Top , Right ,bottom left
    def cell_to_hex(self, cell_walls):
        num = 0
        if cell_walls[0]:
            num += cell_walls[0] * 1
        if cell_walls[1]:
            num += cell_walls[1] * 2
        if cell_walls[2]:
            num += cell_walls[2] * 4
        if cell_walls[3]:
            num += cell_walls[3] * 8
        he_x = format(num, 'X')
        return he_x

    def ft_check_path(self, current, previous):
        i, j = previous
        x, y = current

        diff_r = i - x
        diff_c = j - y
        if diff_r < 0:
            return "S"
        elif diff_r > 0:
            return "N"
        if diff_c < 0:
            return "E"
        elif diff_c > 0:
            return "W" 
        return ""

    def ft_write_the_path(self):
        file = open("output.txt", "a")
        for i in range(1, len(self.path)):
            current = self.path[i]
            previous = self.path[i-1]
            y = self.ft_check_path(current, previous)
            file.write(y)
        file.close()

    def ft_write_entry_exit(self):
        file = open("output.txt", "a")
        x, y = self.conf["ENTRY"]
        file.write(str(x))
        file.write(",")
        file.write(str(y))
        file.write("\n")
        x, y = self.conf["EXIT"]
        file.write(str(x))
        file.write(",")
        file.write(str(y))
        file.write("\n")
        file.close()

    def process_maze(self):
        file = open("output.txt", "w")
        walls = self.maze.get_solver_walls()
        for row in walls:
            for cell_walls in row:
                hex_char = self.cell_to_hex(cell_walls)
                file.write(hex_char)
            file.write("\n")

        file.write("\n")
        file.close()
        self.ft_write_entry_exit()
        # self.ft_write_the_path()
