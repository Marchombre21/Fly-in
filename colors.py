# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    colors.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/13 10:41:58 by bfitte            #+#    #+#             #
#    Updated: 2026/03/13 10:49:37 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from enum import Enum
from arcade import color
from arcade.types import Color


class Colors(Enum):
    RED = 'red'
    BLUE = 'blue'
    GREEN = 'green'
    MAROON = 'maroon'
    ORANGE = 'orange'
    SALMON = 'salmon'
    YELLOW = 'yellow'
    INDIGO = 'indigo'
    PURPLE = 'purple'
    MAGENTA = 'magenta'
    VIOLET = 'violet'
    BROWN = 'brown'
    BEIGE = 'beige'
    GRAY = 'gray'
    SILVER = 'silver'
    BLACK = 'black'
    WHITE = 'white'
    IVORY = 'ivory'
    CYAN = 'cyan'
    GOLD = 'gold'
    CRIMSON = 'crimson'
    DARKRED = 'darkred'
    RAINBOW = 'rainbow'


def get_color(color_name: str) -> Color:
    new_color: str = color_name.strip().upper().replace('dark', 'dark_')
    return getattr(color, new_color, color.DARK_BLUE)
