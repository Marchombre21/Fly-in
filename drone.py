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

from arcade import Sprite
from arcade import SpriteList


class Drone():
    def __init__(self):
        self.__path: list[str] = []
        self.__finish: bool = False
        self.__actual_location: str
        self.__on_connection: SpriteList | None = None
        # self.__sprite: Sprite

    @property
    def actual_location(self) -> str:
        return self.__actual_location

    @actual_location.setter
    def actual_location(self, location: str) -> None:
        self.__actual_location = location

    @property
    def finish(self):
        return self.__finish

    @finish.setter
    def finish(self, finished: bool):
        self.__finish = finished

    @property
    def on_connection(self) -> SpriteList:
        return self.__on_connection

    @on_connection.setter
    def on_connection(self, connection: SpriteList) -> None:
        self.__on_connection = connection

    @property
    def sprite(self):
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: Sprite):
        self.__sprite = new_sprite

    @property
    def path(self) -> list[str]:
        return self.__path

    @path.setter
    def path(self, path_list: list[str]) -> None:
        self.__path = path_list
        self.__actual_location = path_list[0]
