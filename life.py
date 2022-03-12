import conf
import pygame


class Life(pygame.sprite.Sprite):
    def __init__(self, pos, dim, health):
        super().__init__()
        pygame.font.init()
        self.pos = pos
        self.dim = dim
        self.percent = 100
        self.total=health
        self.health=health
        self.rect=pygame.Rect(pos, dim)
        self.colorVida = conf.color_vida
        self.colorFons = conf.color_vida_fons
        self.font = pygame.font.SysFont("arialblack", int(20*conf.coefLletra))
        self.image = pygame.Surface(dim)
        self.flick = False
        self.wait = False

    def update(self):
        if self.flick:
            self.colorVida = (180, 50, 50)
            self.flick= False
            self.wait = True
            
        self.image.fill(self.colorFons)
        recVida = pygame.Rect((0,0),
                (self.dim[0]*self.percent//100, self.dim[1]))
        self.image.fill(self.colorVida, recVida)
        stxt = self.font.render('HEALTH           ('
                  +str(self.health)+"/"+str(self.total)+")", True, (0, 0, 0))
        self.image.blit(stxt, (10, 15))

        if self.wait:
            self.colorVida = conf.color_vida
            self.wait = False       

    def dealDamage(self, damage):
        self.health -= damage
        self.percent = int(round((self.health/self.total)*100))
        self.flick = True

