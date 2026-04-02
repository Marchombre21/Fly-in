# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    dijkstra.py                                        :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/19 13:50:20 by bfitte            #+#    #+#             #
#    Updated: 2026/03/19 13:50:21 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from hub_class import Hub
from heapq import heappop, heappush
from errors import NoPathFound


class Dijkstra:

    @staticmethod
    def dijkstra(hub_list: dict[str, Hub], dest_name: str) -> None:
        """Dijkstra's algorithm is an algorithm for finding the shortest paths
        between nodes in a weighted graph
        """

        # The priority queue which contains all neighbors with their weight
        # (the cost from the goal)
        pq: list[tuple[int, str]] = []
        hub_list[dest_name].weight = 0
        start_hub_reached: bool = False
        heappush(pq, (0, dest_name))

        while pq:
            curr_weight: int
            hub_name: str
            curr_weight, hub_name = heappop(pq)
            current_hub: Hub = hub_list[hub_name]

            if curr_weight > current_hub.weight:
                continue

            for neighbor_name in current_hub.connected_with:
                hub_n: Hub = hub_list[neighbor_name]

                if hub_n.zone == 'blocked':
                    continue

                # I register the neighbor if the actual weight to reach the
                # goal plus the move_cost to reach the actual hub is less
                # expensive than the actual neighbor's weight
                if curr_weight + current_hub.move_cost < hub_n.weight:
                    if hub_n.role == 'start_hub':
                        start_hub_reached = True
                    hub_n.weight = curr_weight + current_hub.move_cost
                    heappush(pq, (hub_n.weight, neighbor_name))
        if not start_hub_reached:
            raise NoPathFound("The destination can't be reached.")
