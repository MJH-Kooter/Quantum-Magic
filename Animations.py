import pygame as pg
from button import Button
import pygame_chart as pyc
import csv

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption("test")

####################Background#########################
scroll = 0
ground_image = pg.image.load("img/front.png").convert_alpha()
ground_width = ground_image.get_width()

bg_images = []
for i in range(1,4):
    bg_image = pg.image.load(f"img/layer{i}.png").convert_alpha()
    bg_images.append(bg_image)
bg_width = bg_images[0].get_width()


def draw_bg(screen):
    for x in range(4):
        speed = 1
        for i in bg_images:
            screen.blit(i, ((x * bg_width) - scroll * speed,0))
            speed += 0.2

def draw_ground(screen):
    for x in range(10):
        screen.blit(ground_image, ((x * ground_width) - scroll * 2.0, 0))

def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("img/font.ttf", size)

#############################SPRITE#########################

class SpriteSheet():
    def __init__(self,image,x_scale,y_scale,steps):
        self.sheet = pg.image.load(image).convert_alpha()
        self.sheet = pg.transform.scale(self.sheet,(x_scale,y_scale))
        self.frames = []
        self.steps = steps

    def load_steps(self,x_frame,y_frame):
        for frame in range(self.steps):
            self.frames.append(self.get_image(frame, x_frame,y_frame))

    def get_image(self, frame, width, height):
        image = pg.Surface((width,height)).convert_alpha()
        image.blit(self.sheet, (0,0), ((frame * width), 0, width, height))
        image.set_colorkey((0,0,0))
        return image

#INITIALIZE ANIMATIONS
##Character 1
IDLE = SpriteSheet('img/Wizard Pack/Idle.png',5544,760,6)
IDLE.load_steps(924,760)

STIR = SpriteSheet('img/Wizard Pack/Stir.png',5544,760,6)
STIR.load_steps(924,760)

WALK = SpriteSheet('img/Wizard Pack/Run.png',7392,760,8)
WALK.load_steps(924,760)

ATTACK = SpriteSheet('img/Wizard Pack/Attack1.png',7392,760,8)
ATTACK.load_steps(924,760)

JUMP = SpriteSheet('img/Wizard Pack/Jump.png',1848,760,2)
JUMP.load_steps(924,760)

DEATH = SpriteSheet('img/Wizard Pack/Death.png',6468,760,7)
DEATH.load_steps(924,760)

##Character 2
IDLE2 = SpriteSheet('img/Wizard Pack/Idle2.png',5544,760,6)
IDLE2.load_steps(924,760)

DEATH2 = SpriteSheet('img/Wizard Pack/Death2.png',6468,760,7)
DEATH2.load_steps(924,760)

##Misc
POTIONS = SpriteSheet('img/EntangledPotions.png',648,150,4)
POTIONS.load_steps(162,150)

TILTKETTLE = SpriteSheet('img/tilted_kettle.png',454,268,2)
TILTKETTLE.load_steps(227,268)

def print_skipline(screen):
    skip_txt = get_font(14).render("Press SPACE to skip", True, "White")
    skip_Rect = skip_txt.get_rect(topleft=(500,580))
    screen.blit(skip_txt, skip_Rect)

