# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    log_maker.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/24 17:05:11 by bfitte            #+#    #+#             #
#    Updated: 2026/03/24 17:05:12 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from drone import Drone


class LogMaker():
    def __init__(self, drones_list: list[Drone]):
        self.__drones_list: list[Drone] = drones_list

    def make_log(self):
        nb_turns: int = max([len(drone.path) for drone in self.__drones_list])
        with open('output.txt', 'a') as f:
            for i in range(nb_turns):
                first: bool = True
                for drone in self.__drones_list:
                    if i + 2 <= len(drone.path):
                        if drone.path[i] != drone.path[i + 1]:
                            if not first:
                                f.write(' ')
                            first = False
                            f.write(drone.id + '-' + drone.path[i + 1])
                f.write('\n')
