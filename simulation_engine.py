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

from .field_class import Hub
from .errors import SimError, FormatConnectionError, ConfigError


class SimEngine():

    def __init__(self):
        self.__hubs: list[Hub] = []
        self.__nb_drones: int = 0

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

    def add_hub(self, hub_dict: dict[str, str]) -> None:
        name: str = hub_dict.get('name')
        x: str = hub_dict.get('x')
        y: str = hub_dict.get('y')
        for hub in self.__hubs:
            if hub.name == name:
                raise ConfigError('All hubs must have different names.')
            if str(hub.x) == x and str(hub.y) == y:
                raise ConfigError(
                    'Two hubs can\'t be at the same coordonates.')
        self.__hubs.append(Hub(**hub_dict))

    def create_connection(self, link: str):
        space_count: int = link.count(' ') 
        if space_count > 1:
            raise FormatConnectionError()
        link_array: list[str] = link.split(' ')
        # En train de gérer les connexions. Ici nous sommes sûrs qu'il y a
        # moins de deux espaces donc le split a donné un tableau de 1 ou 2
        # éléments. Il faut repartir sur le block d'après, refaire un split
        # sur un - (après avoir vérifié que la string ne commence pas par []. 
        # Ah non en fait, les names peuvent contenir n'importe quoi en fait.)
        
        if link.count('-') != 1:
            raise FormatConnectionError()
        for hub in self.__hubs:
            # if hub.name == link_array[0]:
            #     if hub.connected_with.get(link_array[1]):
            #         raise ConfigError(
            #             f'The connection between {link_array[0]}'
            #             f' and {link_array[1]} is declared twice.')
            #     else:

