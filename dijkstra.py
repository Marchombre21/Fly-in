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


def dijkstra(hub_list: dict[str, Hub], dest_name: str) -> None:
    pq: list[tuple[int, str]] = []
    hub_list[dest_name].weight = 0
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

            if curr_weight + current_hub.move_cost < hub_n.weight:
                hub_n.weight = curr_weight + current_hub.move_cost
                heappush(pq, (hub_n.weight, neighbor_name))
