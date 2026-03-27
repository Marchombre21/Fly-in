# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    field_engine.py                                    :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/13 09:32:41 by bfitte            #+#    #+#             #
#    Updated: 2026/03/13 09:32:42 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from hub_class import Hub
from drone import Drone
from collections import defaultdict
from errors import (SimError, FormatConnectionError, ConfigError,
                    NumberLinksError)


class SimEngine():

    def __init__(self):
        self.__hubs: dict[str, Hub] = {}
        self.__nb_drones: int = 0
        self.__hashmap: dict[tuple[str, int], int] = defaultdict(int)

    @property
    def hashmap(self) -> dict[tuple[str, int], int]:
        return self.__hashmap

    @property
    def nb_drones(self):
        return self.__nb_drones

    @nb_drones.setter
    def nb_drones(self, nb: int):
        if not isinstance(nb, int) or nb < 0:
            SimError(
                'The drones number must be an integer and can\'t be a negative'
                ' value.')
        self.__nb_drones = nb

    @property
    def hubs(self):
        return self.__hubs

    def check_coordonates(self):
        """If any coordinates are negative, I change them all to bring
        everything back to a positive base
        """

        min_x: int = min([hub.x for hub in self.__hubs.values()])
        min_y: int = min([hub.y for hub in self.__hubs.values()])
        if min_x < 0:
            offset: int = abs(min_x)
            for hub in self.hubs.values():
                hub.x += offset
        if min_y < 0:
            offset: int = abs(min_y)
            for hub in self.hubs.values():
                hub.y += offset

    def add_hub(self, hub_dict: dict[str, str]) -> None:

        name: str = hub_dict.get('name')
        x: str = hub_dict.get('x')
        y: str = hub_dict.get('y')
        for hub in self.__hubs.values():
            if hub.name == name:
                raise ConfigError('All hubs must have different names.')
            if str(hub.x) == x and str(hub.y) == y:
                raise ConfigError(
                    'Two hubs can\'t be at the same coordonates.')
        self.__hubs[name] = Hub(**hub_dict)
        if len([
                hub for hub in self.__hubs.values() if hub.role == 'start_hub'
        ]) > 1 or len(
            [hub
             for hub in self.__hubs.values() if hub.role == 'end_hub']) > 1:
            raise ConfigError('There cannot be more than one start or end.')

    def create_connection(self, link: str):

        # It can't have more than one space (in case of metadatas)
        space_count: int = link.count(' ')
        if space_count > 1:
            raise FormatConnectionError()
        link_array: list[str] = link.split(' ')

        if link_array[0].count('-') != 1:
            raise FormatConnectionError()
        names: list[str] = link_array[0].split('-')

        # I check if the hubs exist
        for name in names:
            if not self.__hubs.get(name):
                raise ConfigError(
                    'You try to make a connection with an unknown hub name.')
        hub: Hub = self.__hubs.get(names[0])

        # The connection can't be specified two times
        if hub.connected_with.get(names[1]):
            raise ConfigError(f'The connection between {names[0]}'
                              f' and {names[1]} is declared twice.')
        cap_link: int = 1
        if len(link_array) == 2:
            if not (link_array[1].startswith('[') and
                    link_array[1].endswith(']')) or\
                    link_array[1].count('=') != 1:
                raise FormatConnectionError()
            try:
                cap_link = int(link_array[1].split('=')[1].strip(']'))
                if cap_link < 1:
                    raise NumberLinksError()
            except ValueError:
                raise NumberLinksError()

        # I store the link in both ways
        hub.connected_with[names[1]] = cap_link
        hub_linked: Hub = self.__hubs.get(names[1])
        hub_linked.connected_with[names[0]] = cap_link

    def add_drones(self) -> None:
        self.list_drones: list[Drone] = []
        for i in range(self.nb_drones):
            self.list_drones.append(Drone(i))