def run_intro(screen):
    #Variables
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame,frame2 = 0,0
    attack_done = False
    first, F2first = True, True

    global scroll

    run = True
    while run and last_update <= 30000:

        clock.tick(FPS)

        draw_bg(screen)
        draw_ground(screen)
        print_skipline(screen)

        current_time = pg.time.get_ticks()
        if current_time <= 6000:
            Intro_txt = Button(image= None, pos=(400, 150), 
                                    text_input="Welcome to Quantum Magic!", font=get_font(22), base_color="#d7fcd4", hovering_color="White")
            Intro_txt.update(screen)
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        elif current_time <= 18000:
            Follow_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                                    text_input="Follow me! \nWe have to stop \nNôdd-Onh the Detangler \nbefore it's too late!", 
                                    font=get_font(20), base_color="Black", hovering_color="White")
            Follow_txt.update(screen)
            if current_time - last_update >= animation_CD:
                frame += 1
                frame2 += 1
                last_update = current_time
                scroll += 10
                if frame >= len(WALK.frames):
                    frame = 0
                if frame2 >= len(IDLE2.frames):
                    frame2 = 0
            screen.blit(WALK.frames[frame], (-100,0))
            screen.blit(IDLE2.frames[frame2], (1100-scroll,0))
        elif attack_done == False:
            if first:
                frame = 0
                frame2 = 0
            first = False
            Spell_txt = Button(image= pg.image.load("img/Smalltextbox.png").convert_alpha(), pos=(600, 150), 
                                    text_input="RECIPII DEPHAZIO!", font=get_font(20), base_color="Red", hovering_color="White")
            Spell_txt.update(screen)
            if current_time - last_update >= animation_CD:
                frame += 1
                frame2 += 1
                last_update = current_time
                if frame >= len(ATTACK.frames):
                    frame = 0
                    attack_done = True
                if frame2 >= len(IDLE2.frames):
                    frame2 = 0
            if attack_done == False:
                screen.blit(ATTACK.frames[frame], (-100,0))
                screen.blit(IDLE2.frames[frame2], (1100-scroll,0))
        else:
            if F2first:
                frame2 = 0
            F2first = False
            Help_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                                    text_input="Oh no, \nNôdd-Onh destroyed my \nrecipes! Will you help \nrediscover them all?", 
                                    font=get_font(20), base_color="Black", hovering_color="White")
            Help_txt.update(screen)
            if current_time - last_update >= animation_CD:
                frame += 1
                if frame2 < len(DEATH2.frames)-1:
                    frame2 += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
            screen.blit(DEATH2.frames[frame2], (1100-scroll,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()

def level1_intro(screen):
    #Variables
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame = 0
    run = True
    
    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 24000:
            run = False
        screen.blit(pg.image.load("img/tab_bg.png").convert_alpha(), (0,0))
        print_skipline(screen)
        screen.blit(pg.image.load("img/BrokenClock.png").convert_alpha(), (400,450))
        screen.blit(pg.image.load("img/Lvl1Intro.png").convert_alpha(), (250,50))

        if current_time - last_update >= animation_CD:
            frame += 1
            last_update = current_time
            if frame >= len(IDLE.frames):
                frame = 0
        screen.blit(IDLE.frames[frame], (-200,0))


        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()  

def level2_intro(screen):
    #Variables
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    tilt, frame = 0,0
    run = True
    
    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 24000:
            run = False
        screen.blit(pg.image.load("img/tab_bg.png").convert_alpha(), (0,0))
        print_skipline(screen)

        screen.blit(pg.image.load("img/Lvl2Intro.png").convert_alpha(), (250,20))
        if current_time - last_update >= animation_CD:
            frame += 1
            last_update = current_time
            if frame >= len(IDLE.frames):
                frame = 0
        screen.blit(IDLE.frames[frame], (-200,0))


        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()  

def level3_intro(screen):                      
    #Variables
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame = 0
    run = True
    
    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 24000:
            run = False
        screen.blit(pg.image.load("img/tab_bg.png").convert_alpha(), (0,0))
        screen.blit(pg.image.load("img/Entangled.png").convert_alpha(), (0,0))
        print_skipline(screen)
        screen.blit(pg.image.load("img/Lvl3Intro.png").convert_alpha(), (250,20))
    
        if current_time - last_update >= animation_CD:
            frame += 1
            last_update = current_time
            if frame >= len(IDLE.frames):
                frame = 0
        screen.blit(IDLE.frames[frame], (-200,0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()  

def level4_intro(screen):                      
    #Variables
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame = 0
    run = True
    
    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 24000:
            run = False
        screen.blit(pg.image.load("img/tab_bg.png").convert_alpha(), (0,0))
        print_skipline(screen)
        screen.blit(pg.image.load("img/Lvl4Intro.png").convert_alpha(), (250,20))

        if current_time - last_update >= animation_CD:
            frame += 1
            last_update = current_time
            if frame >= len(IDLE.frames):
                frame = 0
        screen.blit(IDLE.frames[frame], (-200,0))


        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()

def level1_result(screen,score):
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame,frame2 = 0, len(ATTACK.frames)-1
    jump_done, move_done = False, False
    first = True
    run = True

    waittime,prob = 0,0
    with open("Levels/lvl1data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            waittime = float(row["X"])
            prob = round(float(row["Y"]), 3)

    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 15000:
            run = False
        draw_bg(screen)
        draw_ground(screen)
        print_skipline(screen)        
        
        if current_time - start_time < 10000:
            Result_txt = Button(image=pg.image.load("img/WideTextbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"You waited for {waittime} μs. \nThe prob. of |1> was {prob}. \nYour score is: {score} !", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        elif move_done == False and score > 1000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nI have never been \nso half excited!!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            frame = 0
            if current_time - last_update >= animation_CD:
                frame2 -= 1
                last_update = current_time
                if frame2 == 0:
                    move_done = True
            screen.blit(ATTACK.frames[frame2], (-100,0))
        elif jump_done == False and score > 1000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nI have never been \nso half excited!!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(JUMP.frames):
                    frame = 0
            screen.blit(JUMP.frames[frame], (-100,0))
        elif score > 1000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nI have never been \nso half excited!!",
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        else: 
            if first:
                frame = 0
                first = False
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \n \nThat's not good enough.", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                if frame < len(DEATH.frames)-1:
                    frame += 1
                last_update = current_time
            screen.blit(DEATH.frames[frame], (-100,0))
        Result_txt.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()

def level2_result(screen,score):
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame,frame2 = 0,len(ATTACK.frames)-1
    jump_done, move_done = False, False
    first = True
    run = True

    with open("Levels/lvl2data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            waittime = float(row["X"])
            prob = round(float(row["Y"]), 3)
    
    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 15000:
            run = False
        draw_bg(screen)
        draw_ground(screen)
        print_skipline(screen)
        if score <5000:
            screen.blit(pg.image.load("img/Spilled.png").convert_alpha(),(0,0))
          
        if current_time - start_time < 10000:
            Result_txt = Button(image=pg.image.load("img/WideTextbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"You waited for {waittime} μs. \nThe coherence was {prob}. \nYour score is: {score} !",
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        elif move_done == False and score >=5000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nThis position is \nindeed super!!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            frame = 0
            if current_time - last_update >= animation_CD:
                frame2 -= 1
                last_update = current_time
                if frame2 == 0:
                    move_done = True
            screen.blit(ATTACK.frames[frame2], (-100,0))
        elif jump_done == False and score >= 5000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nThis position is \nindeed super!!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(JUMP.frames):
                    frame = 0
            screen.blit(JUMP.frames[frame], (-100,0))
        elif score >= 5000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nThis position is \nindeed super!!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        else: 
            if first:
                frame = 0
                first = False
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Oh noo, the kettle \ntripped... What a mess! \n Your score was {score}! \n", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                if frame < len(DEATH.frames)-1:
                    frame += 1
                last_update = current_time
            screen.blit(DEATH.frames[frame], (-100,0))
        Result_txt.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()

def level3_result(screen,score):
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    potfr,frame,frame2 = 0,0,0
    jump_done, move_done = False, False
    first = True
    run = True
    
    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 15000:
            run = False
        draw_bg(screen)
        draw_ground(screen)
        print_skipline(screen)
        if score <5000:
            screen.blit(pg.image.load("img/MixedFlower.png").convert_alpha(),(0,0))
        else:
            screen.blit(pg.image.load("img/BlueFlower.png").convert_alpha(),(0,0))
            if current_time - last_update >= animation_CD:
                potfr += 1
                if potfr >= len(POTIONS.frames):
                    potfr = 0
            screen.blit(POTIONS.frames[potfr], (500,250))
          
        if current_time - start_time < 3000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        elif move_done == False and score >= 5000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nI love these flowers! \nThey are entangled \njust the right way!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            frame = 0
            if current_time - last_update >= animation_CD:
                frame2 += 1
                last_update = current_time
                if frame2 >= len(ATTACK.frames)-1:
                    move_done = True
            screen.blit(ATTACK.frames[frame2], (-100,0))
        elif jump_done == False and score >= 5000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nI love these flowers! \nThey are entangled \njust the right way!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(JUMP.frames):
                    frame = 0
            screen.blit(JUMP.frames[frame], (-100,0))
        elif score >= 5000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nI love these flowers! \nThey are entangled \njust the right way!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        else: 
            if first:
                frame = 0
                first = False
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \nThose are not uniform.. \nMaybe you try again?", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                if frame < len(DEATH.frames)-1:
                    frame += 1
                last_update = current_time
            screen.blit(DEATH.frames[frame], (-100,0))
        Result_txt.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()

def level4_result(screen,score):
    clock = pg.time.Clock()
    last_update = pg.time.get_ticks()
    start_time = pg.time.get_ticks()
    animation_CD = 120
    FPS = 60
    frame,frame2 = 0, len(ATTACK.frames)-1
    jump_done, move_done = False, False
    first = True
    run = True

    while run:
        current_time = pg.time.get_ticks()
        clock.tick(FPS)
        if current_time - start_time >= 15000:
            run = False
        draw_bg(screen)
        draw_ground(screen)
        print_skipline(screen)        
        
        if current_time - start_time < 10000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your score is: {score} !", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        elif move_done == False and score > 1000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \n I talk to Merlin \nevery day now!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            frame = 0
            if current_time - last_update >= animation_CD:
                frame2 -= 1
                last_update = current_time
                if frame2 == 0:
                    move_done = True
            screen.blit(ATTACK.frames[frame2], (-100,0))
        elif jump_done == False and score > 1000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \n I talk to Merlin \nevery day now!", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(JUMP.frames):
                    frame = 0
            screen.blit(JUMP.frames[frame], (-100,0))
        elif score > 1000:
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \n I talk to Merlin \nevery day now!",
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                frame += 1
                last_update = current_time
                if frame >= len(IDLE.frames):
                    frame = 0
            screen.blit(IDLE.frames[frame], (-100,0))
        else: 
            if first:
                frame = 0
                first = False
            Result_txt = Button(image=pg.image.load("img/Textbox.png").convert_alpha(), pos=(300, 130), 
                        text_input=f"Your result was {score}! \n \nThat's not good enough.", 
                        font=get_font(20), base_color="Black", hovering_color="White")
            if current_time - last_update >= animation_CD:
                if frame < len(DEATH.frames)-1:
                    frame += 1
                last_update = current_time
            screen.blit(DEATH.frames[frame], (-100,0))
        Result_txt.update(screen)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                run = False

        pg.display.update()

pg.quit()