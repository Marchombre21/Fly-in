# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    image.py                                           :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/17 08:50:46 by bfitte            #+#    #+#             #
#    Updated: 2026/03/17 08:50:47 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

import arcade
from colors import get_color
from errors import ConfigError
from arcade.types import Color
from arcade.texture import Texture
from arcade import Sprite, SpriteList, color
from arcade.shape_list import ShapeElementList, create_rectangle_filled
from simulation_engine import SimEngine


class View(arcade.Window):

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.background_color: Color = color.BLACK
        self.drones_texture: Texture = arcade.load_texture(
            ":resources:images/space_shooter/playerShip1_green.png")
        self.path_east_west_texture: Texture = arcade.load_texture(
            ":resources:images/topdown_tanks/tileGrass_roadEast.png")
        self.path_north_south_texture: Texture = arcade.load_texture(
            ":resources:images/topdown_tanks/tileGrass_roadNorth.png")
        self.drones_list: SpriteList = SpriteList()
        self.paths_list: SpriteList = SpriteList()
        self.hubs_list: ShapeElementList = ShapeElementList()
        self.offset_x: int = 5
        self.offset_y: int = 5
        self.hub_width: int = 0
        self.hub_height: int = 0
        self.scaling: float = 0

    def init_drones(self, sim: SimEngine):

        cell_height: float = self.hub_height / sim.nb_drones

        # To have the scale value I use the formula: scale = target size /
        # original size.
        self.scaling: float = (cell_height * 0.8) / self.drones_texture.width

        for n in range(sim.nb_drones):
            sprite: Sprite = Sprite(self.drones_texture,
                                    scale=self.scaling,
                                    angle=90)
            sprite.center_x = self.hub_width / 2
            sprite.center_y = (cell_height / 2) + (n * cell_height)
            self.drones_list.append(sprite)

    def init_hubs(self, sim: SimEngine):

        nb_col = max([hub.x for hub in sim.hubs]) + 1
        nb_raw = max([hub.y for hub in sim.hubs]) + 1
        self.hub_width = self.width / nb_col
        self.hub_height = self.height / nb_raw
        for n in range(len(sim.hubs)):
            color_name: Color = color.BLACK if not sim.hubs[
                n].color else get_color(sim.hubs[n].color)
            x: int = self.hub_width / 2 + (sim.hubs[n].x * self.hub_width)
            y: int = self.hub_height / 2 + (sim.hubs[n].y * self.hub_height)
            hub_rect = create_rectangle_filled(x, y,
                                               self.hub_width - self.offset_x,
                                               self.hub_height - self.offset_y,
                                               color_name)
            self.hubs_list.append(hub_rect)

    def init_paths(self, sim: SimEngine):
        already_linked: list[str] = []
        for hub in sim.hubs:
            for key in hub.connected_with.keys():
                if hub.name + key not in already_linked:
                    x: int
                    y: int
                    x, y = [(linked_hub.x, linked_hub.y)
                            for linked_hub in sim.hubs
                            if linked_hub.name == key][0]
                    if (hub.x < x or hub.x > x) and hub.y == y:
                        texture: Texture = self.path_east_west_texture
                        multiplier: int = hub.x + 1 if hub.x < x else hub.x
                        center_x: float = self.hub_width * multiplier + (
                            self.offset_x / 2)

                        center_y: float = self.hub_height / 2 + (
                            hub.y * self.hub_height)
                    elif (hub.y < y or hub.y > y) and hub.x == x:
                        texture = self.path_north_south_texture
                        multiplier = hub.y + 1 if hub.y < y else hub.y
                        center_x = self.hub_width / 2 + (hub.x *
                                                         self.hub_width)
                        center_y = self.hub_height * multiplier + (
                            self.offset_y / 2)
                    else:
                        raise ConfigError(
                            f'Impossible connection.{hub.name} + {key}')
                    sprite: Sprite = Sprite(texture, self.scaling, center_x,
                                            center_y)
                    self.paths_list.append(sprite)
                    already_linked.append(key + hub.name)

    def setup(self, sim: SimEngine):
        self.init_hubs(sim)
        self.init_drones(sim)
        # self.init_paths(sim)

    def on_draw(self):
        self.clear()
        self.hubs_list.draw()
        self.drones_list.draw()
        # self.paths_list.draw()

    def on_key_press(self, key):
        """Called whenever a key is pressed. """

        if key == arcade.key.ESCAPE:
            self.close()
