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

class Drone():
    def __init__(self):
        self.__path: list[str] = []

    @property
    def path(self) -> list[str]:
        return self.__path

    @path.setter
    def path(self, path_list: list[str]) -> None:
        self.__path = path_list
