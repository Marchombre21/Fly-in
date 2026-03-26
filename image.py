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
import time
import math
from arcade import (
    draw_circle_filled,
    draw_circle_outline,
    Text,
    Sprite,
    SpriteList,
    color,
)
from colors import get_color
from arcade.types import Color
from arcade.texture import Texture
from arcade.shape_list import (
    create_line,
    Shape,
    ShapeElementList,
    create_ellipse_filled,
    create_ellipse_outline,
)
from simulation_engine import SimEngine
from hub_class import Hub
from drone import Drone
from pyglet.graphics import Batch


class View(arcade.Window):

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        # self.set_update_rate(0.2)
        self.background_color: Color = color.BLACK
        self.background: Texture = arcade.load_texture(
            ":resources:images/backgrounds/stars.png"
        )
        self.drones_texture_mh: Texture = arcade.load_texture(
            "my_face/mi_content-removebg-preview.png"
        )
        self.drones_texture_h: Texture = arcade.load_texture(
            "my_face/content-removebg-preview.png"
        )
        self.drones_texture_nh: Texture = arcade.load_texture(
            "my_face/pas_content-removebg-preview.png"
        )
        # self.path_texture: Texture = arcade.load_texture(
        #     ":resources:images/topdown_tanks/tileGrass_roadEast.png")
        self.drones_list_sprite: SpriteList = SpriteList()
        self.paths_list: list[Shape] = []
        self.path_points: dict[str, list[tuple[float, float]]] = {}
        self.offset_x: int = 5
        self.offset_y: int = 5
        self.turn: int = 0
        self.drones_list: list[Drone]
        self.dict_hubs: dict[str, Hub]
        self.hashmap: dict[tuple[str, int], list[Drone]]
        self.pause: bool = True
        self.batch: Batch = Batch()
        self.hubs_shapes: ShapeElementList = ShapeElementList()

    def init_drones(self, sim: SimEngine):

        start_hub: Hub = [hub for hub in sim.hubs.values() if hub.role == "start_hub"][
            0
        ]
        # cell_height: float = start_hub.height / sim.nb_drones

        # To have the scale value I use the formula: scale = target size /
        # original size.
        scaling: float = (start_hub.width * 0.8) / self.drones_texture_nh.width
        for i in range(sim.nb_drones):
            sprite: Sprite = Sprite(self.drones_texture_nh, scale=scaling)
            # sprite.center_x = (start_hub.x *
            #                    start_hub.width) + start_hub.width / 4
            # sprite.center_y = (start_hub.y * start_hub.height) + (
            # cell_height / 2) + (i * cell_height)
            sprite.center_x = (start_hub.x + 0.5) * start_hub.width
            sprite.center_y = (start_hub.y + 0.5) * start_hub.height
            self.drones_list_sprite.append(sprite)
            sim.list_drones[i].sprite = sprite
            sim.list_drones[i].text = Text(
                "",
                float(sprite.center_x),
                float(sprite.center_y),
                batch=self.batch,
            )

    def init_hubs(self, hub_dict: dict[str, Hub]):

        nb_col = max([hub.x for hub in hub_dict.values()]) + 1
        nb_raw = max([hub.y for hub in hub_dict.values()]) + 1
        hub_width: int = self.width / nb_col
        hub_height: int = self.height / nb_raw
        diameter: float = float(hub_width - self.offset_x)
        for hub in hub_dict.values():
            if hub.role == "start_hub":
                hub.nb_drones_on = len(self.drones_list)
                text_hub: str = "x" + str(len(self.drones_list))
            else:
                text_hub = ""
            hub.width = hub_width
            hub.height = hub_height
            color_name: Color = color.BLACK if not hub.color else get_color(hub.color)
            x: int = hub_width / 2 + (hub.x * hub_width)
            y: int = hub_height / 2 + (hub.y * hub_height)
            hub.text = Text(
                text_hub,
                float(x + (hub.width / 3)),
                float(y + (hub.width / 3)),
                batch=self.batch,
            )
            hub_shape: Shape = create_ellipse_filled(
                x, y, diameter, diameter, color_name
            )
            self.hubs_shapes.append(hub_shape)
            if color_name == color.BLACK:
                hub_border: Shape = create_ellipse_outline(
                    x, y, diameter + 1, diameter + 1, color.WHITE
                )
                self.hubs_shapes.append(hub_border)

    @staticmethod
    def make_path_points(
        start_x: float, start_y: float, end_x: float, end_y: float, hub_width: float
    ) -> list[tuple[float, float]]:
        distance: float = arcade.math.get_distance(start_x, start_y, end_x, end_y)
        step_size: float = 5
        if distance > hub_width:
            step_size = step_size * (distance / hub_width)
        if distance == 0:
            return [(start_x, start_y)]
        num_steps: int = int(distance / step_size)
        points: list[tuple[float, float]] = []

        for i in range(num_steps + 1):
            progress: float = i / num_steps
            curr_x: float = start_x + progress * (end_x - start_x)
            curr_y: float = start_y + progress * (end_y - start_y)
            points.append((curr_x, curr_y))

        if points[-1] != (end_x, end_y):
            points.append((end_x, end_y))

        return points

    def init_paths(self, hubs_dict: dict[str, Hub]):
        already_linked: list[str] = []
        for hub in hubs_dict.values():
            for key in hub.connected_with.keys():

                # I check if the connection has already been established.
                if hub.name + key not in already_linked:

                    # text_width: int = self.path_texture.width

                    x: int
                    y: int
                    x, y = (hubs_dict.get(key).x, hubs_dict.get(key).y)

                    # I define the starting points and ending points of the
                    # path
                    start_x: float = (hub.x + 0.5) * hub.width + (self.offset_x / 2)
                    start_y: float = (hub.y + 0.5) * hub.height + (self.offset_y / 2)
                    end_x: float = (x + 0.5) * hub.width + (self.offset_x / 2)
                    end_y: float = (y + 0.5) * hub.height + (self.offset_y / 2)
                    dx: float = end_x - start_x
                    dy: float = end_y - start_y
                    distance: float = math.hypot(dx, dy)

                    if distance > 0:
                        dir_x: float = dx / distance
                        dir_y: float = dy / distance

                        recul: float = 15.0
                        end_x -= dir_x * recul
                        end_y -= dir_y * recul

                    distance: float = arcade.math.get_distance(
                        start_x, start_y, end_x, end_y
                    )

                    angle_deg: float = arcade.math.get_angle_degrees(
                        start_x, start_y, end_x, end_y
                    )

                    # I convert into radians because the processors and
                    # libraries use them instead of degrees
                    angle_rad: float = math.radians(angle_deg)

                    # If one path must cross over another path I add an offset
                    path_offset: float = 0.0
                    if (int(distance) > int(hub.width) and angle_deg == 0) or (
                        int(distance) > int(hub.height) and angle_deg == 90
                    ):
                        path_offset = 30.0 * 1.5

                    # The offset is calculated by multiplying the size of a
                    # sprite by the new angle to which I added 90 degrees using
                    # the formula π/2
                    new_offset_x: float = path_offset * (
                        math.cos(angle_rad + (math.pi / 2))
                    )
                    new_offset_y: float = path_offset * (
                        math.sin(angle_rad + (math.pi / 2))
                    )

                    start_x += new_offset_x
                    start_y += new_offset_y
                    end_x += new_offset_x
                    end_y += new_offset_y

                    self.paths_list.append(
                        create_line(
                            start_x, start_y, end_x, end_y, color.WHITE_SMOKE, 3
                        )
                    )

                    self.path_points[hub.name + '-' + key] = self.make_path_points(
                        start_x, start_y, end_x, end_y, float(hub.width)
                    )
                    self.path_points[key + '-' + hub.name] = self.make_path_points(
                        end_x, end_y, start_x, start_y, float(hub.width)
                    )
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
        hub.nb_drones_on += 1
        drone.on_connection = None
        drone.actual_location = drone.path[self.turn + 1]
        self.check_quantity(hub, drone)

    def on_the_road(self, drone: Drone):
        if drone.two_turns and drone.len_connection / 2 >= len(drone.on_connection):
            drone.actual_location = drone.path[self.turn + 1]
            drone.two_turns = False
        else:
            drone.sprite.center_x, drone.sprite.center_y = drone.on_connection.pop(0)
            drone.text.x = drone.sprite.center_x + (
                drone.sprite.width * drone.sprite.scale_x
            )
            drone.text.y = drone.sprite.center_y + (
                drone.sprite.height * drone.sprite.scale_y
            )
            if len(drone.on_connection) == 0:
                self.landing(drone)
                if self.dict_hubs[drone.path[self.turn + 1]].role == "end_hub":
                    drone.finish = True

    def takeoff(self, drone: Drone):

        dest: str = drone.path[self.turn + 1]
        conn_key: str
        if '-' in dest:
            conn_key = dest
            drone.two_turns = True
        else:
            conn_key = drone.actual_location + '-' + dest
        path: list[tuple[float, float]] = self.path_points[conn_key]
        # mc: int = self.dict_hubs[drone.path[self.turn + 1]].move_cost
        # if not path:
        #     drone.two_turns = True
        #     path = self.path_points.get(drone.path[self.turn + 1])
        # if not path:
        #     drone.two_turns = False
        #     path = self.path_points.get(drone.path[self.turn - 1])
        # if mc == 2:
        #     drone.two_turns = True
        self.dict_hubs[drone.actual_location].nb_drones_on -= 1
        drone.on_connection = path.copy()
        self.check_quantity(self.dict_hubs[drone.actual_location], drone)
        drone.sprite.center_x, drone.sprite.center_y = drone.on_connection.pop(0)
        drone.text.x = drone.sprite.center_x + (
            drone.sprite.width * drone.sprite.scale_x
        )
        drone.text.y = drone.sprite.center_y + (
            drone.sprite.height * drone.sprite.scale_y
        )

    def adjust_scale(self, drone: Drone):
        if drone.on_connection:
            drone.sprite.scale = self.height * 0.1 / drone.sprite.texture.height
        else:
            drone.sprite.scale = (
                self.dict_hubs[drone.actual_location].width
                * 0.8
                / drone.sprite.texture.width
            )

    def adjust_texture(self, drone: Drone):
        if drone.sprite.center_x <= self.width * (1 / 3):
            drone.sprite.texture = self.drones_texture_nh
        elif self.width * (1 / 3) < drone.sprite.center_x <= self.width * (2 / 3):
            drone.sprite.texture = self.drones_texture_mh
        else:
            drone.sprite.texture = self.drones_texture_h

    def check_quantity(self, hub: Hub, drone: Drone):
        dest: str = drone.path[self.turn + 1]

        if drone.on_connection:
            if '-' in drone.actual_location:
                conn_key = drone.actual_location
            elif '-' in dest:
                conn_key = dest
            else:
                conn_key = drone.actual_location + '-' + dest

            if (conn_key, self.turn + 1) in self.hashmap:
                drone.text.text = "x" + str(len(self.hashmap[(conn_key, self.turn + 1)]))
        else:
            drone.text.text = ""

        if hub.nb_drones_on > 0:
            self.dict_hubs[hub.name].text.text = f"x{hub.nb_drones_on}"
        else:
            self.dict_hubs[hub.name].text.text = ""

    def on_update(self, delta_time):
        if not self.pause:
            all_hubs_reached: bool = True
            for drone in self.drones_list:
                if not drone.finish:
                    if drone.actual_location != drone.path[self.turn + 1]:
                        all_hubs_reached = False
                        if drone.on_connection:
                            self.on_the_road(drone)
                        else:
                            self.takeoff(drone)
                    self.adjust_scale(drone)
                self.adjust_texture(drone)
            if all_hubs_reached:
                time.sleep(1)
                self.turn += 1

        return super().on_update(delta_time)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.background, arcade.LBWH(0, 0, self.width, self.height)
        )
        self.hubs_shapes.draw()
        for path in self.paths_list:
            path.draw()
        self.drones_list_sprite.draw()
        self.batch.draw()

    def on_key_press(self, key: int, modifier: int):
        """Called whenever a key is pressed."""

        if key == arcade.key.ESCAPE:
            self.close()

        if key == arcade.key.SPACE:
            self.pause = not self.pause
