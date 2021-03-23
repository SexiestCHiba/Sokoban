import map.moveable
import os
import config.constants
import pygame


class Box(map.moveable.Moveable):
    _character = "$"
    _alternativeCharacter = "*"
    path_image = os.path.join(config.constants.BASE_DIR, "images", "box.png")
    path_imageAlternative = os.path.join(config.constants.BASE_DIR, "images", "dark_box.png")

    def __init__(self, x, y, image, image_alternative=None):
        super(Box, self).__init__(x, y, image, image_alternative)
