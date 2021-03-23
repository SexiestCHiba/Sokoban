import os
import config.constants
import map.moveable


class Player(map.moveable.Moveable):
    """The definition of the Player class"""
    _character = "@"
    _alternativeCharacter = "+"  # used when it is superposed to an dot
    path_image = os.path.join(config.constants.BASE_DIR, "images", "player.png")
