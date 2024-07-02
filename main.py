import pygame as pg
import importlib
import threading
import math
import csv
import pygame_chart as pyc

from button import Button
from objects import Object, SpriteSheet
import constants as c
import backend as BE
import Animations as A

pg.init()

#Initialize Game Window
screen = pg.display.set_mode((c.SCREEN_WIDTH,c.SCREEN_HEIGTH))
pg.display.set_caption('Quantum Magic')

#Backend Variables
clock = pg.time.Clock()
run = True
L = None
selectedLVL = 0
result_thread = None
help_on = False

#Backend lists
obj_list = []
rect_list = []
levels = []
highscores = []

#Load Images
bg = pg.image.load('img/bg.png').convert_alpha()
table = pg.image.load('img/table.png').convert_alpha()
scoreboard = pg.image.load('img/scoreboard.png').convert_alpha()
tab_bg = pg.image.load('img/tab_bg.png').convert_alpha()
kettle_sheet_img = pg.image.load('img/kettle.png').convert_alpha()
pickarea = pg.image.load('img/pickarea.png').convert_alpha()
trash = pg.image.load('img/trash.png').convert_alpha()
almanac = pg.image.load('img/almanac.png').convert_alpha()
almbg = pg.image.load('img/almbg.png').convert_alpha()
graph = pg.image.load('img/Graph.png').convert_alpha()

#Sprites
sprites = pg.sprite.Sprite
kettle_sheet = SpriteSheet(kettle_sheet_img)

#Load assets related to current level
def CallCurrentLvl(level):
    global L
    module_i = f"Levels.lvl{level}"
    module = importlib.import_module(module_i)
    L = module

