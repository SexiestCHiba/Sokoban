import os
import typing

import config.constants
import map.dot
import map.moveable
import map.superposeable


class Air(map.superposeable.Superposeable):
    _character = " "
    path_image = os.path.join(config.constants.BASE_DIR, "images", "floor.png")

    def draw(self, surface):
        for image in self.images:
            surface.blit(image, self.rect)

    @property
    def images(self) -> typing.List[str]:
        images = [self.image]

        superposers = self.get_superposers()

        i = 0
        while i < len(superposers):
            use_default_image = True
            if i == len(superposers) - 1 and issubclass(superposers[i].__class__, map.moveable.Moveable):
                try:
                    if isinstance(superposers[i - 1], map.dot.Dot) and superposers[i].imageAlternative:
                        use_default_image = False
                except IndexError:
                    pass

            if use_default_image:
                images.append(superposers[i].image)
            else:
                images.append(superposers[i].imageAlternative)

            i += 1

        return images

    @property
    def character(self) -> str:
        if self.superposer is not None:
            return self.superposer.character

        return super(Air, self).character
