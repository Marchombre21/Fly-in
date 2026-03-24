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
from drone import Drone


def reconstruct_path(node: str, came_from: dict[str, str]) -> list[str]:
    """
    Return the list of nodes of the correct path from the start
    """
    name: str
    name, _ = node
    path = [name]
    while node in came_from:
        # print(node)
        node = came_from[node]
        name, _ = node
        path.append(name)
    # reverse result to get from beginning to end
    path.reverse()
    return path


def a_star_algorithm(sim: SimEngine, drone: Drone) -> list[str]:
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
    neighbors_list: list[tuple[int, int, tuple[str, int]]] = []
    turn: int = 0
    heappush(neighbors_list, (hub_start.weight, 0, (hub_start.name, turn)))
    hashmap: dict[tuple[str, int], list[Drone]] = sim.hashmap

    while len(neighbors_list) > 0:
        curr_datas: tuple
        curr_hub_name: str
        # curr_turn: int
        # print(neighbors_list)
        _, _, curr_datas = heappop(neighbors_list)
        # print('DATAS', curr_datas)
        curr_hub_name, turn = curr_datas
        # print("curr_hub", curr_hub_name)
        # print(turn)
        curr_hub: Hub | None = hubs_dict.get(curr_hub_name)
        # print("weight:", curr_hub.weight)
        if curr_hub.zone == "blocked":
            continue
        if curr_hub and curr_hub.role == "end_hub":
            goal_path: list[str] = reconstruct_path((curr_hub_name, turn),
                                                    came_from)
            return goal_path
        neighbors: list[Hub] = [
            hubs_dict[names] for names in curr_hub.connected_with
            if (names, turn - 1) not in path_cost
        ]
        # Check all possible neighbors of the current cell
        # and register new ones
        path_found: bool = True if len(neighbors) == 0 else False
        while not path_found:
            for neighbor in neighbors:
                mc: int = neighbor.move_cost
                # print('neighbor', neighbor.name)
                # print('nb', hashmap[(neighbor.name, turn)])
                # print('max drones', neighbor.max_drones)
                # print('drones lien',
                #       hashmap[(curr_hub.name + neighbor.name, turn - 1)])
                # print('lien autorisés', curr_hub.connected_with[neighbor.name])
                # print(path_cost)
                # print('nb', hashmap[(neighbor.name, turn + mc)])
                # print('max', neighbor.max_drones)
                # print('nb connexion', hashmap[(curr_hub.name + neighbor.name, turn)])
                # print('nb max', curr_hub.connected_with[neighbor.name])
                # print('mc', mc)
                # print('connexion + 1', hashmap[(curr_hub.name + neighbor.name, turn + 1)])
                if (len(hashmap[(neighbor.name, turn + mc)]) >= neighbor.max_drones
                        or len(hashmap[(curr_hub.name + '-' + neighbor.name, turn)])
                        >= curr_hub.connected_with[neighbor.name]) or\
                        (mc > 1 and len(hashmap[(curr_hub.name + '-' + neighbor.name,
                                        turn + 1)]) >=
                            curr_hub.connected_with[neighbor.name]):
                    continue
                # print('neighbor arrivée', neighbor.name, '\n')
                # print('Path', path_cost, '\n')
                # print('name', curr_hub_name, '\n')
                # print('turn', turn, '\n')
                # print('voisins', neighbors_list, '\n')
                new_cost = path_cost[(curr_hub_name,
                                      turn)] + neighbor.move_cost
                if (neighbor.name,
                        turn + mc) not in path_cost or new_cost < path_cost[(
                            neighbor.name, turn + mc)]:
                    debuff: int = 0 if neighbor.zone == 'priority' else 1
                    path_found = True
                    path_cost[(neighbor.name, turn + mc)] = new_cost
                    heappush(neighbors_list,
                             (new_cost + neighbor.weight, debuff,
                              (neighbor.name, turn + mc)))
                    if mc == 2:
                        came_from[(curr_hub_name + neighbor.name,
                                   turn + 1)] = (curr_hub.name, turn)
                        came_from[(neighbor.name, turn +
                                   mc)] = (curr_hub_name + neighbor.name,
                                           turn + 1)
                    else:
                        came_from[(neighbor.name, turn + mc)] = (curr_hub.name,
                                                                 turn)
                    # I add one drone on the hub for the next turn
                    hashmap[(neighbor.name, turn + mc)].append(drone)
                    # I add one drone on the connection between the hubs for
                    # this turn
                    hashmap[(curr_hub.name + '-' + neighbor.name,
                             turn)].append(drone)
                    # print("Path_cost", path_cost)
                    # print("neighbors_list", neighbors_list)
                    # print("Came from", came_from)
                    # print('voisins après', neighbors_list, '\n')
            if not path_found:
                hashmap[(curr_hub_name, turn + 1)].append(drone)
                came_from[(curr_hub_name, turn + 1)] = (curr_hub_name, turn)
                path_cost[(curr_hub_name,
                           turn + 1)] = path_cost[(curr_hub_name, turn)]
                turn += 1
    # raise NoSolutionError("No solution for this maze!")
