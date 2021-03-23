import pygame


class GoBack(pygame.sprite.Sprite):
    """Create a sprite that will allow the user to get back in the menu"""
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((60, 20))
        pygame.draw.rect(self.image, pygame.Color(255, 255, 255, 255), pygame.Rect(20, 5, 40, 10))
        pygame.draw.polygon(self.image, pygame.Color(255, 255, 255, 255), [(0, 10), (20, 0), (20, 20)])
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
