# Variables globals amb valors per configurar el joc


# Nombre màxim d'imatges per segon (fps)
fps = 30

# ------COLORS
color_fons = 95, 157, 15
color_vida = 100, 180, 0
color_vida_fons = 50, 10, 10
color_money_fons = 50, 50, 180
color_next_round = 192, 64, 64
color_reach = 100, 180, 250, 120
color_menuGrey = 129, 137, 140

# ------SONS
intro_music = "So/musica_intro.mp3"
background_music = "So/musica_joc_fons.mp3"
cannon_shot_sound = "So/dispar_cano.wav"
machineGun_shot_sound="So/dispar_ametralladora2.wav"
victory_sound = "So/victoria.wav"
defeat_sound = "So/derrota.wav"
robot_death_sound = "So/mort_robot.wav"
build_tower_sound = "So/torreta_construida.wav"
next_round_sound = "So/alarma.wav"
delete_turret_sound = "So/torreta_eliminada.wav"
select_turret_sound = "So/torreta_seleccionada.wav"
rayo_sound = "So/rayo.wav"
robot_entrance_sound = "So/entrada_robot.wav"
robot_arrival_sound = "So/arribada_robot.wav"

dicShots={"machineGun":machineGun_shot_sound,"cannon":cannon_shot_sound}

# Zona construible
construible="_Q89"

############ MAPA
# Arxius dels Mapes

mapcas1 = "Maps/map1.txt"
mapmov1 = "Maps/mov1.txt"

mapcas2 = "Maps/map2.txt"
mapmov2 = "Maps/mov2.txt"

mapcas3 = "Maps/map3.txt"
mapmov3 = "Maps/mov3.txt"

mapcas4 = "Maps/map4.txt"
mapmov4 = "Maps/mov4.txt"

# Amplada i alçada de la pantalla             


pantallaLinux=1214, 970
pantallaProjector=1024, 768
pantallaIdeal=1000, 720

mides_pantalla = pantallaIdeal

#Nombre de caselles en el mapa
                 
ampladaMapa = 20
alçadaMapa = 11

#Mida Caselles
                    
midaCas = 50

#Marge d'error al calcular si un sprite està centrat
margeError = 5

#Tamany lletra
Ubuntu=1
Windows=0.6
coefLletra=Windows

#-------------------------------------------------------------------------#
#---------------------# BALANÇ DEL JOC #----------------------------------#
#-------------------------------------------------------------------------#

#General

interval_inicial=2000
interval_minim=1200
initial_cash=1000
vidaBase = 10000
robotDamage = 2000

#Limits

DMGMultLimits={
    "machineGun":3,
    "cannon":3,
    "radar":9999,       #El seu DMG es 0
    "generator":9999,
    }
REACHMultLimits={
    "machineGun":3,
    "cannon":2.3,
    "radar":2.5,
    "generator":2,
    }

#Turrets

#MACHINE GUN
DMG_machineGun=200
firerate_machineGun=250
reach_machineGun=150
coins_machineGun=200+50

#CANNON
DMG_cannon=350
firerate_cannon=1500
reach_cannon=230
coins_cannon=100+50

#GENERATOR
DMG_generator=0
firerate_generator=0
reach_generator=120
coins_generator=450
DMG_boost_generator=1.5

#RADAR
DMG_radar=0
firerate_radar=0
reach_radar=75
coins_radar=125+75
reach_boost_radar=1.35

#Robots

    #Robots senzills


speed_robot1=3
coins_robot1=30         #1 robot base   
health_robot1=1000

speed_robot2=5
coins_robot2=50         #2 robot rapid
health_robot2=1000

speed_robot3=3
coins_robot3=60         #3 robot resistent
health_robot3=3000

speed_robot4=4
coins_robot4=90        #4 robot complet
health_robot4=7500

speed_robot5=2
coins_robot5=100       #5 robot lent i resistent
health_robot5=20000

     #Robots dopats     

speed_robot6=4
coins_robot6=110        #6 robot base OP    
health_robot6=18000

speed_robot7=7
coins_robot7=150        #7 robot rapid OP       
health_robot7=15000

speed_robot8=1
coins_robot8=150        #8 robot resistent OP      
health_robot8=70000

speed_robot9=5
coins_robot9=200        #9 robot complet OP        
health_robot9=40000

speed_robot10=2
coins_robot10=200       #10 robot lent i resistent OP        
health_robot10=150000

   #Robot rei

speed_robot11=1
coins_robot11=0
health_robot11=400000

r1="r1"
r2="r2"
r3="r3"
r4="r4"
r5="r5"
r6="r6"
r7="r7"
r8="r8"
r9="r9"
r10="r10"
r11="r11"

enemics1=[[r1, r1],
          [r1, r2, r1],
          [r1, r3, r1],
          [r3, r1, r2, r1],
          [r3, r3, r1, r1, r2, r2],         #5
          [r2, r2, r2, r2, r3, r3, r3, r3],
          [r2, r3, r4, r2, r3, r4],
          [r1, r1, r5, r1, r1, r5],
          [r2, r3, r4, r5, r2, r3],
          [r6, r6, r4, r4, r1, r6],        #10
          [r4, r4, r3, r2, r3, r4, r4, r4],
          [r7, r4, r4, r7],
          [r4, r4, r6, r4, r4],
          [r5, r5, r4, r4, r6],
          [r6, r4, r6, r5, r4],         #15
          [r5, r5, r7, r3, r7],                 
          [r2, r3, r4, r5, r6, r8],
          [r9, r6, r6, r6, r6, r6, r7],
          [r6, r6, r6, r6, r6, r6, r6, r6, r6, r6],
          [r8,r8, r6, r6, r7,r7],   #20
          [r10,r10,r9,r9],
          [r11]]

