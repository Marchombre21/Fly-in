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
from a_star import PathFinder
from errors import ArgError
from parsing import Parser
from pydantic import ValidationError
from pydantic_core import PydanticCustomError
from simulation_engine import SimEngine
from image import View
from dijkstra import Dijkstra
from log_maker import LogMaker


def main() -> None:

    if len(sys.argv) > 1:
        raise ArgError("Too much arguments!")

    path_map: str = input("Which map? : ")

    sim_engine: SimEngine = SimEngine()
    parser: Parser = Parser()
    dijkstra: Dijkstra = Dijkstra()
    parser.parsing(sim_engine, path_map)

    # Adapt coordonates if there are negative values
    sim_engine.check_coordonates()
    sim_engine.add_drones()

    # Add a weight to the hubs
    dijkstra.dijkstra(
        sim_engine.hubs,
        [
            hub.name for hub in sim_engine.hubs.values()
            if hub.role == "end_hub"
        ][0]
    )
    pathfinder: PathFinder = PathFinder(sim_engine.hubs, sim_engine.hashmap)

    # Find the smallest path for each drone
    for drone in sim_engine.list_drones:
        drone.path = pathfinder.a_star_algorithm(drone)

    width: int
    height: int
    width, height = arcade.get_display_size()
    log_maker: LogMaker = LogMaker(sim_engine.list_drones)
    log_maker.make_log()
    view: View = View(int(width * (4 / 5)), int(height * (4 / 5)), "Fly-in")
    view.setup(sim_engine)
    arcade.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
    except ValidationError as e:
        for error in e.errors():
            print(f"{error.get('loc')[0]}: {error.get('input')}\n"
                  f"{error.get('msg')}")
    except PydanticCustomError as e:
        print(e)
