import conf
import functions as fn
import pygame
import main
import sprite_sheets as ss
import random as r

class Robots(pygame.sprite.LayeredUpdates):

    def __init__(self,robots,nextround):
        super().__init__()
        self.entrance = pygame.mixer.Sound(conf.robot_entrance_sound)
        self.i=0
        self.j=0
        self.robots=robots
        self.last=pygame.time.get_ticks()
        self.interval_inicial=conf.interval_inicial
        self.interval_minim=conf.interval_minim        
        self.nextround=nextround
        self.nextround.n_rondes_totals=len(robots)
        self.dec_temps=0
        self.isFinished=False
        
    def update(self):
        super().update()
        if self.nextround.activated and self.j < len(self.robots):
            self.nextround.n_ronda=self.j+1            
            now=pygame.time.get_ticks()
            self.ronda=self.robots[self.j]
        
            if ((now - self.last) >= self.interval_inicial-self.dec_temps) and self.i < len(self.ronda):
                self.add(self.ronda[self.i],layer=2)
                self.entrance.play()
                self.i+=1
                self.last=now
                if self.interval_inicial-(self.dec_temps+10)>self.interval_minim:
                    self.dec_temps+=5
                if self.i==len(self.ronda):
                    self.i=0
                    self.j+=1
                    if self.interval_inicial-(self.dec_temps+50)>self.interval_minim:
                        self.dec_temps+=30
                    self.nextround.activated=False
                    if self.j==len(self.robots):
                        self.isFinished=True
                    

class Robot(pygame.sprite.Sprite):
    def __init__(self, image, pos, speed, mov, health, vidaBase, cash, coins):
        super().__init__()
        
        self.speed = speed    #constant de velocitat (pixels per frame)
        
        self.mov = mov        #MATRIU de posibles moviments del robot. Vectors de direccions(tuples). Cada vector ve asociat a una casella del mapa
                              #Cada vector indica el moviment obligat que haurá de fer el robot al trobar-se en cada casella del mapa

        self.image = image

        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.health=health

        self.coins=coins

        self.cash=cash

        self.death = pygame.mixer.Sound(conf.robot_death_sound)
        self.death.set_volume(0.3)
        self.arrival = pygame.mixer.Sound(conf.robot_arrival_sound)
        
        self.vidaBase=vidaBase
        self.direc = (0,0)    #Direcció del moviment
        self.flickerCounter = 0
        self.chosen = False
        self.boom = ss.crea_llista_imatges(pygame.image.load(conf.sprite_explosion), 17)
        self.deathCounter = 0
        red = pygame.Surface((image.get_width(), image.get_height()), flags=pygame.SRCALPHA)
        red.fill((170, 0, 0, 0))

        self.imageLight=image.copy()
        self.imageRed = image.copy()
        self.imageRed.blit(red, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.damageDealt = conf.robotDamage
        if speed == 1:
            self.damageDealt = conf.vidaBase
            
        
    def update(self):
        if self.health <= 0:
            self.image = self.boom[self.deathCounter]
            self.deathCounter += 1
            self.speed=0
            if self.deathCounter == 1:
                self.death.play()
            if self.deathCounter >= 17:
                self.kill()
                self.cash.coins=self.cash.coins+self.coins
            
        elif self.flickerCounter == 0:
            self.image=self.imageLight
        cas, cent = fn.tileDetector((self.rect.center))     #cent es el Boolea, True si esta centrat. cas es la casella(tupla)


        

        if not cent and self.chosen:            #SEGUIMENT DEL CAMI
            self.chosen = False
        elif not cent or self.health <= 0:
            pass
        else:
            if self.mov[cas[1]][cas[0]] == (0, 0):
                self.vidaBase.dealDamage(self.damageDealt)      #MAL A LA BASE
                self.arrival.play()
                self.kill()     
                
            elif type(self.mov[cas[1]][cas[0]][0]) == tuple:       #Caselles de multiples direccions
                if self.chosen == False:
                    self.direc = r.choice(self.mov[cas[1]][cas[0]])
                    self.rect.center = (cas[0]*50-25, cas[1]*50-25)
                    self.chosen = True
                    
                
                
            elif self.direc != self.mov[cas[1]][cas[0]]:
                self.rect.center = (cas[0]*50-25, cas[1]*50-25)             #Centra el robot si ha de girar per a que no es descentri del cami
                self.direc = self.mov[cas[1]][cas[0]]       #Cambiar la direcció si fa falta


        self.rect = self.rect.move(self.direc[0]*self.speed, self.direc[1]*self.speed)    #Moure el robot




        if self.flickerCounter > 0 and not self.health <= 0:
            a=self.flickerCounter%2*2-1
            self.image.scroll(a, -a)
            self.flickerCounter -= 1

    def dealDamage(self, damage):
        if not self.health <= 0:
            self.image = self.imageRed

            self.health -= damage

            if self.flickerCounter == 0:
            
               self.flickerCounter = 6      
