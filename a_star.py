# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    a_star.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/19 13:49:22 by bfitte            #+#    #+#             #
#    Updated: 2026/03/19 14:55:26 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#
from heapq import heappop, heappush
from hub_class import Hub
from simulation_engine import SimEngine

# def get_neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
#     """
#     Returns the list of neighboring cells that can be accessed
#     from the current cell
#     """
#     row, col = cell
#     cell_walls: int = Border(self.maze[row][col])
#     neighbors: list[tuple[int, int]] = []

#     # If no NORTH wall -> there's a NORTH neighbor (checking diff 0001)
#     if not (cell_walls & Border.NORTH):
#         neighbors.append((row - 1, col))

#     # If no SOUTH wall -> there's a SOUTH neighbor (checking diff 0010)
#     if not (cell_walls & Border.SOUTH):
#         neighbors.append((row + 1, col))

#     # If no WEST wall -> there's a WEST neighbor (checking diff 0100)
#     if not (cell_walls & Border.WEST):
#         neighbors.append((row, col - 1))

#     # If no EAST wall -> there's a EAST neighbor (checking diff 1000)
#     if not (cell_walls & Border.EAST):
#         neighbors.append((row, col + 1))
#     return neighbors

# @staticmethod
# def h(cell1: tuple[int, int], cell2: tuple[int, int]) -> int:
#     """
#     The Heuristic function chosen here is the
#     [Manhattan Distance](https://en.wikipedia.org/wiki/Taxicab_geometry)

#     Calculate the distance between 2 points on a grid by summing the
#     absolute differences in their x and y coordinates
#     """
#     x1, y1 = cell1
#     x2, y2 = cell2
#     return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(node: str, came_from: dict[str, str]) -> list[str]:
    """
    Return the list of nodes of the correct path from the start
    """
    path = [node]
    while node in came_from:
        # print(node)
        node = came_from[node]
        path.append(node)
    # reverse result to get from beginning to end
    path.reverse()
    return path


def a_star_algorithm(sim: SimEngine) -> list[str]:
    """
    The A* algorithm assign a cost to each cell and calculate the shortest
    SolutionPath from this
    The cost of a cell is defined by
    ```math
    f(n) = g(n) + h(n)
    ```
    with
    - f(n): total cost to reach cell n -> Priority, the lower the better!
    - g(n): actual cost to reach cell n from start
    - h(n): heuristic (or estimated) cost to reach the goal from cell n
    """

    # # open_paths: list[(f_score, node)] is the list of cells path opened to
    # # explore, sorted by priority (f_score)
    # open_paths: list[tuple[int,
    #                         tuple[int,
    #                                 int]]] = [(self.h(self.start,
    #                                                 self.end), self.start)]

    hubs_dict: dict[str, Hub] = sim.hubs

    # Register the precedent node of each newly accessed node
    came_from: dict[str, str] = {}
    for hub in hubs_dict.values():
        if hub.role == "start_hub":
            hub_start: Hub = hub
            break
    # Register the "cost" or progress already made g(n)
    # for each cell visited
    path_cost: dict[str, int] = {hub_start.name: 0}
    neighbors_list: list[tuple[int, str]] = []

    for names in hub_start.connected_with.keys():
        came_from[names] = hub_start.name
        path_cost.update({names: hubs_dict.get(names).weight})
        heappush(neighbors_list, (0 + hubs_dict.get(names).weight, names))
    while len(neighbors_list) > 0:
        curr_hub_name: str
        _, curr_hub_name = heappop(neighbors_list)
        # print("curr_hub", curr_hub_name)
        curr_hub: Hub | None = hubs_dict.get(curr_hub_name)
        # print("role", curr_hub.role)
        if curr_hub and curr_hub.role == "end_hub":
            goal_path: list[str] = reconstruct_path(curr_hub_name, came_from)
            return goal_path
        neighbors: list[Hub] = [
            hubs_dict.get(names) for names in curr_hub.connected_with.keys()
        ]

        # Check all possible neighbors of the current cell
        # and register new ones
        for neighbor in neighbors:
            # print('neighbors', neighbor.name)
            new_cost = path_cost.get(curr_hub_name, 10000) + neighbor.weight
            if neighbor.name not in path_cost or new_cost < path_cost[neighbor.name]:
                path_cost[neighbor.name] = new_cost
                heappush(neighbors_list, (new_cost, neighbor.name))
                came_from[neighbor.name] = curr_hub.name
                # print("Path_cost", path_cost)
                # print("Came from", came_from)

    # raise NoSolutionError("No solution for this maze!")
