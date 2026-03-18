# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    fly_in.py                                          :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/13 09:20:45 by bfitte            #+#    #+#             #
#    Updated: 2026/03/13 09:20:46 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

import sys
import arcade
from errors import ArgError
from parsing import parsing
from pydantic import ValidationError
from pydantic_core import PydanticCustomError
from simulation_engine import SimEngine
from image import View


def main() -> None:

    path_map: str = input('Which map? : ')
    accept_negative: str | bool = input(
        'Accept negative coordonates? (y/n) : ')
    accept_negative = True if accept_negative == 'y' else False
    # if len(sys.argv) > 2:
    #     raise ArgError(
    #         'Too much arguments! Only one argument is allowed (the path to the'
    #         'map file).')

    # if len(sys.argv) == 2:
    #     path_map: str = sys.argv[1]
    # else:
    #     path_map = 'map.txt'

    sim_engine: SimEngine = SimEngine(accept_negative)
    parsing(sim_engine, path_map)
    view: View = View(2000, 1300, 'Fly-in')
    view.setup(sim_engine)
    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    except (PydanticCustomError, ValidationError) as e:
        for error in e.errors():
            print(f"{error.get('loc')[0]}: {error.get('input')}\n"
                  f"{error.get('msg')}")
