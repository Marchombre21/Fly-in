# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    hub_class.py                                       :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: bfitte <bfitte@student.42lyon.fr>          +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2026/03/27 16:27:17 by bfitte            #+#    #+#             #
#    Updated: 2026/03/27 16:27:23 by bfitte           ###   ########lyon.fr   #
#                                                                             #
# ****************************************************************************#

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
    ConfigDict
    )
from typing_extensions import Self
from pydantic_core import PydanticCustomError
from arcade import Text


class Hub(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    x: int
    y: int
    name: str = Field(pattern=r"^[^ -]+$")
    zone: str = Field(default="normal")
    color: str | None = Field(default=None)
    max_drones: int = Field(default=1, ge=1)
    role: str
    connected_with: dict[str, int] = Field(default_factory=dict)
    move_cost: int = Field(0)
    weight: int = Field(100000)
    width: int = Field(0)
    height: int = Field(0)
    nb_drones_on: int = Field(default=0)
    text: Text | None = Field(default=None)

    @field_validator("zone", mode="after")
    @classmethod
    def check_zone(cls, value: str) -> str:
        if value not in ["normal", "blocked", "restricted", "priority"]:
            raise PydanticCustomError(
                "field_zone_error",
                'Field zone can be either "normal", "blocked", "restricted" or'
                ' "priority".',
            )
        return value

    @model_validator(mode="after")
    def calculate_move_cost(self) -> Self:
        match self.zone:
            case "normal" | "priority":
                self.move_cost = 1
            case "blocked":
                self.move_cost = 10000
            case "restricted":
                self.move_cost = 2
        return self
