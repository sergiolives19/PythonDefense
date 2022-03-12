# Pygame
import pygame
from pygame.locals import *

# PGU
import engine

# Mòduls propis
import conf
import sprite_sheets as ss
import functions as fn
import robot
import turret
import HUD
import life
import money

# Classe joc
class Joc(engine.Game):

    # Initialize screen, pygame modules, clock... and states.
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode(conf.mides_pantalla, SWSURFACE)
        self.crono = pygame.time.Clock()
        self._init_state_machine()
        
        # Creates and stores all states as attributes
    def _init_state_machine(self):
        self.jugant1 = Jugant(self,cas=conf.mapcas1,mov=conf.mapmov1,enemics=conf.enemics1)
        self.jugant2 = Jugant(self,cas=conf.mapcas2,mov=conf.mapmov2,enemics=conf.enemics2)
        self.jugant3 = Jugant(self,cas=conf.mapcas3,mov=conf.mapmov3,enemics=conf.enemics3)
        self.jugant4 = Jugant(self,cas=conf.mapcas4,mov=conf.mapmov4,enemics=conf.enemics4)
        self.pause = Pause(self)
        self.mainMenu = MainMenu(self)
        self.secondaryMenu = SecondaryMenu(self)
        self.quit_state = engine.Quit(self)
        self.win = Win(self)
        self.lose = Lose(self)

    # Calls the main loop with the initial state.
    def run(self): 
        super().run(self.mainMenu, self.screen)

    def change_state(self, transition=None):
        """
        Implements the automat for changing the state of the game.
        Given self.state and an optional parameter indicating 
        the kind of transition, computes and returns the new state
        """
        
        if self.state is self.mainMenu:
            if transition == 'NEXT':
                new_state = self.secondaryMenu
            elif transition == 'QUIT':
                new_state=self.quit_state
            else:
                raise ValueError('Unknown transition indicator')

        elif self.state is self.secondaryMenu:
            if transition == 'PLAY1':
                new_state = self.jugant1
                new_state.init()
            elif transition == 'PLAY2':
                new_state = self.jugant2
                new_state.init()
            elif transition == 'PLAY3':                
                new_state = self.jugant3
                new_state.init()
            elif transition == 'PLAY4':                
                new_state = self.jugant4
                new_state.init()                
            elif transition == 'BACK':
                new_state = self.mainMenu
            else:
                raise ValueError('Unknown transition indicator')

        elif self.state in (self.jugant1,self.jugant2,self.jugant3, self.jugant4):
            if transition == 'PAUSE':
                self.ant_jugant = self.state
                new_state = self.pause
                pygame.mixer.pause()
            elif transition == 'WIN':
                new_state = self.win
            elif transition == 'LOSE':
                new_state = self.lose
            else:
                raise ValueError('Unknown transition indicator')
            
        elif self.state is self.pause:
            if transition == 'PLAY':
                new_state = self.ant_jugant
            elif transition == 'LOSE':
                defeat = pygame.mixer.Sound(conf.defeat_sound)
                defeat.play()
                new_state = self.lose
            else:
                raise ValueError('Unknown transition indicator')

        elif self.state is self.win:
            new_state = self.mainMenu
            new_state.init()
            
        elif self.state is self.lose:
            new_state = self.mainMenu
            new_state.init()
            
        else:
            raise ValueError('Unknown game state value')
            
        return new_state    

    # Tick is called once per frame. It shoud control de timing.
    def tick(self):
        self.crono.tick(conf.fps)   # Limits the maximum FPS


