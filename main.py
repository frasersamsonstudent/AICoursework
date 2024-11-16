from collections import deque

from mazelib import Maze
from mazelib.generate.Prims import Prims
import random


def insert_teleportation_links_into_maze(maze, t):
    # Solve the maze to first get a solution for the shortest path
    shortest_path = breadth_first_search(maze, dict())

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
    frontier = deque()
    start_position = maze.start
    parent_nodes = dict()

    parent_nodes[start_position] = None
    frontier.append(start_position)

    while frontier:
        current = frontier.popleft()

        if current == maze.end:
            return reconstruct_solution(parent_nodes, maze.end)

        for neighbour in get_neighbours(maze, current[0], current[1], teleportation_links):
            if neighbour not in parent_nodes.keys():
                parent_nodes[neighbour] = current
                frontier.append(neighbour)

    return None


def reconstruct_solution(previous_nodes, end_node):
    solution_path = []
    current = end_node

    while current is not None:
        solution_path.append(current)
        current = previous_nodes[current]

    solution_path.reverse()
    return solution_path


if __name__ == '__main__':
    m, teleportation_links = get_maze_with_teleportation_links(10, 2)
    print(m)
    print("teleportation links", teleportation_links)
    solution = breadth_first_search(m, teleportation_links)
    if solution is None:
        raise "No solution was found for maze"

    print('\n'.join([str(cell) for cell in solution]))
