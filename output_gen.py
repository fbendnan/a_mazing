class Output():
    def __init__(self, conf, maze, path):
        self.conf = conf
        self.maze = maze 
        self.path = path

#[1,1,1,1] Top , Right ,bottom left
    def cell_to_hex(self, cell):
        num = 0
        if cell[0]:
            num += cell[0] * 1
        if cell[1]:
            num += cell[1] * 2
        if cell[2]:
            num += cell[2] * 4
        if cell[3]:
            num += cell[3] * 8
        he_x = format(num, 'X')
        return he_x

    def process_maze(self):
        file = open("output.txt", "w")
        # file.write("hello")
        for row in self.maze:
            for cell in row:
                hex_char = self.cell_to_hex(cell)
                file.write(hex_char)
            file.write("\n")
        file.close()
