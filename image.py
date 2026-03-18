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
import math
from colors import get_color
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
            ":resources:images/topdown_tanks/tank_red.png")
        self.path_texture: Texture = arcade.load_texture(
            ":resources:images/topdown_tanks/tileGrass_roadEast.png")
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
                                    angle=270)
            sprite.center_x = self.hub_width / 4
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

                # I check if the connection has already been established.
                if hub.name + key not in already_linked:

                    text_width: int = self.path_texture.width

                    x: int
                    y: int
                    x, y = [(linked_hub.x, linked_hub.y)
                            for linked_hub in sim.hubs
                            if linked_hub.name == key][0]

                    # I define the starting points and ending points of the
                    # path
                    # Je suis en train de réfléchir pour changer le display du path
                    # pour qu'il commence plutôt sur le bord du hub et plus au centre.
                    # Pareil pour l'arrivée
                    start_x: float = (hub.x + 0.5) * self.hub_width + (
                        self.offset_x / 2)
                    start_y: float = (hub.y + 0.5) * self.hub_height + (
                        self.offset_y / 2)
                    end_x: float = (x + 0.5) * self.hub_width + (
                        self.offset_x / 2)
                    end_y: float = (y + 0.5) * self.hub_height + (
                        self.offset_y / 2)

                    distance: float = arcade.math.get_distance(
                        start_x, start_y, end_x, end_y)

                    angle_deg: float = arcade.math.get_angle_degrees(
                        start_x, start_y, end_x, end_y)

                    # I convert into radians because the processors and
                    # libraries use them instead of degrees
                    angle_rad: float = math.radians(angle_deg)

                    # If one path must cross over another path I add an offset
                    path_offset: float = 0.0
                    if (int(distance) > int(self.hub_width) and angle_deg
                            == 0) or (int(distance) > int(self.hub_height)
                                      and angle_deg == 90):
                        print(hub.name, distance, self.hub_width, angle_deg)
                        path_offset = text_width * 1.5

                    # The offset is calculated by multiplying the size of a
                    # sprite by the new angle to which I added 90 degrees using
                    # the formula π/2
                    new_offset_x: float = path_offset * (
                        math.cos(angle_rad + (math.pi / 2)))
                    new_offset_y: float = path_offset * (
                        math.sin(angle_rad + (math.pi / 2)))

                    start_x += new_offset_x
                    start_y += new_offset_y

                    num_sprites: int = int(distance / text_width)

                    for i in range(num_sprites):
                        current_distance: float = (i * text_width) + (
                            text_width / 2)

                        center_x: float = start_x + (math.cos(angle_rad) *
                                                     current_distance)
                        center_y: float = start_y - (math.sin(angle_rad) *
                                                     current_distance)

                        sprite: Sprite = Sprite(self.path_texture, 1.0,
                                                center_x, center_y, angle_deg)
                        self.paths_list.append(sprite)

                    already_linked.append(key + hub.name)

    def setup(self, sim: SimEngine):
        self.init_hubs(sim)
        self.init_drones(sim)
        self.init_paths(sim)

    def on_draw(self):
        self.clear()
        self.hubs_list.draw()
        self.paths_list.draw()
        self.drones_list.draw()

    def on_key_press(self, key):
        """Called whenever a key is pressed. """

        if key == arcade.key.ESCAPE:
            self.close()
