from typing import List, Tuple, Dict, Optional, Set


class Brain:
    """
    Helper class that implements core logic for the A* pathfinding algorithm.

    It handles:
    - neighbor discovery
    - heuristic calculation
    - selecting the node with minimum f-score
    """

    def __init__(
        self,
        wall: List[List[List[int]]],
        height: int,
        width: int,
        g: Dict[Tuple[int, int], int],
    ) -> None:
        """
        Initialize the Brain object.

        Args:
            wall: 3D list describing the walls of the maze.
            height: Number of rows in the maze.
            width: Number of columns in the maze.
            g: Dictionary storing the cost from start to each node.
        """
        self.height: int = height
        self.width: int = width
        self.g: Dict[Tuple[int, int], int] = g
        self.wall: List[List[List[int]]] = wall

    def abc(self, num: int) -> int:
        """
        Return the absolute value of a number.

        Args:
            num: Input integer.

        Returns:
            Absolute value of num.
        """
        if num < 0:
            num = -num
        return num

    def found_neighbor(self, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Find accessible neighboring cells for a given node.

        Args:
            current: Current node position (row, column).

        Returns:
            List of valid neighboring coordinates.
        """
        x, y = current
        neighbor: List[Tuple[int, int]] = []

        if x > 0 and self.wall[x][y][0] == 0:
            neighbor.append((x - 1, y))

        if x < self.height - 1 and self.wall[x][y][2] == 0:
            neighbor.append((x + 1, y))

        if y > 0 and self.wall[x][y][3] == 0:
            neighbor.append((x, y - 1))

        if y < self.width - 1 and self.wall[x][y][1] == 0:
            neighbor.append((x, y + 1))

        return neighbor

    def heuristic(self, node: Tuple[int, int], goal: Tuple[int, int]) -> int:
        """
        Compute the Manhattan distance heuristic.

        Args:
            node: Current node (row, column).
            goal: Goal node (row, column).

        Returns:
            Estimated distance from node to goal.
        """
        row, col = goal
        x, y = node
        h = self.abc(col - y) + self.abc(row - x)
        return h

    def min_f(
        self, lst: List[Tuple[int, Tuple[int, int]]]
    ) -> Optional[Tuple[int, Tuple[int, int]]]:
        """
        Find the node with the minimum f-score.

        Args:
            lst: List of (f_score, node) tuples.

        Returns:
            Tuple containing the smallest f-score and its node,
            or None if the list is empty.
        """
        if not lst:
            return None
        f = min(lst, key=lambda t: t[0])
        return f


def solver(maze) -> List[Tuple[int, int]]:
    """
    Solve the maze using the A* pathfinding algorithm.

    Args:
        maze: Maze object containing entry, exit, and wall structure.

    Returns:
        A list of coordinates representing the shortest path
        from entry to exit. Returns an empty list if no path exists.
    """

    wall: List[List[List[int]]] = maze.get_solver_walls()

    g: Dict[Tuple[int, int], int] = {}

    start: Tuple[int, int] = maze.entry
    goal: Tuple[int, int] = maze.exit

    g[start] = 0

    brain = Brain(wall, maze.height, maze.width, g)

    open_list: List[Tuple[int, Tuple[int, int]]] = []
    visited: Set[Tuple[int, int]] = set()
    path: Dict[Tuple[int, int], Tuple[int, int]] = {}

    h = brain.heuristic(start, goal)
    open_list.append((h, start))

    while open_list:
        result = brain.min_f(open_list)
        if result is None:
            break

        f_val, current = result
        open_list.remove((f_val, current))
        visited.add(current)

        if current == goal:
            break

        neighbors = brain.found_neighbor(current)

        for neighbor in neighbors:
            nx, ny = neighbor

            if (nx, ny) in visited:
                continue

            value_g = brain.g[current] + 1
            h = brain.heuristic((nx, ny), goal)
            f = h + value_g

            if (nx, ny) not in brain.g:
                brain.g[(nx, ny)] = value_g
                path[(nx, ny)] = current
                open_list.append((f, (nx, ny)))

            elif value_g < brain.g[(nx, ny)]:
                brain.g[(nx, ny)] = value_g
                path[(nx, ny)] = current

                for index, (old_f, (x, y)) in enumerate(open_list):
                    if (x, y) == (nx, ny):
                        open_list[index] = (f, (nx, ny))
                        break

    final_path: List[Tuple[int, int]] = []
    node = goal

    if node not in path:
        return []

    while node != start:
        final_path.append(node)
        node = path[node]

    final_path.append(start)
    final_path.reverse()

    return final_path
