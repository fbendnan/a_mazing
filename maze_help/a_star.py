from typing import List, Tuple, Dict, Optional, Set
from mazegen import MazeGenerator

Position = Tuple[int, int]
Walls = List[List[List[int]]]


class Brain:
    """
    Helper class implementing core operations for the A* pathfinding algorithm.

    This class is responsible for:
    - Finding valid neighboring cells
    - Computing heuristic distances
    - Selecting the node with the minimum f-score
    """

    def __init__(
        self,
        walls: Walls,
        height: int,
        width: int,
        g_cost: Dict[Position, int],
    ) -> None:
        """
        Initialize the Brain helper.

        Args:
            walls:
                3D structure describing maze walls.
                Format: grid[row][col] -> [N, E, S, W]
                where 1 = wall present, 0 = open.

            height:
                Number of rows in the maze.

            width:
                Number of columns in the maze.

            g_cost:
                Dictionary storing the distance from the start node
                to each visited node.
        """
        self.height: int = height
        self.width: int = width
        self.g_cost: Dict[Position, int] = g_cost
        self.walls: Walls = walls

    def find_neighbors(self, current: Position) -> List[Position]:
        """
        Return all accessible neighboring cells of a node.

        Args:
            current:
                Current cell coordinates (row, column).

        Returns:
            A list of reachable neighboring positions.
        """
        x, y = current
        neighbors: List[Position] = []

        # North
        if x > 0 and self.walls[x][y][0] == 0:
            neighbors.append((x - 1, y))

        # South
        if x < self.height - 1 and self.walls[x][y][2] == 0:
            neighbors.append((x + 1, y))

        # West
        if y > 0 and self.walls[x][y][3] == 0:
            neighbors.append((x, y - 1))

        # East
        if y < self.width - 1 and self.walls[x][y][1] == 0:
            neighbors.append((x, y + 1))

        return neighbors

    def heuristic(self, node: Position, goal: Position) -> int:
        """
        Compute the Manhattan distance heuristic.

        The Manhattan distance is appropriate for grid movement
        without diagonal steps.

        Args:
            node:
                Current node position.

            goal:
                Target node position.

        Returns:
            Estimated distance between node and goal.
        """
        x, y = node
        gx, gy = goal

        return abs(gx - x) + abs(gy - y)

    def min_f(
        self, open_list: List[Tuple[int, Position]]
    ) -> Optional[Tuple[int, Position]]:
        """
        Select the node with the lowest f-score.

        Args:
            open_list:
                List containing tuples of (f_score, position).

        Returns:
            The tuple with the smallest f_score or None if empty.
        """
        if not open_list:
            return None

        return min(open_list, key=lambda item: item[0])


def solver(maze: MazeGenerator) -> List[Position]:
    """
    Solve a maze using the A* pathfinding algorithm.

    The algorithm finds the shortest path from the maze entry
    to the maze exit using a heuristic-guided search.

    Args:
        maze:
            Maze object containing:
            - entry position
            - exit position
            - maze dimensions
            - wall structure

    Returns:
        A list of coordinates representing the shortest path
        from entry to exit.

        If no path exists, an empty list is returned.
    """

    walls: Walls = maze.get_solver_walls()

    g_cost: Dict[Position, int] = {}

    start: Position = maze.entry
    goal: Position = maze.exit

    g_cost[start] = 0

    brain = Brain(walls, maze.height, maze.width, g_cost)

    open_list: List[Tuple[int, Position]] = []
    visited: Set[Position] = set()
    parents: Dict[Position, Position] = {}

    start_h = brain.heuristic(start, goal)
    open_list.append((start_h, start))

    while open_list:

        result = brain.min_f(open_list)

        if result is None:
            break

        f_score, current = result
        open_list.remove((f_score, current))

        visited.add(current)

        if current == goal:
            break

        neighbors = brain.find_neighbors(current)

        for neighbor in neighbors:

            if neighbor in visited:
                continue

            new_g = brain.g_cost[current] + 1
            h = brain.heuristic(neighbor, goal)
            f = new_g + h

            if neighbor not in brain.g_cost:

                brain.g_cost[neighbor] = new_g
                parents[neighbor] = current
                open_list.append((f, neighbor))

            elif new_g < brain.g_cost[neighbor]:

                brain.g_cost[neighbor] = new_g
                parents[neighbor] = current

                for index, (old_f, pos) in enumerate(open_list):

                    if pos == neighbor:
                        open_list[index] = (f, neighbor)
                        break

    path: List[Position] = []
    node: Position = goal

    if node not in parents:
        return []

    while node != start:

        path.append(node)
        node = parents[node]

    path.append(start)
    path.reverse()

    return path
