# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    parsing.py                                         :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/13 11:18:38 by bfitte            #+#    #+#             #
#    Updated: 2026/03/13 11:18:39 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from .simulation_engine import SimEngine
from .errors import (
    ConfigError,
    FirstLineError,
    KeysError,
    FormatHubError,
    FormatMetadatasError)


def first_line(first: str) -> int:

    first_line_array: list[str] = first.split(':')
    if first_line_array[0] != 'nb_drones':
        raise FirstLineError()
    try:
        return int(first_line_array[1])
    except ValueError:
        raise ConfigError('The nb_drones value should be a positive integer.')


def hub(role: str, line: str) -> dict[str, str]:
    line_array: list[str] = line.split(' ', 3)
    if len(line_array) < 3 or len(line_array) > 4:
        raise FormatHubError()
    for element in line_array[1:3]:
        if element.startswith('[') or '[' in element:
            raise FormatHubError()
    hub_dict: dict[str, str] = {
        'x': line_array[1],
        'y': line_array[2],
        'name': line_array[0],
        'role': role
    }
    if len(line_array) == 4:
        if not (line_array[3].startswith('[') and line_array[3].endswith(']')):
            raise FormatHubError()
        if (line_array[3].count(' ') + 1) != (line_array[3].count('=')):
            # There must be one space less than = in good format.
            raise FormatHubError()
        meta_array: list[str] = line_array[3].strip('[').strip(']').split()
        for element in meta_array:
            if element.count('=') == 1:
                element_array: list[str] = element.split('=')
                if element_array[0] in ['zone', 'color', 'max_drones']:
                    if hub_dict.get(element_array[0]) is None:
                        hub_dict.update({element_array[0]: element_array[1]})
                    else:
                        raise FormatMetadatasError()
                else:
                    raise FormatMetadatasError()
            else:
                raise FormatMetadatasError()
    return hub_dict


def parsing(sim: SimEngine, path: str):

    with open(path, 'r') as f:
        line: str = f.readline()
        first_line: bool = True
        while line:
            if line.count(':') != 1:
                raise ConfigError('Each line (except commentaries) should have'
                                  ' "<key>:<value>" format')
            if not line.startswith('#'):
                if first_line:
                    first_line = False
                    sim.nb_drones = first_line(line)
                else:
                    line_array: list[str] = line.split(':')
                    if line_array[0] == 'connection':
                        sim.create_connection(line_array[1])
                    elif line_array[0] in ['start_hub', 'end_hub', 'hub']:
                        sim.add_hub(hub(line_array[0], line_array[1]))
                    else:
                        raise KeysError()
