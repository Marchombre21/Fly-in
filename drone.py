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

from arcade import Sprite, Text


class Drone:

    def __init__(self, id: int) -> None:
        self.__path: list[str] = []
        self.__finish: bool = False
        self.__actual_location: str
        self.__on_connection: list[tuple[float, float]] | None = None
        self.__two_turns: bool = False
        self.__len_connection: int
        self.__sprite: Sprite
        self.__id: str = 'D' + str(id + 1)
        self.text: Text

    @property
    def id(self) -> str:
        return self.__id

    @property
    def len_connection(self) -> int:
        return self.__len_connection

    @property
    def two_turns(self) -> bool:
        return self.__two_turns

    @two_turns.setter
    def two_turns(self, new: bool) -> None:
        self.__two_turns = new

    @property
    def actual_location(self) -> str:
        return self.__actual_location

    @actual_location.setter
    def actual_location(self, location: str) -> None:
        self.__actual_location = location

    @property
    def finish(self) -> bool:
        return self.__finish

    @finish.setter
    def finish(self, finished: bool) -> None:
        self.__finish = finished

    @property
    def on_connection(self) -> list[tuple[float, float]] | None:
        return self.__on_connection

    @on_connection.setter
    def on_connection(self,
                      connection: list[tuple[float, float]] | None) -> None:
        if connection:
            self.__len_connection = len(connection)
        else:
            self.__len_connection = 0
        self.__on_connection = connection

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    @sprite.setter
    def sprite(self, new_sprite: Sprite) -> None:
        self.__sprite = new_sprite

    @property
    def path(self) -> list[str]:
        return self.__path

    @path.setter
    def path(self, path_list: list[str]) -> None:
        self.__path = path_list
        self.__actual_location = path_list[0]
