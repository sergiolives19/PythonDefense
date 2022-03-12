import conf
import tile
import pygame
import rock
import robot
import turret
import math

def mapDecoder(file):       #Des d'un arxiu de mapa (.txt) retorna la matriu de lletres escrites en el mapa
    M=[]
    with open(file, 'r') as mapStr:
        for fila in mapStr:
            m=[]  #fila de la matriu M
            fila=fila.strip()
            for col in fila:
                m.append(col)
            M.append(m)                
    return M     #matriu de lletres

def posDecoder(x, y):  #Donada la fila i columna de una tile en el mapa retorna la posicio en coordenades de pygame (de la esquina superior esquerra)
    return ((x-1)*conf.midaCas, (y-1)*conf.midaCas)   #conf.midaCas = mida dels costats (en pixels) de cada casella

def mapCreator(letterMap):      #Donat una matriu de lletres retorna la LLISTA de Tiles corresponent (les tiles tenen les coordenades incorporades)
    tiles=[]
    for fila in range(len(letterMap)):
        for columna in range(len(letterMap[fila])):
            pos=posDecoder(columna,fila)
            lletra=letterMap[fila][columna]
            tile=tileCreator(lletra,pos)
            tiles.append(tile)
    return tiles



def tileCreator(lletra, pos):     #Des d'un string (lletra de la casella) retorna la tile corresponent
    
    assert len(lletra)==1
    assert type(lletra)==str
    
    if lletra in '_0123456789' :                          #  LLEGENDA de LLETRES en el MAPA DE IMATGES
        im = pygame.image.load(conf.sprite_grassQ)          
    elif lletra == 'V':
        im = pygame.image.load(conf.sprite_pathV)            
    elif lletra == 'H':
        im = pygame.image.load(conf.sprite_pathH)           
    elif lletra == 'I':
        im = pygame.image.load(conf.sprite_pathI)
    elif lletra == 'J':
        im = pygame.image.load(conf.sprite_pathJ)
    elif lletra == 'K':
        im = pygame.image.load(conf.sprite_pathK)
    elif lletra == 'L':
        im = pygame.image.load(conf.sprite_pathL)
    elif lletra == 'Z':
        im = pygame.image.load(conf.sprite_pathZ)
    elif lletra == 'A':
        im = pygame.image.load(conf.sprite_pathA)
    elif lletra == 'S':
        im = pygame.image.load(conf.sprite_pathS)
    elif lletra == 'D':
        im = pygame.image.load(conf.sprite_pathD)
    elif lletra == 'F':
        im = pygame.image.load(conf.sprite_pathF)
    elif lletra == 'v':
        im = pygame.image.load(conf.sprite_pathV)
    elif lletra == 'h':
        im = pygame.image.load(conf.sprite_pathH)
    else:
        raise "Unknown letter"              #No existeix la excepció Unknown letter pero python tirarà un error igualment

    return tile.Tile(im, pos)



def tileMap(file):
    return mapCreator(mapDecoder(file))            #FUNCIO FINAL

##
##
#FINAL DE LES FUNCIONS DEDICADES A CREAR MAPES
##
##

def rockMap(file):
    return rockCreator(mapDecoder(file))

def rockCreator(letterMap):      #Donat una matriu de lletres retorna la LLISTA de Rocks corresponent (les Rocks tenen les coordenades incorporades)
    roques=[]
    for fila in range(len(letterMap)):
        for columna in range(len(letterMap[fila])):
            if letterMap[fila][columna] not in "123456789":
                pass
            else:
                pos=posDecoder(columna,fila)
                index=letterMap[fila][columna]
                roca=rockSpawner(index, pos)
                roques.append(roca)
    return roques

    

def rockSpawner(index, pos):
    
    assert len(index)==1
    assert type(index)==str
    
    if index == "1":                                        #
        im = pygame.image.load(conf.sprite_rock1x2)
    elif index == "2":                                      #       LLEGENDA de LLETRES en el MAPA DE IMATGES referent a ROQUES(i arbres)
        im = pygame.image.load(conf.sprite_rock2x2)
    elif index == "3":                                      #
        im = pygame.image.load(conf.sprite_tree1)
    elif index == "4":                                      #
        im = pygame.image.load(conf.sprite_forest1)
    elif index == "8":                                      #
        im = pygame.image.load(conf.sprite_plant1)          
    else:
        print ("NOMBRE NO VALID EN EL MAPA")

    return rock.Rock(im, pos)

    



