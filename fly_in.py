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
from .errors import ArgError
from pydantic import ValidationError
from pydantic_core import PydanticCustomError
from .simulation_engine import SimEngine


def main() -> None:

    if len(sys.argv) > 2:
        raise ArgError(
            'Too much arguments! Only one argument is allowed (the path to the'
            'map file).'
        )

    if len(sys.argv) == 2:
        path_map: str = sys.argv[1]
    else:
        path_map = 'map.txt'

    sim_engine: SimEngine = SimEngine()
    

if __name__ == "__main__":
    try:
        main()
    # except Exception as e:
    #     print(e)
    except (PydanticCustomError, ValidationError) as e:
        for error in e.errors():
            print(error)
