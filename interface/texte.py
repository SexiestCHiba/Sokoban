import pygame


class Texte(pygame.sprite.Sprite):
    
    def __init__(self, font, texte, x, y):
        super(Texte, self).__init__()
        self.texte = texte
        self.font = font
        self.image = self.font.render(texte, True, pygame.color.THECOLORS['white'])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.dx = 0
        self.dy = 0

    def update(self):
        """Update the text"""
        self.rect = self.rect.move(self.dx, self.dy)