def tileDetector(pos):           #Donada la posicio de un punt, retorna les coordenades de la casella on es troba
                                 #i si el punt esta centrat (dins de un marge d'error) True=punt centrat

                                 #Ho necessitem per a saber si el robot ha de girar per a seguir el cami
    
    return (pos[0]//50+1, pos[1]//50+1), abs(pos[0]%50-25)<=conf.margeError and abs(pos[1]%50-25)<=conf.margeError
    


def dirDecoder(way):            #Donada una direcció Right, Left, Up, Down; o direccions múltiples; retorna el (o els) vector(s) unitari(s) corresponent
    assert len(way)==1
    assert type(way)==str
    
    if way == "R":
        return (1, 0)               #
    elif way == "L":
        return (-1, 0)              #
    elif way == "U":
        return (0, -1)              #  LLEGENDA de LLETRES en el MAPA DE MOVIMENT
    elif way == "D":
        return (0, 1)               #
    elif way == "V":
        return ((0, -1), (0, 1))    # Up-Down
    elif way == "H":
        return ((-1, 0), (1, 0))    # Left-Right
    elif way == "W":
        return ((1, 0), (0, -1))    # Up-Right
    elif way == "Q":
        return ((-1, 0), (0, -1))   # Up-Left
    elif way == "A":
        return ((-1, 0), (0, 1))    # Down-Left
    elif way == "S":
        return ((1, 0), (0, 1))     # Down-Right
    else:
        return (0, 0)


####
##ROBOTS
###

def robotDecoder(llista_de_llistes_tipus_robot,vidaBase,cash,entrada,mapmov):
    lres1=[]      
    imr1 = pygame.image.load(conf.sprite_robot1)
    imr2 = pygame.image.load(conf.sprite_robot2)
    imr3 = pygame.image.load(conf.sprite_robot3)
    imr4 = pygame.image.load(conf.sprite_robot4)
    imr5 = pygame.image.load(conf.sprite_robot5)
    imr6 = pygame.image.load(conf.sprite_robot6)
    imr7 = pygame.image.load(conf.sprite_robot7)
    imr8 = pygame.image.load(conf.sprite_robot8)
    imr9 = pygame.image.load(conf.sprite_robot9)
    imr10 = pygame.image.load(conf.sprite_robot10)
    imr11 = pygame.image.load(conf.sprite_robot11)
    matrMov = robotMap(mapmov)
    for ronda in llista_de_llistes_tipus_robot:
        lres2=[]      
        for tipus_robot in ronda:
            if tipus_robot=='r1':
                lres2.append(robot.Robot(imr1.copy(),entrada,conf.speed_robot1,matrMov,conf.health_robot1,vidaBase,cash,conf.coins_robot1))
            elif tipus_robot=='r2':
                lres2.append(robot.Robot(imr2.copy(),entrada,conf.speed_robot2,matrMov,conf.health_robot2,vidaBase,cash,conf.coins_robot2))
            elif tipus_robot=='r3':
                lres2.append(robot.Robot(imr3.copy(),entrada,conf.speed_robot3,matrMov,conf.health_robot3,vidaBase,cash,conf.coins_robot3))
            elif tipus_robot=='r4':
                lres2.append(robot.Robot(imr4.copy(),entrada,conf.speed_robot4,matrMov,conf.health_robot4,vidaBase,cash,conf.coins_robot4))
            elif tipus_robot=='r5':
                lres2.append(robot.Robot(imr5.copy(),entrada,conf.speed_robot5,matrMov,conf.health_robot5,vidaBase,cash,conf.coins_robot5))
            elif tipus_robot=='r6':
                lres2.append(robot.Robot(imr6.copy(),entrada,conf.speed_robot6,matrMov,conf.health_robot6,vidaBase,cash,conf.coins_robot6))
            elif tipus_robot=='r7':
                lres2.append(robot.Robot(imr7.copy(),entrada,conf.speed_robot7,matrMov,conf.health_robot7,vidaBase,cash,conf.coins_robot7))
            elif tipus_robot=='r8':
                lres2.append(robot.Robot(imr8.copy(),entrada,conf.speed_robot8,matrMov,conf.health_robot8,vidaBase,cash,conf.coins_robot8))
            elif tipus_robot=='r9':
                lres2.append(robot.Robot(imr9.copy(),entrada,conf.speed_robot9,matrMov,conf.health_robot9,vidaBase,cash,conf.coins_robot9))
            elif tipus_robot=='r10':
                lres2.append(robot.Robot(imr10.copy(),entrada,conf.speed_robot10,matrMov,conf.health_robot10,vidaBase,cash,conf.coins_robot10))
            elif tipus_robot=='r11':
                lres2.append(robot.Robot(imr11.copy(),entrada,conf.speed_robot11,matrMov,conf.health_robot11,vidaBase,cash,conf.coins_robot11))

               
        lres1.append(lres2)
    return lres1

#Moviment dels robots

def robotMap(file):
    return movCreator(mapDecoder(file))         #FUNCIO FINAL; Donat el arxiu de moviments del mapa, retorna una matriu de vectors de moviment


def movCreator(letterMap):              #Donada la matriu de lletres de moviment, retorna la matriu de vectors.
    vectors=[]
    for fila in letterMap:
        f=[]
        for lletra in fila:
            v=dirDecoder(lletra)
            f.append(v)
        vectors.append(f)
    return vectors


####
##EVENT HANDLER
###

def refresh(grupTorretes):
    for torreta in grupTorretes:
        torreta.refresh()

def buildable(pos_ese, mapa, grupTorretes):
    cas=pos_ese[0]//50+1, pos_ese[1]//50+1
    c1=cas[0]
    c2=cas[1]
    M=mapDecoder(mapa)
    for torreta in grupTorretes:
        pos=torreta.rect.topleft
        if pos == pos_ese:
            return False       
    if 1<=c2<=conf.alçadaMapa and 1<=c1<=conf.ampladaMapa:
        lletra=M[c2][c1]
        if lletra in conf.construible:
            return True
    else:
        return False

def turretBuilder(pos, im, tipus, mapa, grupTorretes, grupRobots):
    pos_ese = ((pos[0]//50)*50, (pos[1]//50)*50)
    
    if buildable(pos_ese, mapa, grupTorretes):

        if tipus == "machineGun":
            DMG = conf.DMG_machineGun
            firerate = conf.firerate_machineGun
            reach = conf.reach_machineGun
            torreta=turret.Turret(tipus, im, pos_ese, DMG, firerate, grupRobots, reach)
        elif tipus == "cannon":
            DMG = conf.DMG_cannon
            firerate = conf.firerate_cannon
            reach = conf.reach_cannon
            torreta=turret.Turret(tipus, im, pos_ese, DMG, firerate, grupRobots, reach)
        elif tipus == "generator":
            DMG = 0
            firerate = 0
            reach = conf.reach_generator
            DMGboost = conf.DMG_boost_generator
            torreta=turret.Generator(tipus, im, pos_ese, DMG, firerate, grupRobots, reach,
                                  grupTorretes, DMGboost)
        elif tipus == "radar":
            DMG = 0
            firerate = 0
            reach = conf.reach_radar
            REACHboost = conf.reach_boost_radar
            torreta=turret.Radar(tipus, im, pos_ese, DMG, firerate, grupRobots, reach,
                                 grupTorretes, REACHboost)           
        
        return torreta

####
##DISPARAR TORRETES
####
    
def angle(posTurret, posRobot):
    deltaX=posRobot[0]-posTurret[0]    
    deltaY=posRobot[1]-posTurret[1]
    alpha = math.degrees(math.atan2(deltaY, deltaX))
    return (alpha+360)%360
    
def quadrant(angle, nombre_quadrants):
    marge_quadrant = 360/nombre_quadrants
    alpha = angle+marge_quadrant/2
    Qres = alpha//marge_quadrant
    return int(Qres)

def reach(posTurret, posRobot, R):

    return R > math.sqrt((posTurret[0]-posRobot[0])**2+(posTurret[1]-posRobot[1])**2)

def casella_ese(pos):
    t=conf.midaCas
    pos_ese = ((pos[0]//t)*t, (pos[1]//t)*t)
    return pos_ese

def casella_centre(pos):
    t=conf.midaCas
    pos_centre = ((pos[0]//t)*t+t/2, (pos[1]//t)*t-t/2)
    return pos_centre   




####
## MISCELANEA
####

def renderLongText(font, surface, text, deltaY, maxX, sangria, startingY):
    size_Space = font.render(" ", True, (0,0,0)).get_size()[0]
    textList = text.split()
    currentX = sangria
    currentY = startingY
    for word in textList:
        wordImage = font.render(word, True, (0,0,0))
        width, height = wordImage.get_size()
        if currentX+width >= maxX:
            currentY = currentY+deltaY
            currentX = sangria
        surface.blit(wordImage, (currentX, currentY))
        currentX += width+size_Space        




