# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    errors.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/13 09:22:14 by bfitte            #+#    #+#             #
#    Updated: 2026/03/13 09:22:15 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#


class ArgError(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class ConfigError(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class FirstLineError(ConfigError):

    def __init__(self):
        message: str = 'The first line of the map file must be in "nb_drones:'\
            ' <nb>" format'
        super().__init__(message)


class KeysError(ConfigError):

    def __init__(self):
        message: str = 'Allowed keys in the map file are "nb_drone",'\
            ' "start_hub", "end_hub", "hub" and "connection".'
        super().__init__(message)


class FormatHubError(ConfigError):

    def __init__(self):
        message: str = 'The hub value must be in <name> <x> <y>'\
            ' <[metadatas](optional)> format.'
        super().__init__(message)


class FormatConnectionError(ConfigError):

    def __init__(self):
        message: str = 'The connection value must be in <name>-<name>'\
            ' [max_link_capacity=<number>(optionnal)] format.'
        super().__init__(message)


class NumberLinksError(ConfigError):

    def __init__(self):
        message: str = 'max_link_capacity should be positive integer.'
        super().__init__(message)


class FormatMetadatasError(ConfigError):

    def __init__(self):
        message: str = 'Metadatas must be in <[zone=<value> color=<value>'\
            ' max_drones=<value>]> format. All are optional and the order'\
            ' doesn\'t matter.'
        super().__init__(message)


class SimError(Exception):

    def __init__(self, message: str):
        super().__init__(message)


class NoPathFound(Exception):

    def __init__(self, message: str):
        super().__init__(message)