#Initialize level and highscore statistics
def LoadLevels():
    with open("Leveldata.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            levels.append(int(row["level"]))
            highscores.append(int(row["highscore"]))
    return

#Return the highest score for the given level
def GetHighscore(level):
    for lvl, score in zip(levels, highscores):
        if lvl == level:
            return score
    return 0

#Return the highest level where a score is set
def GetHighestLvl():
    highest = 0
    for level in levels:
        if GetHighscore(level) > 0:
            highest = level
        else:
            break
    return highest

#Initialize game by selecting the highest reached level
def SetStartLvl():
    global selectedLVL
    selectedLVL = GetHighestLvl()+1

#Check if given score for given level is higher than
#existing highscore, and if so, replace it
def UpdateHighscore(level, new_highscore):
    global selectedLVL
    updated = False
    for i, lvl in enumerate(levels):
        if lvl == level:
            if highscores[i] < new_highscore:
                highscores[i] = new_highscore
                updated = True
            break
    
    if updated:
        with open("Leveldata.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(["level", "highscore"])  # Write header row
            for lvl, score in zip(levels, highscores):
                writer.writerow([lvl, score])
    LoadLevels()
    selectedLVL = GetHighestLvl()+1
    CallCurrentLvl(selectedLVL)

#Initialize the font for text
def get_font(size): # Returns Press-Start-2P in the desired size
    return pg.font.Font("img/font.ttf", size)

#Display Level Information
def lvlstats(text, font, text_col, x ,y):
    screen.blit(scoreboard, (x,y))    
    for i in text:
        img = font.render(i, True, text_col)
        screen.blit(img, (x+10,y+5))
        y = y+30

#Prepare the text to put on the Level information board
def prepare_txt():
    lvl = selectedLVL
    line = [f"Level: {lvl}", f"Highscore: {GetHighscore(lvl)}", f"Goal: {L.goal}"]
    return line

#Create ingredient objects based on input variables
def create_obj(img,id,txt,x,y):
    if "," in txt:
        split = txt.split(",")
        curr_obj = Object(img,id,split[0],split[1])
    else:
        curr_obj = Object(img,id,txt,"")
    curr_rect = curr_obj.img.get_rect()
    curr_rect.center = (x,y)
    rect_list.append(curr_rect)
    obj_list.append(curr_obj)

#Sub-function for threading. Calls backend for selected level
def call_api():
    BE.run(selectedLVL, L.lines_list)

#Starts an extra thread to calculate results
def prepare_result():
    global result_thread
    result_thread = threading.Thread(target=call_api)
    result_thread.daemon = True
    result_thread.start()

#Loop for the menu when opening the game
def main_menu():
    global selectedLVL
    global run
    global L
    global result_thread
    global help_on
    Lines = list()
    Objs = list()
    

    #Animation variables
    last_update = pg.time.get_ticks()
    animation_list = []
    animation_steps = 2
    animation_cd = 100
    frame,frame2 = 0,0
    update = pg.time.get_ticks()

    #Level variables
    Levelselect = False
    LoadLevels()
 
    #Start the game on the highest available level
    if selectedLVL == 0:
        SetStartLvl()
    CallCurrentLvl(selectedLVL)

    #Load the steps for animation
    for a in range(animation_steps):
        animation_list.append(kettle_sheet.get_image(a, 227, 268))

    #prepare buttons for the levelselect page
    lvlbuttons = [Button(image=pg.image.load("img/Play Rect.png"), pos=(c.SCREEN_WIDTH/2, 500), 
                    text_input="BACK", font=get_font(35), base_color="#d7fcd4", hovering_color="White")]
    for index in range(0,GetHighestLvl()+1):
        lvlbuttons.append(Button(image=pg.image.load("img/Lvl Rect.png"), pos=(250, (150+index*70)), 
                    text_input=f"Level {index+1}", font=get_font(16), base_color="#d7fcd4", hovering_color="White"))
    buttoncoords = [(150,250),(220,250),(290,250),(360,250),(430,250),(150,550),(220,550),(290,550),(360,550),(430,550)]

    while run:

        clock.tick(c.FPS)       
        screen.blit(bg,(0,0))

        #update animation
        if not result_thread:
            current_time = pg.time.get_ticks()
            if current_time - update >= animation_cd:
                frame +=1
                update = current_time
                if frame >= len(animation_list):
                    frame = 0
            screen.blit(animation_list[frame],(269,299))

        Mouse_Pos = pg.mouse.get_pos()

        #When levelselect = true, the levelselectpage is shown instead of the main menu
        #Everything related to a different level should be cleared
        if Levelselect:
            rect_list.clear()
            obj_list.clear()
            CallCurrentLvl(selectedLVL)
            
            #Draw the level buttons
            for i,coord in enumerate(buttoncoords):
                y = coord[0]
                x = coord[1]
                pg.draw.rect(screen, "dimgrey", pg.Rect(x-67,y-13,135,27))
                rect_txt = get_font(16).render(f"Level {i+1}",True,"Black")
                rect_rect = rect_txt.get_rect(center=(x,y))
                screen.blit(rect_txt,rect_rect)
            
            #Draw the menutext for the levelselect page
            selected_txt = get_font(30).render(f"Selected Level: {selectedLVL}", True, "Darkred")
            select_rect = selected_txt.get_rect(center = (400,70))
            screen.blit(selected_txt,select_rect)
            
            #Highlight buttons when hovered over.
            for button in lvlbuttons:
                button.changeColor(Mouse_Pos)
                button.update(screen)

            #Check for events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN:
                    if lvlbuttons[0].checkForInput(Mouse_Pos):
                        Levelselect = False
                    else:
                        for index,button in enumerate(lvlbuttons):
                            if index != 0:
                                if button.checkForInput(Mouse_Pos):
                                    selectedLVL = index
        
        #if the levelselect menu is not open, display the main menu
        else:
            #display everything when no result is being generated
            if not result_thread:

                #Display menu text and level statistics
                Menu_txt = get_font(40).render("MAIN MENU", True, "White")
                Menu_Rect = Menu_txt.get_rect(center=(c.SCREEN_WIDTH/2, 180))
                screen.blit(Menu_txt, Menu_Rect)
                lvlstats(prepare_txt(), get_font(20), "#c28d14", 225,20)

                #initialize the buttons for the level.
                #Levels button calls the levelselect menu
                #HELP button toggles the help menu
                #Quit button ends the game
                #Table button redirects to the potion preparation page
                #Kettle button starts a thread and sends the result to the backend
                LEVELS_BUTTON = Button(image=pg.image.load("img/Big Rect.png"), pos=(107, 20), 
                                    text_input="Select Level", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
                if help_on:
                    HELP_BUTTON = Button(image=pg.image.load("img/Big Rect.png"), pos=(107, 50), 
                                        text_input="HELP = ON", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
                else:
                    HELP_BUTTON = Button(image=pg.image.load("img/Big Rect.png"), pos=(107, 50), 
                                        text_input="HELP = OFF", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
                QUIT_BUTTON = Button(image=pg.image.load("img/Quit Rect.png"), pos=(52, 80), 
                                    text_input="QUIT", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
                TABLE_BUTTON = Button(image=pg.image.load("img/table.png"), pos=(675,465),
                                    text_input="Prepare the Recipe", font=get_font(10), base_color="#d7fcd4" ,hovering_color='White')
                KETTLE_BUTTON = Button(image=pg.image.load("img/kettlebutton.png").convert_alpha(), pos=(388,463),
                                    text_input="Start brewing", font=get_font(10), base_color="#d7fcd4" ,hovering_color='White')

                #update buttons when hovered over
                for button in [LEVELS_BUTTON, HELP_BUTTON, QUIT_BUTTON, TABLE_BUTTON, KETTLE_BUTTON]:
                    button.changeColor(Mouse_Pos)
                    button.update(screen)
                
                #when help is toggled, display information on the game
                if help_on:
                    screen.blit(pg.image.load("img/HelpMainMenu.png").convert_alpha(),(0,0))
            
            #If a result is being calculated, the player has to wait, so no buttons are shown
            if result_thread:
                if result_thread.is_alive():
                    #timer for the animation
                    current_time = pg.time.get_ticks()

                    #Visual elements initialized
                    table = Button(image=pg.image.load("img/table.png"), pos=(675,465),
                                    text_input="", font=get_font(10), base_color="#d7fcd4" ,hovering_color='White')
                    Intro_txt = Button(image= None, pos=(400, 150), 
                                            text_input="Brewing ...", font=get_font(22), base_color="#d7fcd4", hovering_color="White")
                    Intro_txt.update(screen)
                    
                    #animation of the wizard
                    if current_time - last_update >= animation_cd:
                        frame2 += 1
                        last_update = current_time
                        if frame2 >= len(A.STIR.frames):
                            frame2 = 0
                    screen.blit(A.STIR.frames[frame2], (-150,0))
                    
                    #animation of the kettle
                    if current_time - update >= animation_cd:
                        frame +=1
                        update = current_time
                        if frame >= len(animation_list):
                            frame = 0
                    screen.blit(animation_list[frame],(269,299))
                    table.update(screen)

                #when calculations are done, update the score and end the extra thread
                else:
                    getattr(A, f"level{selectedLVL}_result")(screen,L.getScore())
                    UpdateHighscore(selectedLVL,L.getScore())
                    result_thread = None

            #check for events and handle them
            event_list = pg.event.get()
            for event in event_list:
                if event.type == pg.QUIT:
                    run = False
                if event.type == pg.MOUSEBUTTONDOWN and not result_thread:
                    if LEVELS_BUTTON.checkForInput(Mouse_Pos):
                        Levelselect = True
                    if HELP_BUTTON.checkForInput(Mouse_Pos):
                        if help_on:
                            help_on = False
                        elif not help_on:
                            help_on = True
                    if QUIT_BUTTON.checkForInput(Mouse_Pos):
                        run = False
                    if TABLE_BUTTON.checkForInput(Mouse_Pos):
                        getattr(A, f"level{selectedLVL}_intro")(screen)
                        tablepage()
                    if KETTLE_BUTTON.checkForInput(Mouse_Pos):
                        prepare_result()

        if run:
            pg.display.update()

#Loop for the potion preparation table environment
def tablepage():
    global L
    global help_on
    almanac_open,graph_open = False, False

    #Build the board if it doesn't exist yet
    if not L.lines_list:
        L.create_lines()
    else:
        for i,line in enumerate(L.lines_list):
            for obj in line.circuit:
                if obj.gate != "":
                    pass

    #initilize Potion buttons
    potionlist = []
    L.Num_Objects = len(L.potion_buttons)
    for index, potion in enumerate(L.potion_buttons):
        button = Button(image=pg.image.load(f"img/pots/potion{selectedLVL*10+index}.png").convert_alpha(), pos=(((c.PLAY_RIGHT-c.PLAY_LEFT)/L.Num_Objects+1)*(index+1), 550), 
        text_input=potion, font=get_font(12), base_color="#d7fcd4", hovering_color="White")
        potionlist.append(button)

    #initalize lines
    linelist = list()
    for line in L.lines_list:
        for i, segment in enumerate(line.circuit):
            linelist.append(pg.Rect(40+(c.Object_width*i),(140 + ((c.PLAY_BOT-c.PLAY_TOP)/(L.numberOfLines+1))*(line.line_id+1)), c.Object_width, 2))

    #initialize selected object
    selected = None
    obj_index = 0

    #Load graph
    if selectedLVL <=2:
        figure = pyc.Figure(screen, 100,100,600,400)
        X,Y = [],[]
        X,Y = L.loadpoints(X,Y)

    #Create Game Loop
    global run
    while run:
        clock.tick(c.FPS)
        Mouse_Pos = pg.mouse.get_pos()

        #if almanac_open is true, a different page will be shown with info on the current level and potions
        if almanac_open:
            screen.blit(almbg,(0,0))
            
            #Initialize and display a back button to leave the almanac page
            BACK_BUTTON = Button(image=pg.image.load("img/Quit Rect.png"), pos=(50, 20), 
                        text_input="BACK", font=get_font(15), base_color="#d7fcd4", hovering_color="White")

            BACK_BUTTON.changeColor(Mouse_Pos)
            BACK_BUTTON.update(screen)

            #Show level description
            Lvl_txt = get_font(18).render(L.getLvlDescription(), True, "Black")
            Lvl_Rect = Lvl_txt.get_rect(topleft=(30,c.PLAY_TOP ))
            screen.blit(Lvl_txt, Lvl_Rect) 
            
            #Show potion descriptions
            for index, potion in enumerate(L.potion_buttons):
                screen.blit(pg.image.load(f"img/pots/potion{selectedLVL*10+index}.png").convert_alpha(), (450,c.PLAY_TOP+index*75 ))
                Desc_txt = get_font(14).render(L.getPotDescription(index), True, "Black")
                Desc_Rect = Desc_txt.get_rect(topleft=(490,c.PLAY_TOP+15+index*75 ))
                screen.blit(Desc_txt, Desc_Rect)

            #check for events and handle them if necessary
            event_list = pg.event.get()
            for event in event_list:
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (event.button == 1):
                        if BACK_BUTTON.checkForInput(Mouse_Pos):
                            almanac_open = False
            if run:
                pg.display.update() 

        #When the graph menu is selected a graph with player performance on the level is shown        
        elif graph_open:
            #draw a scatter graph based on earlier results
            figure.scatter('progress',X,Y)
            figure.draw()

            #init and show the back button to leave the graph interface
            BACK_BUTTON = Button(image=pg.image.load("img/lvl Rect.png"), pos=(80, 20), 
                        text_input="Close Graph", font=get_font(14), base_color="#d7fcd4", hovering_color="White")

            BACK_BUTTON.changeColor(Mouse_Pos)
            BACK_BUTTON.update(screen)

            #check for events and handle them if necessary
            event_list = pg.event.get()
            for event in event_list:
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (event.button == 1):
                        if BACK_BUTTON.checkForInput(Mouse_Pos):
                            graph_open = False
                        
        #If no pages are open, display the recipe prepare table interface
        else:
            #display the background and level statistics
            screen.blit(tab_bg,(0,0))
            screen.blit(pickarea,(0,500))
            lvlstats(prepare_txt(), get_font(20), "#c28d14", 225,20)  
            
            #Initialize the buttons for this page
            #Back button to go back to the main menu
            #Alm button to open the almanac menu
            #Help button toggles the help mode
            # In the first two levels the graph button opens the graph page
            BACK_BUTTON = Button(image=pg.image.load("img/Quit Rect.png"), pos=(50, 20), 
                        text_input="BACK", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
            BACK_BUTTON.changeColor(Mouse_Pos)
            BACK_BUTTON.update(screen)

            ALM_BUTTON = Button(image=almanac, pos=(680, 80), 
                        text_input="", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
            ALM_BUTTON.changeColor(Mouse_Pos)
            ALM_BUTTON.update(screen)

            if help_on:
                HELP_BUTTON = Button(image=pg.image.load("img/Big Rect.png"), pos=(107, 50), 
                                text_input="HELP = ON", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
            else:
                HELP_BUTTON = Button(image=pg.image.load("img/Big Rect.png"), pos=(107, 50), 
                                text_input="HELP = OFF", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
            HELP_BUTTON.changeColor(Mouse_Pos)
            HELP_BUTTON.update(screen)

            if selectedLVL <= 2:
                GRAPH_BUTTON = Button(image=graph, pos=(680, 225), 
                            text_input="Progress", font=get_font(11), base_color="Black", hovering_color="Darkblue")
                GRAPH_BUTTON.changeColor(Mouse_Pos)
                GRAPH_BUTTON.update(screen)
           
            #Draw everything 
            screen.blit(trash,(40,80))
            #lines to prepare the recipe
            for segment in linelist:
                pg.draw.rect(screen, "white", segment)
            #potions
            for img,instance in zip(obj_list,rect_list):
                screen.blit(img.img,instance)                
            #Potion buttons
            for button in potionlist:
                button.changeColor(Mouse_Pos)
                button.update(screen)
            
            #The help menu changes based on number of lines, but all in all if help menu is on,
            #information on the current page and the level is shown
            if help_on:
                if selectedLVL == 1 or selectedLVL == 2:
                    screen.blit(pg.image.load("img/HelpTablePage.png").convert_alpha(), (0,0))
                elif selectedLVL == 3 or selectedLVL == 4:
                    screen.blit(pg.image.load("img/HelpTablePage34.png").convert_alpha(), (0,0))

            #check for events and handle them properly
            event_list = pg.event.get()
            for event in event_list:
                if event.type == pg.QUIT:
                    run = False
                    pg.quit()
                #Check if the player clicks anywhere
                if event.type == pg.MOUSEBUTTONDOWN:
                    if (event.button == 1):
                        if BACK_BUTTON.checkForInput(Mouse_Pos):
                            main_menu()
                        if ALM_BUTTON.checkForInput(Mouse_Pos):
                            almanac_open = True
                        if selectedLVL <=2:
                            if GRAPH_BUTTON.checkForInput(Mouse_Pos):
                                graph_open = True
                        if HELP_BUTTON.checkForInput(Mouse_Pos):
                            if help_on:
                                help_on = False
                            elif not help_on:
                                help_on = True
                        #When the player clicks on a potion button, that potion will be created
                        if any(buttons.checkForInput(Mouse_Pos) for buttons in potionlist):
                            for buttons in potionlist:
                                if buttons.checkForInput(Mouse_Pos):
                                    text = buttons.text_input
                                    #Some extra processing is necessary for wait objects, to fit them to the backend
                                    if "wait" in text:
                                        text = f"wait, {int(float(text.split(' ')[1])*50)}"
                                    create_obj(buttons.image,1,text,200,200)
                        else:
                            #check if the player clicks on any of the existing potions in the field
                            for index, rect1 in enumerate(rect_list):
                                if rect1.collidepoint(event.pos):
                                    selected = rect1
                                    obj_index = index
                                    for index, line in enumerate(linelist, start = 0):
                                        #if the player clicks on a potion that is already on a line, remove that potion from the line list
                                        if selected.colliderect(line):
                                            selectedobj = L.lines_list[math.floor(index/c.Length)].circuit[index % c.Length]
                                            #If a two element potion is removed, also remove the second element from the line list and the field
                                            if selectedobj.gate == "CZ" or selectedobj.gate == "CNOT" or selectedobj.gate == "SWAP":
                                                helper = selectedobj.data 
                                                for lindex, line in enumerate(L.lines_list):
                                                    if helper == lindex:
                                                        for indexi, objecti in enumerate(line.circuit):
                                                            
                                                            if objecti.gate.split("|")[0] == "ignore":
                                                                if int(objecti.gate.split("|")[1]) == L.lines_list[math.floor(index/c.Length)].line_id:
                                                                    for ind,obj in enumerate(obj_list):
                                                                        if obj.gate == objecti.gate:
                                                                            obj_list.pop(ind)
                                                                            rect_list.pop(ind)
                                                                            line.rem_obj(indexi)
                                                                            break
                                                                    break
                                            L.lines_list[math.floor(index/c.Length)].rem_obj(index % c.Length)

                #To determine where the player drops a potion, it is checked where the mousebutton is released
                if event.type == pg.MOUSEBUTTONUP and selected != None:
                    if event.button == 1:
                        #if a potion is released onto the trashcan, it should be deleted
                        if selected.colliderect(trash.get_rect()):
                            for index, rect in enumerate(rect_list):
                                if selected == rect:
                                    obj_list.pop(index)
                                    rect_list.pop(index)
                        #if a potion is dropped on a line segment, add it to line list and clamp it to that line segment            
                        for index, line in enumerate(linelist, start = 0):
                            if selected.colliderect(line):
                                curr = obj_list[obj_index]
                                #If the second part of a two element potion is released on the same line as the first part
                                #Do not add it to the list and ask the user to select a different line
                                if ("ignore" in curr.gate):
                                    if int(curr.gate.split("|")[1]) == math.floor(index/c.Length):
                                        print("Please attach to a different line")
                                    else:
                                        selected.clamp_ip(line)
                                        L.lines_list[math.floor(index/c.Length)].add_obj(index % c.Length, curr.img, curr.id, curr.gate,seconds)
                                        L.lines_list[int(curr.gate.split("|")[1])].data = L.lines_list[math.floor(index/c.Length)].line_id
                                else:
                                    selected.clamp_ip(line)
                                    #if a multi element gate is placed on a line, create the second part
                                    if (curr.gate == "CZ" or curr.gate == "CNOT" or curr.gate == "SWAP"):
                                        if curr.gate == "CZ":
                                            create_obj(pg.image.load("img/pots/CZ.png").convert_alpha(),2,f"ignore|{math.floor(index/c.Length)}",200,200)
                                        elif curr.gate == "CNOT":
                                            create_obj(pg.image.load("img/pots/CNOT.png").convert_alpha(),2,f"ignore|{math.floor(index/c.Length)}",200,200)
                                        else: 
                                            create_obj(curr.img,2,f"ignore|{math.floor(index/c.Length)}",200,200)
                                        firsts = L.lines_list[math.floor(index/c.Length)].line_id
                                        if firsts + 1 >= L.numberOfLines:
                                            if firsts - 1 < 0:
                                                pass
                                            else:
                                                seconds = firsts - 1
                                        else:
                                            seconds = firsts + 1
                                        L.lines_list[math.floor(index/c.Length)].add_obj(index % c.Length, curr.img, curr.id, curr.gate,seconds)
                                    else:  
                                        L.lines_list[math.floor(index/c.Length)].add_obj(index % c.Length, curr.img, curr.id, curr.gate, curr.data)
                            
                        selected = None
                #move the selected element based on mouse movement          
                if event.type == pg.MOUSEMOTION:
                    if selected != None:
                        selected.move_ip(event.rel)

        if run:
            pg.display.update()       

#start the program
A.run_intro(screen)
main_menu()

pg.quit()