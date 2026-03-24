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
from hub_class import Hub
from drone import Drone
from pyglet.graphics import Batch


class View(arcade.Window):

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.set_update_rate(0.2)
        self.background_color: Color = color.BLACK
        self.drones_texture_mh: Texture = arcade.load_texture(
            "my_face/mi_content-removebg-preview.png")
        self.drones_texture_h: Texture = arcade.load_texture(
            "my_face/content-removebg-preview.png")
        self.drones_texture_nh: Texture = arcade.load_texture(
            "my_face/pas_content-removebg-preview.png")
        self.path_texture: Texture = arcade.load_texture(
            ":resources:images/topdown_tanks/tileGrass_roadEast.png")
        self.drones_list_sprite: SpriteList = SpriteList()
        self.paths_list: dict[str, SpriteList] = {}
        self.hubs_list: ShapeElementList = ShapeElementList()
        self.offset_x: int = 5
        self.offset_y: int = 5
        self.turn: int = 0
        self.drones_list: list[Drone]
        self.dict_hubs: dict[str, Hub]
        self.hashmap: dict[tuple[str, int], list[Drone]]
        self.pause: bool = True
        self.batch: Batch = Batch()

    def init_drones(self, sim: SimEngine):

        start_hub: Hub = [
            hub for hub in sim.hubs.values() if hub.role == 'start_hub'
        ][0]
        cell_height: float = start_hub.height / sim.nb_drones

        # To have the scale value I use the formula: scale = target size /
        # original size.
        scaling: float = (cell_height * 0.8) / self.drones_texture_mh.height
        for i in range(sim.nb_drones):
            sprite: Sprite = Sprite(self.drones_texture_mh, scale=scaling)
            sprite.center_x = (start_hub.x *
                               start_hub.width) + start_hub.width / 4
            sprite.center_y = (start_hub.y * start_hub.height) + (
                cell_height / 2) + (i * cell_height)
            # for n in range(sim.nb_drones):
            #     sprite: Sprite = Sprite(self.drones_texture_mh,
            #                             scale=scaling,
            #                             angle=270)
            #     sprite.center_x = self.hub_width / 4
            #     sprite.center_y = (cell_height / 2) + (n * cell_height)
            self.drones_list_sprite.append(sprite)
            sim.list_drones[i].sprite = sprite

    def init_hubs(self, hub_dict: dict[str, Hub]):

        nb_col = max([hub.x for hub in hub_dict.values()]) + 1
        nb_raw = max([hub.y for hub in hub_dict.values()]) + 1
        hub_width: int = self.width / nb_col
        hub_height: int = self.height / nb_raw
        for hub in hub_dict.values():
            hub.width = hub_width
            hub.height = hub_height
            color_name: Color = color.BLACK if not hub.color else get_color(
                hub.color)
            x: int = hub_width / 2 + (hub.x * hub_width)
            y: int = hub_height / 2 + (hub.y * hub_height)
            hub_rect = create_rectangle_filled(x, y, hub_width - self.offset_x,
                                               hub_height - self.offset_y,
                                               color_name)
            self.hubs_list.append(hub_rect)

    def init_paths(self, hubs_dict: dict[str, Hub]):
        already_linked: list[str] = []
        for hub in hubs_dict.values():
            for key in hub.connected_with.keys():

                # I check if the connection has already been established.
                if hub.name + key not in already_linked:

                    text_width: int = self.path_texture.width

                    x: int
                    y: int
                    x, y = (hubs_dict.get(key).x, hubs_dict.get(key).y)

                    # I define the starting points and ending points of the
                    # path
                    start_x: float = (hub.x + 0.5) * hub.width + (
                        self.offset_x / 2)
                    start_y: float = (hub.y + 0.5) * hub.height + (
                        self.offset_y / 2)
                    end_x: float = (x + 0.5) * hub.width + (self.offset_x / 2)
                    end_y: float = (y + 0.5) * hub.height + (self.offset_y / 2)

                    distance: float = arcade.math.get_distance(
                        start_x, start_y, end_x, end_y)

                    angle_deg: float = arcade.math.get_angle_degrees(
                        start_x, start_y, end_x, end_y)

                    # I convert into radians because the processors and
                    # libraries use them instead of degrees
                    angle_rad: float = math.radians(angle_deg)

                    # If one path must cross over another path I add an offset
                    path_offset: float = 0.0
                    if (int(distance) > int(hub.width) and angle_deg
                            == 0) or (int(distance) > int(hub.height)
                                      and angle_deg == 90):
                        # print(hub.name, distance, self.hub_width, angle_deg)
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

                    sprite_list: SpriteList = SpriteList()
                    for i in range(num_sprites):
                        current_distance: float = (i * text_width) + (
                            text_width / 2)

                        center_x: float = start_x + (math.cos(angle_rad) *
                                                     current_distance)
                        center_y: float = start_y - (math.sin(angle_rad) *
                                                     current_distance)

                        sprite: Sprite = Sprite(self.path_texture, 1.0,
                                                center_x, center_y, angle_deg)
                        sprite_list.append(sprite)

                    self.paths_list[key + hub.name] = sprite_list
                    reversed_list: SpriteList = SpriteList()
                    reversed_list.extend(reversed(sprite_list))
                    self.paths_list[hub.name + key] = reversed_list
                    already_linked.append(key + hub.name)

    def setup(self, sim: SimEngine):
        self.drones_list = sim.list_drones
        self.hashmap = sim.hashmap
        self.dict_hubs = sim.hubs
        self.init_hubs(sim.hubs)
        self.init_drones(sim)
        self.init_paths(sim.hubs)

    def landing(self, drone: Drone):
        hub: Hub = self.dict_hubs[drone.path[self.turn + 1]]
        drone.sprite.center_x = (hub.x + 0.5) * hub.width
        drone.sprite.center_y = (hub.y + 0.5) * hub.height
        drone.on_connection = None
        drone.actual_location = drone.path[self.turn + 1]

    def on_the_road(self, drone: Drone):
        for i, sprite in enumerate(drone.on_connection):
            if sprite.center_x == drone.sprite.center_x and sprite.center_y ==\
                    drone.sprite.center_y:
                if drone.two_turns and i >= len(drone.on_connection) / 2:
                    drone.actual_location = drone.path[self.turn + 1]
                    drone.two_turns = False
                else:
                    drone.sprite.center_x =\
                        drone.on_connection[i + 1].center_x
                    drone.sprite.center_y =\
                        drone.on_connection[i + 1].center_y
                    if i + 1 == len(drone.on_connection) - 1:
                        # print(drone.actual_location)
                        # print(drone.path[self.turn + 1])
                        self.landing(drone)
                        if self.dict_hubs[drone.path[self.turn +
                                                     1]].role == 'end_hub':
                            drone.finish = True
                break

    def takeoff(self, drone: Drone):
        drone.on_connection = self.paths_list.get(drone.path[self.turn + 1] +
                                                  drone.actual_location)
        if not drone.on_connection:
            # print('+1', drone.sprite.center_x)
            # print(drone.path[self.turn + 1])
            drone.two_turns = True
            drone.on_connection = self.paths_list.get(drone.path[self.turn +
                                                                 1])
        if not drone.on_connection:
            # print('-1', drone.sprite.center_x)
            drone.two_turns = False
            drone.on_connection = self.paths_list.get(drone.path[self.turn -
                                                                 1])

        # print('drone dest', drone.path[self.turn + 1])
        # print('drone depart', drone.actual_location)
        # print(self.paths_list)
        drone.sprite.center_x = drone.on_connection[0].center_x
        drone.sprite.center_y = drone.on_connection[0].center_y

    def adjust_scale(self, drone: Drone):
        if drone.on_connection:
            drone.sprite.scale = drone.on_connection[
                0].texture.height / drone.sprite.texture.height
        else:
            cell_height: float = self.dict_hubs[
                drone.actual_location].height / len(
                    self.hashmap[(drone.actual_location, self.turn + 1)])
            drone.sprite.scale = cell_height * 0.8 /\
                drone.sprite.texture.height

    def adjust_texture(self, drone: Drone):
        if drone.sprite.center_x <= self.width * (1 / 3):
            drone.sprite.texture = self.drones_texture_nh
        elif self.width * (1 / 3) < drone.sprite.center_x <= self.width * (2 /
                                                                           3):
            drone.sprite.texture = self.drones_texture_mh
        else:
            drone.sprite.texture = self.drones_texture_h

    def on_update(self, delta_time):
        if not self.pause:
            all_hubs_reached: bool = True
            for drone in self.drones_list:
                if not drone.finish:
                    # print('actual', drone.actual_location)
                    # print('path', drone.path[self.turn + 1])
                    # print('turn', self.turn)
                    if drone.actual_location != drone.path[self.turn + 1]:
                        all_hubs_reached = False
                        if drone.on_connection:
                            self.on_the_road(drone)
                        else:
                            self.takeoff(drone)
                    self.adjust_scale(drone)
                self.adjust_texture(drone)
            if all_hubs_reached:
                self.turn += 1
        return super().on_update(delta_time)

    def on_draw(self):
        self.clear()
        self.hubs_list.draw()
        for path_sprite in self.paths_list.values():
            path_sprite.draw()
        self.drones_list_sprite.draw()

    def on_key_press(self, key: int, modifier: int):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.close()

        if key == arcade.key.SPACE:
            self.pause = not self.pause
