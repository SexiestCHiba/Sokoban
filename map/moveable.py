import enum
import typing

import map.entity

DIRECTION = enum.Enum('direction', 'UP DOWN LEFT RIGHT')


class Moveable(map.entity.Entity):
    directions_dict = {DIRECTION.LEFT: lambda x, y: (x, y - 1),
                       DIRECTION.RIGHT: lambda x, y: (x, y + 1),
                       DIRECTION.UP: lambda x, y: (x - 1, y),
                       DIRECTION.DOWN: lambda x, y: (x + 1, y)}

    def __init__(self, x, y, image, image_alternative=None):
        super(Moveable, self).__init__(x, y, image, image_alternative)

    @classmethod
    def get_new_coords(cls, direction: DIRECTION, coords: typing.Tuple[int, int]) -> typing.Tuple[int, int]:
        """
        Get the new coordinates from a move by a moveable entity.
        this function takes a direction from the ENUM "DIRECTION"
        and the coordinates that you want to change with the chosen direction.

        direction: enum.ENUM DIRECTION
        coords: typing.Tuple(int, int) - line/column

        This function return a typing.Tuple(int, int)
        """
        return cls.directions_dict[direction](coords[0], coords[1])
