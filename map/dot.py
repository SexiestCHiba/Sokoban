import os
import pygame
import config.constants
import map.moveable
import map.superposeable


class Dot(map.superposeable.Superposeable):
    _character = "."
    path_image = os.path.join(config.constants.BASE_DIR, "images", "dot.png")

    @property
    def character(self):
        if isinstance(self.superposer, map.moveable.Moveable):
            return self.superposer.alternativeCharacter

        return super(Dot, self).character
