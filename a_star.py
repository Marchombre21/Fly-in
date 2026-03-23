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

    hubs_dict: dict[str, Hub] = sim.hubs

    # Register the precedent node of each newly accessed node
    came_from: dict[tuple[str, int], tuple[str, int]] = {}
    for hub in hubs_dict.values():
        if hub.role == "start_hub":
            hub_start: Hub = hub
            break
    # Register the "cost" or progress already made g(n)
    # for each cell visited
    path_cost: dict[tuple[str, int], int] = {(hub_start.name, 0): 0}
    neighbors_list: list[tuple[int, str]] = []
    turn: int = 0
    heappush(neighbors_list, (hub_start.weight, hub_start.name))
    hashmap: dict[tuple[str, int], int] = sim.hashmap

    while len(neighbors_list) > 0:
        curr_hub_name: str
        _, curr_hub_name = heappop(neighbors_list)
        # print("curr_hub", curr_hub_name)
        curr_hub: Hub | None = hubs_dict.get(curr_hub_name)
        # print("weight:", curr_hub.weight)
        if curr_hub.zone == "blocked":
            continue
        if curr_hub and curr_hub.role == "end_hub":
            goal_path: list[str] = reconstruct_path(curr_hub_name, came_from)
            return goal_path
        neighbors: list[Hub] = [hubs_dict[names] for names in curr_hub.connected_with]

        # Check all possible neighbors of the current cell
        # and register new ones
        turn += 1
        for neighbor in neighbors:
            # print("neighbors", neighbor.name)
            if (
                hashmap[(neighbor.name, turn)] >= neighbor.max_drones
                or hashmap[(curr_hub.name + neighbor.name, turn - 1)]
                >= curr_hub.connected_with[neighbor.name]
            ):
                continue
            # J'en suis là, il faut que je continue d'ajouter les vérifications liées à la
            # hashmap.
            new_cost = path_cost[(curr_hub_name, turn - 1)] + neighbor.move_cost
            if (neighbor.name, turn) not in path_cost or new_cost < path_cost[
                (neighbor.name, turn)
            ]:
                path_cost[(neighbor.name, turn)] = new_cost
                heappush(neighbors_list, (new_cost + neighbor.weight, neighbor.name))
                came_from[(neighbor.name, turn)] = (curr_hub.name, turn - 1)
                # I add one drone on the hub for the next turn
                hashmap[(neighbor.name, turn)] += 1
                # I add one drone on the connection between the hubs for
                # this turn
                hashmap[(curr_hub.name + neighbor.name, turn - 1)] += 1
                # print("Path_cost", path_cost)
                # print("neighbors_list", neighbors_list)
                # print("Came from", came_from)

    # raise NoSolutionError("No solution for this maze!")
