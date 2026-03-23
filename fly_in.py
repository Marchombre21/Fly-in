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
from a_star import a_star_algorithm
from errors import ArgError
from parsing import parsing
from pydantic import ValidationError
from pydantic_core import PydanticCustomError
from simulation_engine import SimEngine
from image import View
from dijkstra import dijkstra


def main() -> None:

    if len(sys.argv) > 1:
        raise ArgError("Too much arguments!")

    path_map: str = input("Which map? : ")
    accept_negative: str = input("\nAccept negative coordinates? (y/n) : ")
    accept_negative = True if accept_negative == "y" else False

    sim_engine: SimEngine = SimEngine(accept_negative)
    parsing(sim_engine, path_map)
    sim_engine.check_coordonates()
    sim_engine.add_drones()
    dijkstra(
        sim_engine.hubs,
        [hub.name for hub in sim_engine.hubs.values() if hub.role == "end_hub"][0],
    )
    for drone in sim_engine.list_drones:
        drone.path = a_star_algorithm(sim_engine)
        # print(drone.path)
        width: int
        height: int
        width, height = arcade.get_display_size()
    view: View = View(width / 2, height / 2, "Fly-in")
    view.setup(sim_engine)
    arcade.run()
    # print([hub.weight for hub in sim_engine.hubs.values()])


if __name__ == "__main__":
    # try:
        main()
    # except Exception as e:
    #     print(e)
    # except (PydanticCustomError, ValidationError) as e:
    #     for error in e.errors():
    #         print(
    #             f"{error.get('loc')[0]}: {error.get('input')}\n" f"{error.get('msg')}"
    #         )
