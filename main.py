from mazelib import Maze
from mazelib.generate.Prims import Prims
import random

def insert_teleportation_links_into_maze(maze, t):
    # Solve the maze to first get a solution for the shortest path
    solution = astar_solve(maze)

    # Do not insert teleportation links along the shortest path, to ensure the maze will still always be solveable
    cells_not_to_insert_solutions = solution.keys()

    all_empty_cells = []
    for rowIndex, row in enumerate(maze.grid):
        for columnIndex, cell in enumerate(row):
            # If empty and not
            if cell == 0 and (rowIndex, columnIndex) not in cells_not_to_insert_solutions:
                all_empty_cells.append((rowIndex, columnIndex))

    # Sample empty cells to get entrance and exits of teleportation links
    cells_to_add_teleportation_links = random.sample(all_empty_cells, t*2)

    # Create teleportation links between sampled empty cells.
    teleportation_links = dict()
    for i in range(0, t, 2):
        entrance_cell = cells_to_add_teleportation_links[t]
        exit_cell = cells_to_add_teleportation_links[t+1]

        teleportation_links[entrance_cell] = exit_cell

    return teleportation_links

def get_neighbours(maze, row, column, teleportation_links):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    possible_neighbours = [
        (row+rowOffset, column+columnOffset) for rowOffset, columnOffset in directions
    ]

    # Remove neighbours which are walls
    neighbours_without_walls = [(row, col) for (row, col) in possible_neighbours if maze.grid[row][column] == 0]

    # If neighbouring cell is a teleportation link, replace the neighbour with the exit cell of the link
    neighbours_with_teleportation_links_checked = [
        teleportation_links.get(neighbour, neighbour) for neighbour in neighbours_without_walls
    ]

    return neighbours_with_teleportation_links_checked

def get_maze_with_teleportation_links(n, t):
    m = Maze()
    m.generator = Prims(int(n / 2), int(n / 2))
    m.generate()
    m.generate_entrances(True, True)
    return m

def astar_solve(maze):
    solution = dict()
    return solution

m = get_maze_with_teleportation_links(10, 2)

