import conf
import functions as fn
import pygame
import robot
import random as r

class Turret(pygame.sprite.Sprite):
    def __init__(self, tipus, matImages, pos, damage, firerate, grupRobots, reach):
        super().__init__()
        self.tipus = tipus
        self.matImages = matImages
        self.angle = 0.0
        if type(matImages)==list:
            self.image = matImages[0][0]
        else:
            self.image=matImages
            
        self.grupRobots = grupRobots
        
        self.damage = damage
        self.currentDamage = damage         #El que s'usa per a fer mal
        self.firerate = firerate
        self.reach = reach
        self.currentReach = reach           #El que s'usa per a fer reach
        
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.t1=pygame.time.get_ticks()-firerate
        self.robotFixat = None
        self.fireState = 5
        self.DMGmult=1
        self.REACHmult=1
        if tipus in conf.dicShots:
            self.shot = pygame.mixer.Sound(conf.dicShots[tipus])
            self.shot.set_volume(0.37)
        
    def update(self):        
        
        t2=pygame.time.get_ticks()
        
        if self.robotFixat == None:
            pass
        else:
            angle=fn.angle(self.rect.center, self.robotFixat.rect.center)
            quadrant=fn.quadrant(angle, 16)
            self.image = self.matImages[int(self.fireState)][(quadrant+8)%16]


        
        if t2-self.t1 > self.firerate:
            self.t1=t2          

            for Robot in self.grupRobots:
                
                if fn.reach(self.rect.center, Robot.rect.center, self.currentReach):
                    self.robotFixat = Robot

                    Robot.dealDamage(self.currentDamage)
                    self.fireState = 2
                    self.shot.play()
                    break
                
        if self.fireState <5:
            self.fireState += 0.4
    
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


    def refresh(self):
        self.currentDamage = self.damage*min(self.DMGmult, conf.DMGMultLimits[self.tipus])
        self.currentReach = self.reach*min(self.REACHmult, conf.REACHMultLimits[self.tipus])
                                                
                                                
    def remove(self):
        self.kill()

class Generator(Turret):
    def __init__(self, tipus, matImages, pos, damage, firerate, grupRobots, reach, grupTorretes, DMGboost):
        super().__init__(tipus,matImages, pos, damage, firerate, grupRobots, reach)
        self.grupTorretes = grupTorretes
        self.image = matImages[0][0]
        self.DMGboost = DMGboost
        self.turretBoosted=[]
        self.firestate = 0
        
    def update(self):
        
        self.image = self.matImages[0][self.firestate%6]
        self.firestate=self.firestate+1
        
    def refresh(self):
        for torreta in self.grupTorretes:
            if fn.reach(self.rect.center, torreta.rect.center, self.currentReach) and torreta is not self:
                if torreta not in self.turretBoosted and torreta.alive():
                    torreta.DMGmult=torreta.DMGmult*self.DMGboost
                    self.turretBoosted.append(torreta)
        self.currentReach = self.reach*min(self.REACHmult, conf.REACHMultLimits[self.tipus])
        
    def remove(self):
        for torreta in self.turretBoosted:
            torreta.DMGmult=torreta.DMGmult/self.DMGboost
            self.turretBoosted=[]        
        self.kill()


class Radar(Turret):
    def __init__(self, tipus, matImages, pos, damage, firerate, grupRobots, reach, grupTorretes, REACHboost):
        super().__init__(tipus, matImages, pos, damage, firerate, grupRobots, reach)
        self.grupTorretes = grupTorretes
        self.image = matImages[0][0]
        self.REACHboost = REACHboost
        self.turretBoosted=[]
        self.firestate = 0
        self.electro=0
        self.rayo = pygame.mixer.Sound(conf.rayo_sound)
        self.rayo.set_volume(0.25)
        self.sounding = False


    def update(self):
        self.firestate += r.randint(0, 15)
        self.image = self.matImages[0][int(self.electro)]
        if self.firestate>=500:
            if not self.sounding:                
                self.rayo.play()
                self.sounding = True
            self.electro +=0.5
            
            
        if self.electro == 15:
            self.firestate=0
            self.electro=0
            self.sounding = False
            

    def refresh(self):
        for torreta in self.grupTorretes:
            if fn.reach(self.rect.center, torreta.rect.center, self.currentReach) and torreta is not self:
                if torreta not in self.turretBoosted and torreta.alive():
                    torreta.REACHmult=torreta.REACHmult*self.REACHboost
                    self.turretBoosted.append(torreta)        

        self.currentReach = self.reach*min(self.REACHmult, conf.REACHMultLimits[self.tipus])

    def remove(self):
        for torreta in self.turretBoosted:
            torreta.REACHmult=torreta.REACHmult/self.REACHboost
            self.turretBoosted=[]        
        self.kill()



















        
