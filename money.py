import conf
import pygame


class Money(pygame.sprite.Sprite):
    
    def __init__(self, pos, dim, coins):
        
        super().__init__()
        pygame.font.init()
        self.pos = pos
        self.dim = dim
        self.rect=pygame.Rect(pos, dim)
        self.colorFons = conf.color_money_fons
        self.font = pygame.font.SysFont("arialblack", int(20*conf.coefLletra))
        self.image = pygame.Surface(dim)
        self.coins=coins

    def update(self):
            
        self.image.fill(self.colorFons)
        stxt = self.font.render('CASH                '    
                  +str(self.coins)+"$", True, (0, 0, 0))
        self.image.blit(stxt, (10, 15))
 

    def build_turret(self, tipus):
        if tipus == "machineGun":
            price = conf.coins_machineGun
        elif tipus == "cannon":
            price = conf.coins_cannon
        elif tipus == "generator":
            price = conf.coins_generator
        elif tipus == "radar":
            price = conf.coins_radar

        self.coins -= price
