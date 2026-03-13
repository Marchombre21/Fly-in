# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    field_class.py                                     :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/13 09:35:29 by bfitte            #+#    #+#             #
#    Updated: 2026/03/13 09:35:30 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from pydantic import BaseModel, Field, field_validator
from pydantic_core import PydanticCustomError
from .colors import Colors


class Hub(BaseModel):
    __x: int = Field(ge=0)
    __y: int = Field(ge=0)
    __name: str = Field(pattern=r'[^ -]')
    __zone: str = Field(default='normal')
    __color: str | None = Field(default=None)
    __max_drones: int = Field(default=1, ge=1)
    __role: str
    __connected_with: dict[str, int] = Field(default_factory=dict)

    @field_validator('zone', mode='after')
    @classmethod
    def check_zone(cls, value: str) -> str:
        if value not in ['normal', 'blocked', 'restricted', 'priority']:
            raise PydanticCustomError(
                'field_zone_error',
                'Field zone can be either "normal", "blocked", "restricted" or'
                '"priority".')
        return value

    @field_validator('color', mode='after')
    @classmethod
    def check_color(cls, value: str) -> str:
        if value not in list(Colors):
            raise PydanticCustomError(
                'field_color_error',
                'Unknown color. Check Readme.md to know which colors are'
                ' supported.', {'Unknown color': value}
            )
        return value

    @property
    def name(self):
        return self.__name

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def zone(self):
        return self.__zone

    @property
    def color(self):
        return self.__color

    @property
    def max_drones(self):
        return self.__max_drones

    @property
    def role(self):
        return self.__role

    @property
    def connected_with(self):
        return self.__connected_with
