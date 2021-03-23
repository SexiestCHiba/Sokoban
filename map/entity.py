import pygame


class Entity(pygame.sprite.Sprite):
    _character: str = ""
    _alternativeCharacter: str = ""
    
    path_image: str = ""
    path_imageAlternative: str = ""

    _image: str = ""
    _imageAlternative: str = ""

    def __init__(self, x, y, image, image_alternative=""):
        super(Entity, self).__init__()
        self.dx = 0
        self.dy = 0
        self.image = image
        self._imageAlternative = image_alternative
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def update(self):
        self.rect = self.rect.move(self.dx, self.dy)

    @property
    def imageAlternative(self) -> str:
        return self._imageAlternative

    @property
    def alternativeCharacter(self) -> str:
        return self._alternativeCharacter

    @property
    def character(self) -> str:
        return self._character
