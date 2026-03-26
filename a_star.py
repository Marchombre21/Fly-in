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
from drone import Drone
from errors import NoPathFound


class PathFinder():

    def __init__(self, hubs_dict: dict[str, Hub],
                 hashmap: dict[tuple[str, int], list[Drone]]):
        self.hubs_dict: dict[str, Hub] = hubs_dict
        self.hashmap: dict[tuple[str, int], list[Drone]] = hashmap
        self.came_from: dict[tuple[str, int], tuple[str, int]] = {}

    def reconstruct_path(self, node: tuple, drone: Drone):
        """
        Return the list of nodes of the correct path from the start
        """
        name: str
        prev_name: str
        prev_turn: int
        turn: int
        name, turn = node
        path = [name]
        self.hashmap[(name, turn)].append(drone)
        prev_name = name
        prev_turn = turn
        while node in self.came_from:
            node = self.came_from[node]
            name, turn = node
            self.hashmap[(name + prev_name, turn + 1)].append(drone)
            self.hashmap[(prev_name + name, turn + 1)].append(drone)
            if prev_turn - turn == 2:
                self.hashmap[(name + prev_name, turn + 2)].append(drone)
                self.hashmap[(prev_name + name, turn + 2)].append(drone)
            self.hashmap[(name, turn)].append(drone)
            path.append(name)
            prev_name = name
        # reverse result to get from beginning to end
        path.reverse()
        return path

    def a_star_algorithm(self, drone: Drone) -> list[str]:
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

        # Register the precedent node of each newly accessed node

        for hub in self.hubs_dict.values():
            if hub.role == "start_hub":
                hub_start: Hub = hub
                break
        # Register the "cost" or progress already made g(n)
        # for each cell visited
        path_cost: dict[tuple[str, int], int] = {(hub_start.name, 0): 0}
        neighbors_list: list[tuple[int, int, tuple[str, int]]] = []
        turn: int = 0
        heappush(neighbors_list, (hub_start.weight, 0, (hub_start.name, turn)))
        while len(neighbors_list) > 0:
            curr_datas: tuple
            curr_hub_name: str
            _, _, curr_datas = heappop(neighbors_list)
            curr_hub_name, turn = curr_datas
            curr_hub: Hub | None = self.hubs_dict.get(curr_hub_name)
            if curr_hub.zone == "blocked":
                continue
            if curr_hub and curr_hub.role == "end_hub":
                goal_path: list[str] = self.reconstruct_path(
                    (curr_hub_name, turn), drone)
                return goal_path
            neighbors: list[Hub] = [
                self.hubs_dict[names] for names in curr_hub.connected_with
            ]
            # Check all possible neighbors of the current cell
            # and register new ones
            for neighbor in neighbors:
                mc: int = neighbor.move_cost
                # if drone.id == 'D1':
                #     print('name', neighbor.name)
                #     print('nb', len(self.hashmap[(neighbor.name, turn + mc)]))
                #     print('max', neighbor.max_drones)
                #     print('nb link', len(
                #         self.hashmap[(curr_hub.name + neighbor.name,
                #                       turn + 1)]))
                #     print('nb autor', curr_hub.connected_with[neighbor.name])
                if (len(self.hashmap[(neighbor.name, turn + mc)]) >=
                    neighbor.max_drones or len(
                        self.hashmap[(curr_hub.name + neighbor.name,
                                      turn + 1)])
                        >= curr_hub.connected_with[neighbor.name]) or\
                        (mc > 1 and len(self.hashmap[(curr_hub.name +
                                                      neighbor.name,
                                        turn + 2)]) >=
                            curr_hub.connected_with[neighbor.name]):
                    continue
                new_cost = path_cost[(curr_hub_name,
                                      turn)] + neighbor.move_cost
                if (neighbor.name,
                        turn + mc) not in path_cost or new_cost < path_cost[(
                            neighbor.name, turn + mc)]:
                    # if drone.id == 'D1':
                    #     print('name2', neighbor.name)
                    # if drone.id == 'D15':
                    #     print('nei name pass', neighbor.name)
                    debuff: int = 0 if neighbor.zone == 'priority' else 1
                    path_cost[(neighbor.name, turn + mc)] = new_cost
                    heappush(neighbors_list,
                             (new_cost + neighbor.weight, debuff,
                              (neighbor.name, turn + mc)))
                    # if mc == 2:
                    #     # self.came_from[(curr_hub_name + neighbor.name,
                    #     #                 turn + 1)] = (curr_hub.name, turn)
                    #     self.came_from[(neighbor.name, turn +
                    #                     mc)] = (curr_hub_name + neighbor.name,
                    #                             turn + 1)
                    # else:
                    self.came_from[(neighbor.name,
                                    turn + mc)] = (curr_hub.name, turn)
                    # I add one drone on the hub for the next turn
                    # self.hashmap[(neighbor.name, turn + mc)].append(drone)
                    # I add one drone on the connection between the hubs for
                    # this turn
                    # self.hashmap[(curr_hub.name + '-' + neighbor.name,
                    #          turn)].append(drone)
                    # print("Path_cost", path_cost)
                    # print("neighbors_list", neighbors_list)
                    # print("Came from", self.came_from)
                    # print('voisins après', neighbors_list, '\n')
            # if drone.id == 'D2':
            #     print(len(self.hashmap[(curr_hub_name, turn + 1)]))
            #     print(curr_hub.max_drones)
            #     print(curr_hub.name)
            if len(self.hashmap[curr_hub_name,
                                turn + 1]) < curr_hub.max_drones:
                new_cost = path_cost[(curr_hub_name, turn)] + 1
                # if drone.id == 'D2':
                #     print(new_cost)
                #     print(path_cost)
                # print(path_cost[(curr_hub_name, turn + 1)])
                if (curr_hub_name,
                        turn + 1) not in path_cost or new_cost < path_cost[(
                            curr_hub_name, turn + 1)]:
                    debuff = 0 if curr_hub.zone == 'priority' else 1
                    path_cost[(curr_hub_name, turn + 1)] = new_cost
                    self.came_from[(curr_hub_name, turn + 1)] = (curr_hub_name,
                                                                 turn)
                    heappush(neighbors_list,
                             (new_cost + curr_hub.weight, debuff,
                              (curr_hub_name, turn + 1)))
            # if len(neighbors_list) == 0:
            #     while len(neighbors_list) == 0:
            #         curr_hub_name, turn = self.came_from[curr_hub_name]
            #         curr_hub = hubs_dict.get(curr_hub_name)
            #         if not curr_hub:
            #             continue
            #         neighbors = [
            #             hubs_dict[names] for names in curr_hub.connected_with if
            #             (names, turn) not in path_cost
            #         ]
            #         if

        raise NoPathFound(f"No path for drone {drone.id}!")
