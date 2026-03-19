# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    drone.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/19 09:37:54 by bfitte            #+#    #+#             #
#    Updated: 2026/03/19 09:38:54 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from hub_class import Hub


class Drone():
    def __init__(self, actual_hub: Hub):
        self.__hub: Hub = actual_hub

    @property
    def hub(self) -> Hub:
        return self.__hub
