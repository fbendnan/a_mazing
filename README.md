# A-Maze-ing

*This project has been created as part of the 42 curriculum by \<fbendnan\>, \<cramadan\>.*

---

# Description

**A-Maze-ing** is a project that focuses on generating and solving mazes using different algorithms.  
The objective is to design a flexible program capable of generating a maze, displaying it in the terminal, and solving it using pathfinding techniques.

The maze is represented as a grid of cells. Each cell initially contains four walls (North, East, South, West).  
Maze generation algorithms progressively remove walls between neighboring cells to create valid paths from the **entry** to the **exit**.

This project emphasizes:

- Algorithm design and implementation
- Object-oriented programming
- Code modularity and reusability
- Configuration-based execution
- Terminal visualization

---

# Instructions

## Requirements

- Python 3.10 or higher
- Linux environment (recommended)

---

## Installation

Clone the repository:

```bash
git clone <repository_link>
cd a-maze-ing
```

---

## Running the Program

You can run the program using:

```bash
python3 main.py config.json
```

Or with the Makefile:

```bash
make run
```

---

## Makefile Commands

```bash
make run      # run the program
make clean    # remove temporary files
make fclean   # full clean
```

---

# Configuration File Structure

The program uses a **JSON configuration file** to control the maze generation.

Example configuration:

```json
{
  "ALGO": "PRIM",
  "HEIGHT": 20,
  "WIDTH": 20,
  "ENTRY": [0, 0],
  "EXIT": [19, 19],
  "SEED": 42,
  "PERFECT": true
}
```

### Parameters

| Parameter | Description |
|----------|-------------|
| ALGO | Maze generation algorithm (`PRIM` or `DFS`) |
| HEIGHT | Height of the maze |
| WIDTH | Width of the maze |
| ENTRY | Entry coordinates `[x, y]` |
| EXIT | Exit coordinates `[x, y]` |
| SEED | Optional seed for deterministic maze generation |
| PERFECT | If `true`, the maze will have only one solution |

---

# Maze Generation Algorithms

## Prim's Algorithm

Prim’s algorithm is adapted to generate mazes by progressively removing walls between cells.

Steps:

1. Start with a grid full of walls
2. Choose a starting cell
3. Add its neighboring walls to a list
4. Randomly choose a wall
5. If the wall separates a visited cell from an unvisited cell:
   - Remove the wall
   - Mark the new cell as visited
6. Repeat until all cells are connected

### Why We Chose Prim's Algorithm

Prim’s algorithm generates **well-balanced mazes** with many branching paths.  
It also guarantees the generation of a **perfect maze**, meaning there is exactly **one unique path between any two cells**.

---

## Depth-First Search (DFS)

DFS is another classic algorithm used for maze generation.

Steps:

1. Start from an initial cell
2. Visit a random unvisited neighbor
3. Remove the wall between the two cells
4. Continue recursively
5. If a cell has no unvisited neighbors, backtrack to the previous cell

DFS often produces **long corridors and deep paths**, creating a different maze style compared to Prim’s algorithm.

---

# Maze Solving

The project includes a maze solver based on the **A\* (A Star) algorithm**.

A\* is a pathfinding algorithm that finds the **shortest path** between the entry and exit using a heuristic evaluation.

It combines:

- The cost from the start node
- A heuristic estimate of the remaining distance

This makes it efficient and widely used in pathfinding systems.

---

# Code Reusability

The code was designed with modularity in mind so that components can be reused easily.

## MazeGenerator

The `MazeGenerator` class acts as a controller that selects the maze generation algorithm based on the configuration file.

New algorithms can easily be added without modifying the core logic.

---

## Algorithm Classes

Each algorithm is implemented independently:

- `PrimGenerator`
- `DFSGenerator`

This design allows:

- easy extension
- clear separation of responsibilities
- maintainable code

---

## Grid Structure

The grid and cell representation can also be reused for:

- other maze generation algorithms
- different pathfinding algorithms
- graphical visualization tools

---

# Advanced Features

This project includes several advanced features:

- Multiple maze generation algorithms
- Maze solving using A\*
- Configurable parameters via JSON
- Deterministic maze generation using seeds
- Terminal visualization of the maze

---

# Team and Project Management

## Team Members

| Name | Login | Role |
|-----|------|------|
| Fatima-Zahra Bendnane | fbendnan | Prim algorithm, parsing, display, Makefile |
| Chaimae Ramadan | cramadan | A* solver, DFS algorithm, output file |

---

## Project Planning

At the beginning of the project, tasks were divided between the two team members to allow parallel development:

- Maze generation algorithms
- Maze solving algorithm
- Configuration parsing
- Display implementation
- Output file generation
- Build automation with Makefile

Each component was tested individually before integration into the final program.

---

## Tools Used

- Python
- Git
- GitHub
- Linux Terminal
- Makefile
- VS Code

---

## What Worked Well

- Clear task distribution between team members
- Modular and maintainable code structure
- Independent development of algorithms

---

## What Could Be Improved

- More automated testing
- Additional visualization options
- More maze generation algorithms

---

# Resources

The following resources were used to understand maze algorithms and pathfinding:

- https://en.wikipedia.org/wiki/Maze_generation_algorithm
- https://en.wikipedia.org/wiki/Prim%27s_algorithm
- https://en.wikipedia.org/wiki/Depth-first_search
- https://en.wikipedia.org/wiki/A*_search_algorithm

---

# Use of AI

AI tools were used to:

- Improve documentation
- Structure the README file
- Clarify algorithm explanations
- Review code style and documentation