from collections import deque

from mazelib import Maze
from mazelib.generate.Prims import Prims
import random
import numpy


def insert_teleportation_links_into_maze(maze, t):
    """ Create a dictionary of teleportation links.

    :param maze: Maze object
    :param t: Number of teleportation links to create

    :return: Dictionary mapping entrance cell of a teleportation link to an exit cell
    """
    # Solve the maze to first get a solution for the shortest path
    (shortest_path, _steps) = breadth_first_search(maze, dict())

    # Do not insert teleportation links along the shortest path, to ensure the maze will still always be solvable
    cells_not_to_insert_links = shortest_path

    all_empty_cells = []
    for rowIndex, row in enumerate(maze.grid):
        for columnIndex, cell in enumerate(row):
            # If empty and not
            if cell == 0 and (rowIndex, columnIndex) not in cells_not_to_insert_links:
                all_empty_cells.append((rowIndex, columnIndex))

    # Sample empty cells to get entrance and exits of teleportation links
    cells_to_add_teleportation_links = random.sample(all_empty_cells, t * 2)

    # Create teleportation links between sampled empty cells.
    teleportation_links = dict()
    for i in range(0, t * 2, 2):
        entrance_cell = cells_to_add_teleportation_links[i]
        exit_cell = cells_to_add_teleportation_links[i + 1]

        teleportation_links[entrance_cell] = exit_cell

    return teleportation_links


def get_neighbours(maze, current_row, current_col, teleportation_links):
    """ Get neighbours in  maze.

    Gets all empty neighbours of cell. Where a neighbour contains a teleportation link, it will be replaced with
    the exit of the teleportation link.

    :param maze: Maze object
    :param current_row: Current row
    :param current_col: Current col
    :param teleportation_links: Dictionary of teleportation entrance to exit

    :return: List of neighbouring cells
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    height, width = len(maze.grid), len(maze.grid[0])

    neighbours = [
        (current_row + rowOffset, current_col + columnOffset) for rowOffset, columnOffset in directions
    ]
    if [cell for cell in neighbours if cell in teleportation_links]:
        pass

    # Remove out of bounds
    neighbours = [(row, col) for (row, col) in neighbours if 0 <= row < height and 0 <= col < width]

    # Remove neighbours which are walls and are not entrance/exits
    neighbours = [
        (row, col) for (row, col) in neighbours if maze.grid[row][col] == 0 or (row, col) in (maze.start, maze.end)]

    # If neighbouring cell is a teleportation link, replace the neighbour with the exit cell of the link
    neighbours = [teleportation_links.get(neighbour, neighbour) for neighbour in neighbours]
    return neighbours


def get_maze_with_teleportation_links(n, t):
    m = Maze()
    m.generator = Prims(int(n / 2), int(n / 2))
    m.generate()
    m.generate_entrances(True, True)

    teleportation_links = insert_teleportation_links_into_maze(m, t)

    return m, teleportation_links


def breadth_first_search(maze, teleportation_links):
    """Run breadth-first search on a given maze with teleportation links, to find a path from the start to the end.

    :param maze: Maze object
    :param teleportation_links: Dictionary of teleportation entrance cells to exit cells

    :return: Path from start to end, number of steps taken to find path
    :rtype: (list[(int, int)], int)
    """
    # Initial data structures
    frontier = deque()
    start_position = maze.start
    parent_nodes = dict()

    # Set starting nodes parent to None
    parent_nodes[start_position] = None

    # Add first cell to frontier
    frontier.append(start_position)

    steps = 0

    while len(frontier):
        steps += 1
        current = frontier.popleft()

        if current == maze.end:
            return reconstruct_solution(parent_nodes, maze.end), steps

        for neighbour in get_neighbours(maze, current[0], current[1], teleportation_links):
            if neighbour not in parent_nodes.keys():
                parent_nodes[neighbour] = current
                frontier.append(neighbour)

    return None, steps


def reconstruct_solution(previous_nodes, end_node):
    solution_path = []
    current = end_node

    while current is not None:
        solution_path.append(current)
        current = previous_nodes[current]

    solution_path.reverse()
    return solution_path


def run_algorithm_on_maze(n, t):
    m, teleportation_links = get_maze_with_teleportation_links(n, t)
    (solution, number_of_steps) = breadth_first_search(m, teleportation_links)
    if solution is None:
        raise "No solution was found for maze"

    return solution, number_of_steps


def get_data_for_task_2():
    samples_for_each_n_value = dict()
    n_values = (10, 15, 20, 25, 30)
    t = 2

    # Repeat each maze size a set number of times and take an average to get more consistent and generalizable results
    num_of_samples_for_each_size = 100

    for n in n_values:
        sample_time_steps = [run_algorithm_on_maze(n, t)[1] for _ in range(num_of_samples_for_each_size)]
        samples_for_each_n_value[n] = sample_time_steps

    for n, samples in samples_for_each_n_value.items():
        min_sample, q1, median, q3, max_sample = numpy.quantile(samples, [0, 0.25, 0.5, 0.75, 1])

        print(f'Data for size {n}')
        print(f'Median value: {median}')


def get_data_for_task_3():
    samples_for_each_t_value = dict()
    t_values = range(11)
    n = 30

    # Repeat each maze size a set number of times and take an average to get more consistent and generalizable results
    num_of_samples_for_each_size = 1000

    for t in t_values:
        sample_time_steps = [run_algorithm_on_maze(n, t)[1] for _ in range(num_of_samples_for_each_size)]
        samples_for_each_t_value[t] = sample_time_steps

    for t, samples in samples_for_each_t_value.items():
        min_sample, q1, median, q3, max_sample = numpy.quantile(samples, [0, 0.25, 0.5, 0.75, 1])

        print(f'Data for {t} teleportation links')
        print(f'Median value: {median}')


if __name__ == '__main__':
    get_data_for_task_3()
