from Prim_algo import PrimeGenerator


class Info:
    def __init__(self, height, width, g):
        self.height = height
        self.width = width
        self.g = g

    def position_start(self):
        start = (0, 0)
        return start

    def position_goal(self):
        goal = (self.height - 1, self.width - 1)
        return goal


class Brain(Info):
    def __init__(self, wall, height, width, g):
        super().__init__(height, width, g)
        self.height = height
        self.width = width
        self.g = g
        self.wall = wall

    def abc(self, num):
        if num < 0:
            num = -num
        return num

    def found_neighbor(self, current):
        x, y = current
        neighbor = []
        # print("now ",self.wall[x])
        if x > 0 and self.wall[x][y][0] == 0:
            # print("first neighbor",neighbor)
            neighbor.append((x - 1, y))
        if x < self.height - 1 and self.wall[x][y][2] == 0:
            # print("first neighbor",neighbor)
            neighbor.append((x + 1, y))
        if y > 0 and self.wall[x][y][3] == 0:
            # print("first neighbor",neighbor)
            neighbor.append((x, y - 1))
        if y < self.width - 1 and self.wall[x][y][1] == 0:
            # print("first neighbor",neighbor)
            neighbor.append((x, y + 1))
        return neighbor

    def heuristic(self, node, goal):
        row, col = goal
        x, y = node
        h = self.abc(col - y) + self.abc(row - x)
        # f = h + self.g[(x, y)]
        # lic_h.append((f,(x,y)))
        # return lic_h
        return h

    def min_f(self, lst):
        if not lst:
            return None
        f = min(lst, key=lambda t: t[0])
        return f


def solver(wall):
    height = 12
    width = 40
    g = {}
    # maze = PrimeGenerator({'WIDTH': 4, 'HEIGHT': 4, 'EXIT': (3, 2), 'ENTRY': (0, 0), 'OUTPUT_FILE': 'maze.txt', 'PERFECT': True, 'SEED': 27, 'ALGO': 'prim'})
    # maze.generate()
    wall = wall
    
    info = Info(height, width, g)
    start = info.position_start()
    g[start] = 0
    goal = info.position_goal()
    brain = Brain(wall, height, width, g)
    # print("wall",brain.wall)
    open_list = []
    h = brain.heuristic(start, goal)
    open_list.append((h, start))
    visited = set()
    # print("Goal is:", goal)
    path = {}
    # print("it here",open_list)
    while open_list:  # if it return none what it will be
        (f_val, current) = brain.min_f(open_list)
        open_list.remove((f_val, current))
        visited.add(current)
        if current == goal:
            # path[current] = goal
            print("Goaaal")
            break
        # print("current",current)
        neighbors = brain.found_neighbor(current)
        # print("visited :",neighbor)

        for neighbor in neighbors:
            nx, ny = neighbor
            if (nx, ny) in visited:
                continue
            value_g = brain.g[(current)] + 1
            h = brain.heuristic((nx, ny), goal)
            f = h + value_g
            if (nx, ny) not in brain.g:
                brain.g[(nx, ny)] = value_g
                path[(nx, ny)] = current
                open_list.append((f, (nx, ny)))
            elif value_g < brain.g[(nx, ny)]:
                brain.g[(nx, ny)] = value_g
                path[(nx, ny)] = current
                # visited.add(current)
                for index, (old_f, (x, y)) in enumerate(open_list):
                    if (x, y) == (nx, ny):
                        open_list[index] = (f, (nx, ny))
                        break
    return path
