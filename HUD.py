import conf
import pygame
import functions as fn

class Menu(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos


        
class SimpleButton(pygame.sprite.Sprite):           #Botó senzill amb una imatge i el mètode "pressed" per a saber si s'ha clicat.
    def __init__(self, image, pos, tipus=None):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.tipus = tipus

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

class Button(pygame.sprite.Sprite):                 #Botó de torretes.
    def __init__(self, image, pos, cash, tipus=None):
        super().__init__()
        self.cash = cash
        self.image = image

        self.rect = self.image.get_rect()

        self.rect.topleft = pos
        self.tipus = tipus
        self.font = pygame.font.SysFont("arialblack", int(20*conf.coefLletra))
        self.price = conf.prices[self.tipus]
        stext=self.font.render(str(self.price)+"$", True, (0,0,0))
        self.image.blit(stext, (12, 60))

        dark = pygame.Surface((image.get_width(), image.get_height()), flags=pygame.SRCALPHA)
        dark.fill((90, 90, 90, 0))

        self.imageLight =image.copy()
        self.imageDark = image.copy()
        self.imageDark.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    def update(self):
        if self.cash.coins >= self.price:
            self.image=self.imageLight
        else:
            self.image=self.imageDark
    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False

        
#    def tipus(self):
#        return self.tipus



class Icon(pygame.sprite.Sprite):
    def __init__(self, image, radius):
        super().__init__()
        self.image = pygame.Surface((2*radius,2*radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        self.radius=radius
        self.color=conf.color_reach
        torreta = image
        
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.image.blit(torreta, (radius-25, radius-25))                
    def update(self):

        pos = pygame.mouse.get_pos()
        cas = pos[0]//50*50+25, pos[1]//50*50+25
        self.rect.center = cas      

class Reach(pygame.sprite.Sprite):
    def __init__(self, pos,radius):
        super().__init__()
        self.radius=radius
        self.pos=pos
        self.image = pygame.Surface((2*radius,2*radius), pygame.SRCALPHA)
        self.rect=pygame.Rect(pos, (2*radius,2*radius))
        self.rect.center=pos

        self.color=conf.color_reach
        self.color_transparent=(0,0,0,0)
        self.image.fill(self.color_transparent)
        
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)

class NextRound(pygame.sprite.Sprite):
    
    def __init__(self, pos, dim):
        
        super().__init__()
        pygame.font.init()
        self.n_ronda=0
        self.n_rondes_totals=0
        self.pos = pos
        self.dim = dim
        self.activated = False
        self.rect=pygame.Rect(pos, dim)
        self.colorFons = conf.color_next_round
        self.image = pygame.Surface(dim)          
        self.font = pygame.font.SysFont("arialblack", int(20*conf.coefLletra))

    def update(self):
        self.image.fill(self.colorFons)
        stxt = self.font.render('NEXT ROUND round '+str(self.n_ronda)+' out of '+str(self.n_rondes_totals),True,(0, 0, 0))
        self.image.blit(stxt, (10, 15))
        

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False





class TurretInfo(pygame.sprite.Sprite):
    def __init__(self, dim, topleft, turret):
        super().__init__()
        self.image = pygame.Surface(dim, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft=topleft
        self.image.fill(conf.color_menuGrey)
        
        NAME=turret.tipus.upper()


            
        if hasattr(turret, 'DMGboost'):
            DMGs="Damage Boost"
            dmg=str(turret.DMGboost)
            MAXDMG = False
            firerate="0"
        elif hasattr(turret, 'REACHboost'):
            DMGs="Reach Boost"
            dmg=str(turret.REACHboost)
            MAXDMG = False
            firerate="0"
        else:
            DMGs="Damage"
            dmg=str(round(turret.currentDamage, 1))
            MAXDMG=conf.DMGMultLimits[turret.tipus]<turret.DMGmult
            firerate=str(round(1/turret.firerate*conf.fps*60, 2))
            
        #VALOR = ("VALOR = ", valor, isMaxed?)
        REACH=("Reach",   str(round(turret.currentReach, 1)),  conf.REACHMultLimits[turret.tipus]<turret.REACHmult)
        DMG=(DMGs,             dmg,                  conf.DMGMultLimits[turret.tipus]<turret.DMGmult)
        FIRERATE=("Firerate", firerate,              False)

        self.font = pygame.font.SysFont("arial", int(11))#(2.2*conf.coefLletra-1.2)))
                
      
        margeX = 10
        margeY = 10
        sep = 18
        margeBlanc = 75
        attrLis=[NAME, DMG, REACH, FIRERATE]
        for i in [0,1,2,3]:
            if i==0:
                row = self.font.render(NAME,True,(0, 0, 0))
                self.image.blit(row, (dim[0]/2-55, margeY))
            else:
                row = self.font.render(attrLis[i][0], True, (0,0,0))
                self.image.blit(row, (margeX, margeY+(1+i)*sep))
                
                valor = attrLis[i][1]
                maxed = attrLis[i][2]
                row = self.font.render(valor+maxed*" MAX", True, (0+200*maxed,0,0))
                self.image.blit(row, (margeX+margeBlanc, margeY+(1+i)*sep))


        startingY=margeY+5*sep
        text='"'+conf.descripcio[turret.tipus]+'"'
        maxX=self.rect.width
        fn.renderLongText(self.font, self.image, text, 13, maxX, margeX, startingY)