class Pause(engine.State):        

    def init(self):
        centre=tuple(map(lambda x: x//2, conf.mides_pantalla))
        image = pygame.image.load(conf.sprite_buttonSurrender)
        self.grupHUDbutton = pygame.sprite.LayeredUpdates()
        self.buttonSurrender = HUD.SimpleButton(image,(0,0))
        self.buttonSurrender.rect.center = centre
        self.grupHUDbutton.add(self.buttonSurrender)
        
    def paint(self, screen):
        screen.fill((100, 100, 100), special_flags=BLEND_MULT)
        self.grupHUDbutton.draw(screen)
        pygame.display.flip()      
        
    def event(self,event): 
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE or event.key == K_p:
                pygame.mixer.music.unpause()
                return self.game.change_state('PLAY')
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:            
            if self.buttonSurrender.pressed(event.pos):
                #self.buttonSurrender.kill()
                return self.game.change_state('LOSE')

    def loop(self):
        self.grupHUDbutton.update()      


class MainMenu(engine.State):   
    
    def init(self):

        pygame.mixer.init()
        pygame.mixer.music.load(conf.intro_music)
        pygame.mixer.set_num_channels(16)
        pygame.mixer.music.play(-1)
        
        
        self.buttonPlay = pygame.image.load(conf.sprite_buttonPlay)
        self.buttonQuit = pygame.image.load(conf.sprite_buttonQuit)
        
        self.grupHUDbutton = pygame.sprite.LayeredUpdates()
        self.grupHUDmenu = pygame.sprite.LayeredUpdates()
        
        centre=tuple(map(lambda x: x//2, conf.mides_pantalla))
        
        self.buttonPlay = HUD.SimpleButton(self.buttonPlay,(0,0))
        self.buttonPlay.rect.center = centre[0],centre[1]-30
        self.buttonQuit = HUD.SimpleButton(self.buttonQuit,(0,0))
        self.buttonQuit.rect.center = centre[0],centre[1]+180
        self.grupHUDbutton.add(self.buttonPlay,self.buttonQuit)

        margeY = 50
        
        titleImage = pygame.image.load(conf.sprite_title)
        title = HUD.Menu(titleImage, (0,0))
        title.rect.center = (centre[0], margeY)
        drawerImage = pygame.image.load(conf.sprite_drawer)
        drawer = HUD.Menu(drawerImage, (0,0))
        drawer.rect.center = (centre[0], centre[1]+70)
        backgroundImage = pygame.image.load(conf.sprite_background)
        background = HUD.Menu(backgroundImage, (0,0))
        
        self.grupHUDmenu.add(title, layer=1)
        self.grupHUDmenu.add(drawer, layer=2)
        self.grupHUDmenu.add(background, layer=0)

    def paint(self, screen):
        self.update(screen)
        
    def event(self,event):
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:            
            if self.buttonPlay.pressed(event.pos):
                return self.game.change_state('NEXT')
            elif self.buttonQuit.pressed(event.pos):
                return self.game.change_state('QUIT')


    def loop(self):
        self.grupHUDmenu.update()
        self.grupHUDbutton.update()      

    def update(self,screen):

        self.grupHUDmenu.draw(screen)
        self.grupHUDbutton.draw(screen)        
        pygame.display.flip()        

class SecondaryMenu(engine.State):
    
    def init(self):
        centre=tuple(map(lambda x: x//2, conf.mides_pantalla))
        
        #image = pygame.image.load(conf.sprite_mainMenu)
        #menu = HUD.Menu(image, (0,0))
        #menu.rect.center=(centre[0], centre[1]+50)
        
        imageMap1 = pygame.image.load(conf.sprite_buttonMap1)
        imageMap2 = pygame.image.load(conf.sprite_buttonMap2)
        imageMap3 = pygame.image.load(conf.sprite_buttonMap3)
        imageMap4 = pygame.image.load(conf.sprite_buttonMap4)
        imageBack = pygame.image.load(conf.sprite_buttonBack)
        
        self.grupHUDbutton = pygame.sprite.LayeredUpdates()
        self.grupHUDmenu = pygame.sprite.LayeredUpdates()       
               
        sep=107
        cent=42+50-20
        
        self.buttonMap1 = HUD.SimpleButton(imageMap1,(0,0))
        self.buttonMap1.rect.center = centre[0],centre[1]+cent-2*sep

        self.buttonMap2 = HUD.SimpleButton(imageMap2,(0,0))
        self.buttonMap2.rect.center = centre[0],centre[1]+cent-1*sep

        self.buttonMap3 = HUD.SimpleButton(imageMap3,(0,0))
        self.buttonMap3.rect.center = centre[0],centre[1]+cent-0*sep

        self.buttonMap4 = HUD.SimpleButton(imageMap4,(0,0))
        self.buttonMap4.rect.center = centre[0],centre[1]+cent+1*sep

        self.buttonBack = HUD.SimpleButton(imageBack,(0,0))
        self.buttonBack.rect.center = centre[0],centre[1]+cent+2*sep
        
        self.grupHUDbutton.add(self.buttonMap1,self.buttonMap2,self.buttonMap3,self.buttonMap4,self.buttonBack, layer=5)

        margeY = 50
        
        titleImage = pygame.image.load(conf.sprite_title)
        title = HUD.Menu(titleImage, (0,0))
        title.rect.center = (centre[0], margeY)
        drawerImage = pygame.image.load(conf.sprite_drawer)
        drawer = HUD.Menu(drawerImage, (0,0))
        drawer.rect.center = (centre[0], centre[1]+70)
        backgroundImage = pygame.image.load(conf.sprite_background)
        background = HUD.Menu(backgroundImage, (0,0))
        
        self.grupHUDmenu.add(title, layer=1)
        self.grupHUDmenu.add(drawer, layer=2)
        self.grupHUDmenu.add(background, layer=0)
    
    def paint(self, screen):

        self.update(screen)

    def event(self,event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            if self.buttonMap1.pressed(event.pos):
                return self.game.change_state('PLAY1')

            elif self.buttonMap2.pressed(event.pos):
                return self.game.change_state('PLAY2')

            elif self.buttonMap3.pressed(event.pos):
                return self.game.change_state('PLAY3')

            elif self.buttonMap4.pressed(event.pos):
                return self.game.change_state('PLAY4')

            elif self.buttonBack.pressed(event.pos):
                return self.game.change_state('BACK')

    def loop(self):
        self.grupHUDmenu.update()
        self.grupHUDbutton.update()      

    def update(self,screen):

        self.grupHUDmenu.draw(screen)
        self.grupHUDbutton.draw(screen)        
        pygame.display.flip()   
            
class Win(engine.State):
    
    def init(self):
        self.image = pygame.image.load(conf.sprite_victoryLetters)
    
    def paint(self, s):
        s.fill((0, 255, 0), special_flags=BLEND_MULT)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()

    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            return self.game.change_state()
           
class Lose(engine.State):
    
    def init(self):
        self.image = pygame.image.load(conf.sprite_gameoverLetters)
    
    def paint(self, s):
        s.fill((255, 0, 0), special_flags=BLEND_MULT)
        rect = self.image.get_rect()
        rect.center = s.get_rect().center
        s.blit(self.image, rect)
        pygame.display.flip()       

    def event(self,e): 
        if e.type == pygame.KEYDOWN:
            return self.game.change_state()

# A state may subclass engine.State.
class Jugant(engine.State):

    # The init method should load data, etc.  The __init__ method
    # should do nothing but record the parameters.  If the init method
    # returns a value, it becomes the new state.

    def __init__(self, game, cas=conf.mapcas1,mov=conf.mapmov1,enemics=conf.enemics1):
        super().__init__(game)
        self.cas=cas             # Arxiu de text de caselles del mapa
        self.mov=mov             # Arxiu de text de vectors del mapa
        self.enemics = enemics        

    def init(self):

        #Música
        pygame.mixer.init()
        pygame.mixer.music.load(conf.background_music)
        pygame.mixer.music.set_volume(0.45)
        pygame.mixer.music.play(-1)

        #grups de sprites
        
        self.grupMap = pygame.sprite.LayeredUpdates()  
        self.grupRocks = pygame.sprite.LayeredUpdates()
        self.grupTurrets = pygame.sprite.LayeredUpdates()
        self.grupHUDbutton = pygame.sprite.LayeredUpdates()
        self.grupHUDmenu = pygame.sprite.LayeredUpdates()
        self.grupExplosions = pygame.sprite.LayeredUpdates()

        #-----------Menus

        imMenuLower = pygame.image.load(conf.sprite_menuLower)
        self.menuTopLeft = (0, conf.mides_pantalla[1] - 170)
        self.menuLower = HUD.Menu(imMenuLower, self.menuTopLeft)
        self.grupHUDmenu.add(self.menuLower, layer=0)

        self.mides_turretInfo=(140, 150)
        self.pos_turretInfo=(600, self.menuTopLeft[1]+10)

        sep = 50
        margeY=10
        botoX=220
        botoY=45
        
        #----------NextRound
        
        self.nextround = HUD.NextRound((conf.mides_pantalla[0]-250,self.menuTopLeft[1]+margeY+0*sep),(botoX,botoY))
        self.grupHUDmenu.add(self.nextround,layer=5)

        #-----------Money

        self.cash=         money.Money((conf.mides_pantalla[0]-250,self.menuTopLeft[1]+margeY+1*sep),(botoX,botoY),conf.initial_cash)
        self.grupHUDmenu.add(self.cash, layer=5)
        

        #-----------Vida
        
        self.vidaBase =      life.Life((conf.mides_pantalla[0]-250,self.menuTopLeft[1]+margeY+2*sep),(botoX,botoY),conf.vidaBase) 
        self.grupHUDmenu.add(self.vidaBase, layer=5)

        #---------------Definició del Mapa
        
        self.grupMap.add(fn.tileMap(self.cas), layer=1)
        matriu_lletres_mapa = fn.mapDecoder(self.cas)
        for filai in range(len(matriu_lletres_mapa)):
            for columnai in range(len(matriu_lletres_mapa[filai])):
                lletra = matriu_lletres_mapa[filai][columnai]
                if lletra == "v" or lletra=='h':
                    cas_entrada_topleft=fn.posDecoder(filai, columnai)
                    entrada = (cas_entrada_topleft[1]+25, cas_entrada_topleft[0]+25)        #ENTRADA DELS ROBOTS
                    break

        #---------------Definició de les Roques       

        self.grupRocks.add(fn.rockMap(self.cas), layer=3)

        #---------------Definició dels Robots             
        
        self.grupRobots = robot.Robots(fn.robotDecoder(self.enemics,self.vidaBase,self.cash,entrada,self.mov),self.nextround)
        

        #---------------IMATGES
        #-----------Torretes

        machineGun_SpriteSheet = pygame.image.load(conf.machineGun_SpriteSheet)
        self.machineGun_SpriteMatrix = ss.crea_matriu_imatges(machineGun_SpriteSheet, 13, 16)

        cannon_SpriteSheet = pygame.image.load(conf.cannon_SpriteSheet)
        self.cannon_SpriteMatrix = ss.crea_matriu_imatges(cannon_SpriteSheet, 13, 16)

        generator_SpriteSheet = pygame.image.load(conf.generator_SpriteSheet)
        self.generator_SpriteMatrix = ss.crea_matriu_imatges(generator_SpriteSheet, 1, 16)
      
        radar_SpriteSheet = pygame.image.load(conf.radar_SpriteSheet)
        self.radar_SpriteMatrix = ss.crea_matriu_imatges(radar_SpriteSheet, 1, 16)

        self.imMachineGun = self.machineGun_SpriteMatrix[0][0]
        self.imCannon = self.cannon_SpriteMatrix[0][0]
        self.imGenerator = self.generator_SpriteMatrix[0][0]
        self.imRadar = self.radar_SpriteMatrix[0][0]
        
        self.torreta_a_construir=''                             

        #-----------BOTONS
        self.imButtonDelete = pygame.image.load(conf.sprite_buttonDelete)
        #-----------De Torretes
        imButtonMachineGun = pygame.image.load(conf.sprite_buttonMachineGun)
        imButtonCannon = pygame.image.load(conf.sprite_buttonCannon) 
        imButtonGenerator = pygame.image.load(conf.sprite_buttonGenerator)
        imButtonRadar = pygame.image.load(conf.sprite_buttonRadar)

        imButtonInf = pygame.image.load(conf.sprite_buttonInf)
        
        sep=85
        margeX=30
        margeY=20

        self.buttonCannon = HUD.Button(imButtonCannon, (self.menuTopLeft[0]+margeX+0*sep
                                     , self.menuTopLeft[1]+margeY), self.cash, "cannon")
        self.buttonInfCannon = HUD.SimpleButton(imButtonInf,(self.menuTopLeft[0]+margeX+0*sep+60
                                     , self.menuTopLeft[1]+margeY),"infCannon")
        self.grupHUDbutton.add(self.buttonCannon,self.buttonInfCannon, layer=3)
        
        self.buttonMachineGun = HUD.Button(imButtonMachineGun, (self.menuTopLeft[0]+margeX+1*sep
                                     , self.menuTopLeft[1]+margeY), self.cash, "machineGun")
        self.buttonInfMachineGun = HUD.SimpleButton(imButtonInf,(self.menuTopLeft[0]+margeX+1*sep+60
                                     , self.menuTopLeft[1]+margeY),"infMachineGun")
        self.grupHUDbutton.add(self.buttonMachineGun,self.buttonInfMachineGun, layer=3)

        self.buttonradar = HUD.Button(imButtonRadar, (self.menuTopLeft[0]+margeX+2*sep
                                     , self.menuTopLeft[1]+margeY), self.cash, "radar")
        self.buttonInfRadar = HUD.SimpleButton(imButtonInf,(self.menuTopLeft[0]+margeX+2*sep+60
                                     , self.menuTopLeft[1]+margeY),"infRadar")
        self.grupHUDbutton.add(self.buttonradar,self.buttonInfRadar, layer=3)

        self.buttongenerator = HUD.Button(imButtonGenerator, (self.menuTopLeft[0]+margeX+3*sep
                                     , self.menuTopLeft[1]+margeY), self.cash, "generator")
        self.buttonInfGenerator = HUD.SimpleButton(imButtonInf,(self.menuTopLeft[0]+margeX+3*sep+60
                                     , self.menuTopLeft[1]+margeY),"infGenerator")
        self.grupHUDbutton.add(self.buttongenerator,self.buttonInfGenerator, layer=3)

        #------------Estats Booleans

        self.has_turret_selected = False      
        self.turretImage = None
        self.has_turret_clicked = False
        self.has_info_clicked = False
        self.finished=False
        self.last=''
        self.estat=''

        #-------------Sons
        
        self.defeatSound = pygame.mixer.Sound(conf.defeat_sound)
        self.victorySound = pygame.mixer.Sound(conf.victory_sound)
        self.turretSound = pygame.mixer.Sound(conf.build_tower_sound)
        self.roundSound = pygame.mixer.Sound(conf.next_round_sound)
        self.roundSound.set_volume(0.65)
        self.del_turretSound = pygame.mixer.Sound(conf.delete_turret_sound)
        self.selectSound = pygame.mixer.Sound(conf.select_turret_sound)



        #-------------Torretes model
        self.modelMachineGun=turret.Turret("machineGun", self.machineGun_SpriteMatrix, (0,0),
                                            conf.DMG_machineGun, conf.firerate_machineGun, "robots", conf.reach_machineGun)
        self.modelCannon=turret.Turret("cannon", self.cannon_SpriteMatrix, (0,0),
                                            conf.DMG_cannon, conf.firerate_cannon, "robots", conf.reach_cannon)
        self.modelGenerator=turret.Generator("generator", self.generator_SpriteMatrix, (0,0),
                                            conf.DMG_generator, conf.firerate_generator, "robots", conf.reach_generator, "torretes", conf.DMG_boost_generator)
        self.modelRadar=turret.Radar("radar", self.radar_SpriteMatrix, (0,0),
                                            conf.DMG_radar, conf.firerate_radar, "robots", conf.reach_radar, "torretes", conf.reach_boost_radar)
        

    # The paint method is called once.  If you call repaint(), it
    # will be called again.
    def paint(self,screen):
        self.update(screen)

    # Every time an event occurs, event is called.  If the event
    # method returns a value, it will become the new state.
    def event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:

            self.has_turret_selected = False
            try:
                self.icon.kill()
            except AttributeError:
                pass                                       
            try:
                self.turretInfo.kill() 
            except AttributeError:
                pass
            try:
                self.cercle.kill()
            except AttributeError:
                pass 
            
        if event.type == pygame.KEYDOWN:
            if event.key == K_r:
                fn.refresh(self.grupTurrets)
            
            if event.key == K_ESCAPE or event.key == K_p:
                pygame.mixer.music.pause()
                return self.game.change_state('PAUSE')
            elif event.key == K_SPACE and len(self.grupRobots)==0:
                self.nextround.activated = True
                self.roundSound.play()
            elif event.key == K_m:
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.play(-1)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:      #Si ha clicat algo...

            if self.has_info_clicked:
                self.turretInfo.kill()
                self.has_info_clicked=False
            
            if self.has_turret_clicked:
                self.turretInfo.kill()
                self.has_info_clicked=False
                self.cercle.kill()
                self.has_turret_clicked=False
                if self.delete.pressed(event.pos):
                    self.cash.coins += 0.5*conf.prices[self.torreta_a_eliminar.tipus]
                    self.torreta_a_eliminar.remove()
                    fn.refresh(self.grupTurrets)
                    if type(self.torreta_a_eliminar)==turret.Radar or type(self.torreta_a_eliminar)==turret.Generator:
                        fn.refresh(self.grupTurrets)
                        fn.refresh(self.grupTurrets)
                        fn.refresh(self.grupTurrets)
                    self.del_turretSound.play()
                self.delete.kill()
                
            if self.nextround.pressed(event.pos) and len(self.grupRobots)==0:                 
                self.nextround.activated=True
                self.roundSound.play()           
            
            if self.has_turret_selected == False:       #I no te cap torreta seleccionada...
                
                for button in self.grupHUDbutton:
                    if button.pressed(event.pos):       #Ha presionat un botó
                        
                        if button.tipus[0:3] == "inf":

                            if button.tipus=="infMachineGun":
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelMachineGun)

                            elif button.tipus=="infCannon":
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelCannon)                                

                            elif button.tipus=="infGenerator":
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelGenerator)

                            elif button.tipus=="infRadar":
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelRadar)

                            self.grupHUDmenu.add(self.turretInfo, layer=14)
                            self.has_info_clicked=True                            

                        elif conf.prices[button.tipus]<=self.cash.coins:        #conf.prices diccionari{tipus:preu}                                           

                            if button.tipus=="machineGun":
                                self.torreta_a_construir="machineGun"
                                self.turretImage = self.machineGun_SpriteMatrix
                                self.icon = HUD.Icon(self.imMachineGun, conf.reach_machineGun)
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelMachineGun)
                                
                            elif button.tipus=="cannon":
                                self.torreta_a_construir="cannon"
                                self.turretImage = self.cannon_SpriteMatrix
                                self.icon = HUD.Icon(self.imCannon, conf.reach_cannon)
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelCannon)

                            elif button.tipus=="generator":
                                self.torreta_a_construir="generator"
                                self.turretImage = self.generator_SpriteMatrix
                                self.icon = HUD.Icon(self.imGenerator, conf.reach_generator)
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelGenerator)

                            elif button.tipus=="radar":
                                self.torreta_a_construir="radar"
                                self.turretImage = self.radar_SpriteMatrix
                                self.icon = HUD.Icon(self.imRadar, conf.reach_radar)
                                self.turretInfo=HUD.TurretInfo(self.mides_turretInfo, self.pos_turretInfo, self.modelRadar)
                                
                            self.grupHUDmenu.add(self.icon, layer=4)
                            self.grupHUDmenu.add(self.turretInfo, layer=14)
                            self.has_turret_selected = True                       

                for torreta in self.grupTurrets:                        # I ha clicat una torreta en el camp
                    if torreta.pressed(event.pos):
                        fn.refresh(self.grupTurrets)
                        self.selectSound.play()
                        self.torreta_a_eliminar=torreta
                        self.cercle = HUD.Reach(torreta.rect.center,int(torreta.currentReach))
                        self.delete=HUD.SimpleButton(self.imButtonDelete,(fn.casella_ese(event.pos)[0]+30,fn.casella_ese(event.pos)[1]))

                        self.turretInfo=HUD.TurretInfo((140, 150),(600, self.menuTopLeft[1]+10), torreta)
                        self.grupHUDmenu.add(self.turretInfo, layer=14)

                        
                        self.grupHUDmenu.add(self.cercle)
                        self.grupHUDbutton.add(self.delete)
                        self.has_turret_clicked=True
                        
                        

            elif self.has_turret_selected == True:        #I si que te alguna torreta seleccionada...
                
                torreta=fn.turretBuilder(event.pos, self.turretImage, self.torreta_a_construir, self.cas,
                                  self.grupTurrets, self.grupRobots)             
                                                                    
                if torreta==None or torreta.rect.center[1] > self.menuTopLeft[1]:
                    self.icon.kill()
                    self.has_turret_selected = False
                    self.turretInfo.kill()

                else:                    
                    self.grupTurrets.add(torreta)
                    
                    self.turretSound.play()
                    
                    self.icon.kill()
                    self.turretInfo.kill()
                    
                    self.has_turret_selected = False
                    self.cash.build_turret(self.torreta_a_construir)
                    fn.refresh(self.grupTurrets)
                    if type(torreta)==turret.Radar or type(torreta)==turret.Generator:
                        fn.refresh(self.grupTurrets)
                        fn.refresh(self.grupTurrets)
                        fn.refresh(self.grupTurrets)                    

    
    # Loop is called once a frame.  It should contain all the logic.
    # If the loop method returns a value it will become the new state.
    def loop(self):

        #self.grupMap.update()
        #self.grupRocks.update()
        self.grupRobots.update()       
        self.grupHUDmenu.update()
        self.grupTurrets.update()
        self.grupHUDbutton.update()
        self.grupExplosions.update()
        #self.grup.update()

        if self.vidaBase.health <= 0 and not self.finished:
            self.last=pygame.time.get_ticks()
            self.estat='LOSE'
            self.finished=True

        elif self.grupRobots.isFinished and len(self.grupRobots)==0 and not self.finished:
            self.last=pygame.time.get_ticks()
            self.estat='WIN'
            self.finished=True

        if self.finished:
            now=pygame.time.get_ticks()
            if now-self.last>2000:
                pygame.mixer.music.stop()
                if self.estat=='LOSE':
                    self.defeatSound.play()
                else:
                    self.victorySound.play()
                return self.game.change_state(self.estat)
            

    # Update is called once a frame.  It should update the display.
    def update(self,screen):
        
        screen.fill(conf.color_fons)
        self.grupExplosions.draw(screen)
        self.grupMap.draw(screen)
        self.grupRocks.draw(screen)
        self.grupRobots.draw(screen)
        self.grupTurrets.draw(screen)
        self.grupHUDmenu.draw(screen)
        self.grupHUDbutton.draw(screen)
        pygame.display.flip()
        #self.grup.draw(screen)

# Programa principal
def main():
    game = Joc()
    game.run()    


# Crida el programa principal només si s'executa el mòdul:
#
#   python3 joc.py
#
# o bé
#
#   python3 -m joc
#
# Importa les funcions i les classes, però no executa el programa
# principal si s'importa el mòdul:
#
#   import joc
if __name__ == "__main__":
    main()
