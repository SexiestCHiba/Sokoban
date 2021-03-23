import os

import config.constants
import map.entity


class Wall(map.entity.Entity):
    _character = "#"
    path_image = os.path.join(config.constants.BASE_DIR, "images", "wall.png")

    def __init__(self, x, y, image, image_alternative=None):
        super(Wall, self).__init__(x, y, image, image_alternative)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
