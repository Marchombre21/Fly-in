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
from errors import NoPathFound, UnknownHub


class PathFinder():

    def __init__(self, hubs_dict: dict[str, Hub],
                 hashmap: dict[tuple[str, int], int]):
        self.hubs_dict: dict[str, Hub] = hubs_dict
        self.hashmap: dict[tuple[str, int], int] = hashmap
        self.came_from: dict[tuple[str, int], tuple[str, int]] = {}

    def reconstruct_path(self, node: tuple[str, int]) -> list[str]:
        """
        Return the list of nodes of the correct path from the start
        """
        name: str
        turn: int
        name, turn = node
        path = [name]
        self.hashmap[(name, turn)] += 1

        # I store the name and the turn for storage in the hashmap
        prev_name: str = name
        prev_turn: int = turn

        while node in self.came_from:
            node = self.came_from[node]
            name, turn = node

            # If the drone doesn't move, there is no connection to store
            if name != prev_name:
                self.hashmap[(name + '-' + prev_name, turn + 1)] += 1
                self.hashmap[(prev_name + '-' + name, turn + 1)] += 1

                # If the move_cost is 2 the connection is occupied 2 turns
                if prev_turn - turn == 2:
                    self.hashmap[(name + '-' + prev_name, turn + 2)] += 1
                    self.hashmap[(prev_name + '-' + name, turn + 2)] += 1
                    path.append(f'{name}-{prev_name}')

            # I store the drone presence in hashmap at that turn
            self.hashmap[(name, turn)] += 1
            path.append(name)
            prev_name = name
            prev_turn = turn

        # reverse result to get from beginning to end
        path.reverse()
        return path

    def a_star_algorithm(self, drone: Drone) -> list[str]:
        """
        The A* algorithm assign a cost to each hub and calculate the shortest
        path to the goal.
        The cost of a hub is defined by f(n) = g(n) + h(n) with

        - f(n): total cost to reach hub n -> Priority, the lower the better!
        - g(n): actual cost to reach hub n from start
        - h(n): heuristic (or estimated) cost to reach the goal from hub n
        """

        for hub in self.hubs_dict.values():
            if hub.role == "start_hub":
                hub_start: Hub = hub
                break

        # I initiate the path cost with the first hub and a cost of 0 (the
        # drone is actually on it)
        path_cost: dict[tuple[str, int], int] = {(hub_start.name, 0): 0}
        neighbors_list: list[tuple[int, int, tuple[str, int]]] = []
        turn: int = 0

        # I store a tuple in the neighbors_list containing f(n), followed by
        # the priority assigned to the hub, and finally a tuple with the
        # hub's name and the current round.
        heappush(neighbors_list, (hub_start.weight, 0, (hub_start.name, turn)))

        while len(neighbors_list) > 0:
            curr_datas: tuple[str, int]
            curr_hub_name: str

            # I select the hub with the lowest f(n)
            _, _, curr_datas = heappop(neighbors_list)
            curr_hub_name, turn = curr_datas

            try:
                curr_hub: Hub = self.hubs_dict[curr_hub_name]
            except KeyError:
                raise UnknownHub(
                    f"Unknown hub in neighbors_list: {curr_hub_name}")
            if curr_hub.zone == "blocked":
                continue

            # If the end is reached we have the shortest path to the goal
            if curr_hub.role == "end_hub":
                goal_path: list[str] = self.reconstruct_path(
                    (curr_hub_name, turn))
                return goal_path

            # I'm retrieving all the neighbors connected with the hub
            neighbors: list[Hub] = [
                self.hubs_dict[names] for names in curr_hub.connected_with
            ]

            # Check all possible neighbors of the current hub
            # and register new ones
            for neighbor in neighbors:
                mc: int = neighbor.move_cost

                # I check whether, on the next turn, the maximum number of
                # drones is already present on the adjacent tile or on
                # the connection
                if (self.hashmap[(neighbor.name, turn + mc)] >=
                    neighbor.max_drones or
                        self.hashmap[(curr_hub.name + '-' + neighbor.name,
                                      turn + 1)]
                        >= curr_hub.connected_with[neighbor.name]) or\
                        (mc > 1 and self.hashmap[(curr_hub.name + '-' +
                                                 neighbor.name,
                                                 turn + 2)] >=
                            curr_hub.connected_with[neighbor.name]):
                    continue

                # The new cost is equal to the cost up to that hub plus the
                # move_cost of the neighbor
                new_cost = path_cost[(curr_hub_name,
                                      turn)] + neighbor.move_cost

                # If the neighbor hasn't been visited yet, or if their last
                # visit was less expensive than this one, it's a potential path
                if (neighbor.name,
                        turn + mc) not in path_cost or new_cost < path_cost[(
                            neighbor.name, turn + mc)]:

                    # If it is a priority hub, it must be selected over a
                    # normal hub in the event of a tie in cost.
                    debuff: int = 0 if neighbor.zone == 'priority' else 1
                    path_cost[(neighbor.name, turn + mc)] = new_cost
                    heappush(neighbors_list,
                             (new_cost + neighbor.weight, debuff,
                              (neighbor.name, turn + mc)))
                    self.came_from[(neighbor.name,
                                    turn + mc)] = (curr_hub.name, turn)

            # I store the possibility of waiting one turn one the current hub
            if self.hashmap[curr_hub_name, turn + 1] < curr_hub.max_drones:
                new_cost = path_cost[(curr_hub_name, turn)] + 1
                if (curr_hub_name,
                        turn + 1) not in path_cost or new_cost < path_cost[(
                            curr_hub_name, turn + 1)]:

                    # Even though it's a priority hub, I don't want the drone
                    # to wait if there's a free neighbor
                    debuff = 1
                    path_cost[(curr_hub_name, turn + 1)] = new_cost
                    self.came_from[(curr_hub_name, turn + 1)] = (curr_hub_name,
                                                                 turn)
                    heappush(neighbors_list,
                             (new_cost + curr_hub.weight, debuff,
                              (curr_hub_name, turn + 1)))

        raise NoPathFound(f"No path for drone {drone.id}!")
