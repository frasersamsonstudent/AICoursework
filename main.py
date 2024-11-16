from queue import PriorityQueue

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

def get_neighbours(maze, current_row, current_col, teleportation_links):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    height, width = len(maze.grid), len(maze.grid[0])

    possible_neighbours = [
        (current_row+rowOffset, current_col+columnOffset) for rowOffset, columnOffset in directions
    ]

    # Remove out of bounds
    neighbours_in_bounds = [(row, col) for (row, col) in possible_neighbours if 0 <= row < height and 0 <= col < width]

    # Remove neighbours which are walls and are not entrance/exits
    neighbours_without_walls = [
        (row, col) for (row, col) in neighbours_in_bounds if maze.grid[row][col] == 0 or (row, col) in (maze.start, maze.end)]

    # If neighbouring cell is a teleportation link, replace the neighbour with the exit cell of the link
    neighbours_with_teleport_replacements = [
        teleportation_links.get(neighbour, neighbour) for neighbour in neighbours_without_walls
    ]

    print(f'Neighbours of ({current_row}, {current_col}): {neighbours_with_teleport_replacements}')
    return neighbours_with_teleport_replacements

def get_maze_with_teleportation_links(n, t):
    m = Maze()
    m.generator = Prims(int(n / 2), int(n / 2))
    m.generate()
    m.generate_entrances(True, True)

    teleportation_links = dict()

    return m, teleportation_links

def h(neighbour, end):
    return 0

def astar_solve(maze, teleportation_links):
    print(maze)
    frontier = PriorityQueue()
    start_position = maze.start
    parent_nodes = dict()
    distance = dict()

    parent_nodes[start_position] = None
    distance[start_position] = 0
    frontier.put((0, start_position))

    while frontier:
        current = frontier.get()[1]

        if current == maze.end:
            return parent_nodes

        for neighbour in get_neighbours(maze, current[0], current[1], teleportation_links ):
            if neighbour not in parent_nodes.keys():
                parent_nodes[neighbour] = current
                distance[neighbour] = distance[current] + 1

                f_value =  distance[neighbour] + h(neighbour, maze.end)
                frontier.put((f_value, neighbour))

    print(maze.grid[start_position[0]][start_position[1]])
    frontier.put((0, start_position))



    return None

def reconstruct_solution(previous_nodes, end_node):
    solution_path = []
    current = end_node

    while current is not None:
        solution_path.append(current)
        current = previous_nodes[current]

    solution_path.reverse()
    return solution_path

m, teleportation_links = get_maze_with_teleportation_links(10, 2)
solution = astar_solve(m, teleportation_links)
if solution is None:
    raise "No solution was found for maze"

solution_path = reconstruct_solution(solution, m.end)
print(solution_path)
