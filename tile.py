import pygame

class Tile(pygame.sprite.Sprite):

    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        
