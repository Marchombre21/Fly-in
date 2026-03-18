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
from colors import Colors


class Hub(BaseModel):
    x: int
    y: int
    name: str = Field(pattern=r'[^ -]')
    zone: str = Field(default='normal')
    color: str | None = Field(default=None)
    max_drones: int = Field(default=1, ge=1)
    role: str
    connected_with: dict[str, int] = Field(default_factory=dict)

    @field_validator('zone', mode='after')
    @classmethod
    def check_zone(cls, value: str) -> str:
        if value not in ['normal', 'blocked', 'restricted', 'priority']:
            raise PydanticCustomError(
                'field_zone_error',
                'Field zone can be either "normal", "blocked", "restricted" or'
                ' "priority".')
        return value

    @field_validator('color', mode='after')
    @classmethod
    def check_color(cls, value: str) -> str:
        if value not in [color.value for color in list(Colors)]:
            raise PydanticCustomError(
                'field_color_error',
                'Unknown color. Check Readme.md to know which colors are'
                ' supported.', {'Unknown color': value}
            )
        return value