enemics2=enemics1          

enemics3=[[r1, r1],
          [r1, r1, r2, r2],
          [r1, r2, r3, r2, r1],
          [r2, r2, r2, r2, r2, r2, r3],
          [r3, r2, r3, r2, r3, r2],         #5
          [r4, r3, r2, r3, r2],
          [r4, r2, r4, r2, r3],
          [r4, r4, r4, r2, r2, r4, r4, r4],
          [r5, r5, r4, r4],
          [r4, r4, r5, r5, r4, r4, r5, r4], #10
          [r6, r4, r3, r5, r3, r6, r4, r3],
          [r4, r6, r4, r6, r4, r6, r6],
          [r7, r4, r4, r3, r6],
          [r6, r7, r6, r4, r4],
          [r5, r5, r5, r5, r5, r5],         #15
          [r7, r4, r4, r7, r4, r4, r6],
          [r8, r4, r6, r4, r6],
          [r9, r9, r8, r6, r7],
          [r8, r7, r6, r5, r9],
          [r8, r9, r9, r8, r9, r9, r8, r9, r9],     #20
          [r10,r6, r6,r9, r6, r6,r10],
          [r11]]


enemics4=enemics3


#DICCIONARIS de preus
prices={
    "machineGun":coins_machineGun,
    "cannon":coins_cannon,
    "generator":coins_generator,
    "radar":coins_radar}

descripcio={
    "machineGun":"A double barrel machine gun turret.",
    "cannon":"A long range semi-automatic cannon.",
    "generator":"An electric generator that boosts adjacent turrets' damage.",
    "radar":"A long range dish that boosts adjacent turrets' reach."}

############ Noms dels SPRITES
# - Grass
sprite_grassQ = "Sprites/grassQ.png"

# - Path
sprite_pathV = "Sprites/pathV.png"
sprite_pathH = "Sprites/pathH.png"

sprite_pathI = "Sprites/pathI.png"
sprite_pathJ = "Sprites/pathJ.png"
sprite_pathK = "Sprites/pathK.png"
sprite_pathL = "Sprites/pathL.png"
sprite_pathZ = "Sprites/pathZ.png"

sprite_pathA = "Sprites/pathA.png"
sprite_pathS = "Sprites/pathS.png"
sprite_pathD= "Sprites/pathD.png"
sprite_pathF = "Sprites/pathF.png"

# - Objectes
sprite_rock1x2 = "Sprites/rock1x2.png"
sprite_rock2x2 = "Sprites/rock2x2.png"

sprite_tree1 = "Sprites/tree1.png"
sprite_forest1 = "Sprites/forest1.png"

sprite_plant1 = "Sprites/plant8.png"

sprite_explosion = "Sprites/explode.png"

# - Enemics
sprite_robot1 = "Sprites/robot1.png"
sprite_robot2 = "Sprites/robot2.png"
sprite_robot3 = "Sprites/robot3.png"
sprite_robot4 = "Sprites/robot4.png"
sprite_robot5 = "Sprites/robot5.png"
sprite_robot6 = "Sprites/robot6.png"
sprite_robot7 = "Sprites/robot7.png"
sprite_robot8 = "Sprites/robot8.png"
sprite_robot9 = "Sprites/robot9.png"
sprite_robot10 = "Sprites/robot10.png"
sprite_robot11 = "Sprites/robot11.png"

# - Torretes
machineGun_SpriteSheet = "Sprites/MachineGun_SpriteSheet.png"
cannon_SpriteSheet = "Sprites/Cannon_SpriteSheet.png"
generator_SpriteSheet = "Sprites/Generator_SpriteSheet.png"
radar_SpriteSheet = "Sprites/Radar_SpriteSheet.png"

# - Menus
sprite_mainMenu = "Sprites/mainMenu.png"
sprite_secondaryMenu = "Sprites/secondaryMenu.png"
sprite_menuLower = "Sprites/menu.png"
sprite_victoryLetters = "Sprites/youWin.png"
sprite_gameoverLetters = "Sprites/youLose.png"

sprite_background = "Sprites/background.png"
sprite_title = "Sprites/title.png"
sprite_drawer = "Sprites/drawer.png"

# - Botons
sprite_buttonPlay = "Sprites/buttonPlay.png"
sprite_buttonQuit = "Sprites/buttonQuit.png"

sprite_buttonMachineGun = "Sprites/buttonMachineGun.png"
sprite_buttonCannon = "Sprites/buttonCannon.png"
sprite_buttonGenerator = "Sprites/buttonGenerator.png"
sprite_buttonRadar = "Sprites/buttonRadar.png"
sprite_buttonDelete = "Sprites/buttonDelete.png"

sprite_buttonMap1="Sprites/buttonMap1.png"
sprite_buttonMap2="Sprites/buttonMap2.png"
sprite_buttonMap3="Sprites/buttonMap3.png"
sprite_buttonMap4="Sprites/buttonMap4.png"
sprite_buttonBack="Sprites/buttonBack.png"

sprite_buttonSurrender="Sprites/buttonSurrender.png"

sprite_buttonInf="Sprites/buttonInf.png"




