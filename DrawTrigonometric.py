from typing import Set
import pygame
import math
import time

from pygame import Rect, key
from pygame import draw
from pygame.constants import SCRAP_SELECTION, SHOWN

pygame.font.init()
from pygame import gfxdraw


#==( Display Values )================================
WIDTH, HEIGHT = 900,500
# WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK, RED, WHITE, DARK_GRAY = (0, 0, 0), (255, 0, 0), (255, 255, 255), (150, 150, 150)
FONT = pygame.font.SysFont('comicsans', 20)
CURRENT_SECTION = 'MENU'
MENU_SECTION = 'MENU'


#==( Menu UI Values )================================
FPS_REFRESH_RATE = 1 #s

CENTER_WIDTH, CENTER_HEIGHT =  WIDTH//2, HEIGHT//2
MENU_WIDTH, MENU_HEIGHT = 500, 400

GRAY ,YELLOW = (209, 209, 209), (255, 255, 0)

#Corner circle
CORNER_CIRCLE_COLOR = (180, 180, 180)
MENU_CORNER_RADIUS = 11
MENU_TITLE_FONT = pygame.font.SysFont('comicsans', 35)
MENU_TITLE_SELECT_FONT = pygame.font.SysFont('comicsans', 45)
MENU_OPTION_FONT = pygame.font.SysFont('comicsans', 25)
TOP_HEIGHT = CENTER_HEIGHT - MENU_HEIGHT//2 + 30 

OPTIONS_FONT = pygame.font.SysFont('comicsans', 25)
INFO_FONT = pygame.font.SysFont('comicsans', 25)


#==( Control Values )================================
VEL, VEL_MUL = 125, 10

#==( User Settings )=================================
SETTING_COLOR = (0, 200, 255)
showXaxis = False
renderFPS = 60
lineThickness = 1
showDrawPoints = False

FPS_SELECTIONS = [30, 60, 90, 144, math.inf]
THICKNESS_SELECTIONS = [1, 2, 3, 4, 5]




#setting up an user event for the renender to know if the metric changes
# (+num) is equal to the ID of the event so every one needs to be different  
Value_update = pygame.USEREVENT + 1 
QUIT_CALL = pygame.USEREVENT + 2


class UserSettings():
    #Change users setting 

    def __init__(self, showXaxis, renderFPS, lineThickness, showDrawPoints) -> None:
        self.showXaxis = showXaxis
        self.lineThickness = lineThickness
        self.renderFPS = renderFPS
        self.showDrawPoints = showDrawPoints
        self.Current_FPS = 1
        self.Current_Thickness = 1

    def changeXaxis(self):
        self.showXaxis = True if self.showXaxis == False else False

    def changePoints(self):
        self.showDrawPoints = True if self.showDrawPoints == False else False

    def changeFPS(self):
        if self.Current_FPS < len(FPS_SELECTIONS)-1 :
            self.Current_FPS += 1
            self.renderFPS = FPS_SELECTIONS[self.Current_FPS]
        else :
            self.Current_FPS = 0
            self.renderFPS = FPS_SELECTIONS[self.Current_FPS]

    def changeThickness(self):
        #loop through THICKNESS_SELECTIONS. Can be add more or less options in future
        if self.Current_Thickness < len(THICKNESS_SELECTIONS)-1 :
            self.Current_Thickness += 1
            self.lineThickness = THICKNESS_SELECTIONS[self.Current_Thickness]
        else:
            self.Current_Thickness = 0
            self.lineThickness = THICKNESS_SELECTIONS[self.Current_Thickness]


Settings = UserSettings(showXaxis, renderFPS, lineThickness, showDrawPoints)

class Coshape():

    def __init__(self, xstart, xend, xaxis, xunit, yunit):
        """
        ----------------------
        return the pointes of the cos height(y) and output it into an array of points
        ----------------------
        x: Specify the line of X axis
        r: Specify amplitude of the cos shape
        xaxis: Specify the x axis position in order for the cos to draw
        xunit: Specify the x axis for one unit (pixel for one pi)
        yunit: Specify the y axis for one unit (pixel height for y = 1)
        return : all the position of the shape
        """
        self.xstart = xstart
        self.xend = xend
        self.xaxis = xaxis 
        self.xunit = xunit
        self.yunit = yunit  


    def GetCords(self):#xstart: int, xend: int, xaxis: int, xunit: int, yunit: int
        result = []
        piAxis = []
        for x in range(self.xstart, self.xend+1, 1):
            #implement show y-axis if x == pi
            #print(math.floor(self.xunit))
            if x%math.floor(self.xunit) == 0:
                piAxis.append(x)

            #calculate width(x) into angle to feed in cos() and get the height(y)
            #算出弧度後乘以180° (π = 180°) 
            angle = (x/self.xunit)
            #get the height(y)
            y = math.cos(angle)*self.yunit
            #add it to the result list (x, y)
            result.append((x, self.xaxis-y))

        return result, piAxis


        

#inpurt handling, changing values
#inpurt FPS in order to get delta time for keeping the speed the same in different FPS 
def inputState(keys_pressed, metric, previous_time, now):
    global CURRENT_SECTION, MENU_SECTION

    #only calculate delta time if any key was pressed down to save resources
    if any(keys_pressed):

        #post event to tell updating the renender values
        pygame.event.post(pygame.event.Event(Value_update))     

        #delta time to keep movement at any frame speed would be the same 
        #inspired by:  https://youtu.be/XuyrHE6GIsc
        dt = now - previous_time
    else :
        return 

    #speed boost
    if keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_LSHIFT]:
       dt *= VEL_MUL

    if keys_pressed[pygame.K_ESCAPE]:
        CURRENT_SECTION = 'MENU'
        MENU_SECTION = 'MENU'

    if CURRENT_SECTION == 'Draw':
        SPEED = VEL * dt
        if keys_pressed[pygame.K_LEFT]:
            if metric.xunit - SPEED >= 1:
                metric.xunit -= SPEED
            else:
                metric.xuint = 1
        if keys_pressed[pygame.K_RIGHT]:
            metric.xunit += SPEED
        if keys_pressed[pygame.K_UP]:
            metric.yunit += SPEED
        if keys_pressed[pygame.K_DOWN]:
            if metric.yunit - SPEED >= 0:
                metric.yunit -= SPEED
            else:
                metric.yunit = 0



    
#function for drawing every thing int the windows : fps, shpaes etc.
def Draw_window(points, piAxis, FPS, section):

    #fill background with white to cover up previous renender
    SCREEN.fill(WHITE)

    if section == 'MENU':
        draw_menu()


    #draw.lines --> draw mutiple lines at same time
    #draw.line only draw one line
    elif section == 'Draw':

        if Settings.showXaxis == True:
            pygame.draw.line(SCREEN, DARK_GRAY,(0, HEIGHT//2), (WIDTH, HEIGHT//2))

        pygame.draw.lines(SCREEN, BLACK, False, points, Settings.lineThickness)
        #draw circle to display the points that where been calcualted
        if Settings.showDrawPoints == True:
            for x, y in points:
                pygame.gfxdraw.circle(SCREEN, int(x), int(y), 2, RED)
        if True :
            for x in piAxis:
                pygame.draw.line(SCREEN, BLACK, (x, 0), (x, HEIGHT))


    #display FPS at the top right
    FPS_text = FONT.render(f'FPS : {FPS}', 1, BLACK)
    SCREEN.blit(FPS_text, (WIDTH - FPS_text.get_width() -10, 10))



previous_click = False
#draw menu when startup
def draw_menu():
    global CURRENT_SECTION, MENU_SECTION, previous_click

    #rectangle backround of main menu
    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2, MENU_WIDTH, MENU_HEIGHT))
    pygame.draw.rect(SCREEN, GRAY, pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2, MENU_WIDTH, MENU_HEIGHT), width=5)

    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2), MENU_CORNER_RADIUS) #top_left
    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH + MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2), MENU_CORNER_RADIUS) #top_right
    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT + MENU_HEIGHT//2), MENU_CORNER_RADIUS) #botten_left 
    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH + MENU_WIDTH//2, CENTER_HEIGHT + MENU_HEIGHT//2), MENU_CORNER_RADIUS) #botten_right


    #menu Title and options

    if MENU_SECTION == 'MENU':
    #TITLE - MY PROJECT
        MENU_TITLE = MENU_TITLE_FONT.render("MY Project 110-1 20713", 1, WHITE)
        SCREEN.blit(MENU_TITLE, (CENTER_WIDTH - MENU_TITLE.get_width()//2, TOP_HEIGHT))
        #START
        MENU_START = MENU_OPTION_FONT.render('START', 1, WHITE)
        SCREEN.blit(MENU_START, (CENTER_WIDTH - MENU_START.get_width()//2, TOP_HEIGHT + 70))
        bt1 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT + 70, MENU_WIDTH, 35)
        #OPTION
        MENU_OPTIONS = MENU_OPTION_FONT.render('OPTIONS', 1, WHITE)
        SCREEN.blit(MENU_OPTIONS, (CENTER_WIDTH - MENU_OPTIONS.get_width()//2, TOP_HEIGHT + 120))
        bt2 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT + 120, MENU_WIDTH, 35)
        #IMFO
        MENU_INFO = MENU_OPTION_FONT.render('INFO', 1, WHITE)
        SCREEN.blit(MENU_INFO, (CENTER_WIDTH - MENU_INFO.get_width()//2, TOP_HEIGHT + 170))
        bt3 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT+ 170, MENU_WIDTH, 35)
        #QUIT
        MENU_QUIT = MENU_OPTION_FONT.render('QUIT', 1, WHITE)
        SCREEN.blit(MENU_QUIT, (CENTER_WIDTH - MENU_QUIT.get_width()//2, TOP_HEIGHT + 220))
        bt4 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT +220, MENU_WIDTH, 35)

        #options check boxes

        #detecting mouse will have collison with button hitbox
        MENU_BUTTON_HITBOX = [bt1, bt2, bt3, bt4]
        #get index to identify which botton it is (index, message)
        for i in enumerate(MENU_BUTTON_HITBOX):
            if i[1].collidepoint(pygame.mouse.get_pos()):
                SELECTED = MENU_TITLE_SELECT_FONT.render('*', 1, YELLOW)
                SCREEN.blit(SELECTED, (CENTER_WIDTH - i[1].width//2 + MENU_WIDTH//3, TOP_HEIGHT + 70 + 50*i[0]))

                # detect the button that was been pressed
                if pygame.mouse.get_pressed(3)[0] == True:
                    if i[0] == 0: 
                        CURRENT_SECTION = 'Draw'
                    elif i[0] == 1 :
                        MENU_SECTION = 'OPTIONS'
                    elif i[0] == 2 : 
                        MENU_SECTION = 'INFO'
                    elif i[0] == 3 :
                        #post QUIT Event to the main loop and it will QUIT
                        pygame.event.post(pygame.event.Event(QUIT_CALL))
        
    elif MENU_SECTION == 'OPTIONS':
        RIGHT_OPTION = CENTER_WIDTH- MENU_WIDTH//2 + 30
        LEFT_OPTION = CENTER_WIDTH + MENU_WIDTH//2 - 30
        
        #Title OPTION
        OPTION_TITLE = MENU_TITLE_FONT.render('OPTIONS', 1, WHITE)
        SCREEN.blit(OPTION_TITLE, (CENTER_WIDTH - OPTION_TITLE.get_width()//2, TOP_HEIGHT))
        #FPS OPTION
        SHOW_FPS = OPTIONS_FONT.render('Max Render FPS', 1, WHITE)
        SCREEN.blit(SHOW_FPS, (RIGHT_OPTION , TOP_HEIGHT + 70))
        #X-AXIS
        SHOW_XAXIS = OPTIONS_FONT.render('X-AXIS', 1, WHITE)
        SCREEN.blit(SHOW_XAXIS, (RIGHT_OPTION, TOP_HEIGHT + 140 ))
        #Draw points of the metric
        DRAW_POINTS = OPTIONS_FONT.render('Draw Points', 1, WHITE)
        SCREEN.blit(DRAW_POINTS, (RIGHT_OPTION, TOP_HEIGHT + 210 ))
        #Line Thickness
        LINE_THICKNESS = OPTIONS_FONT.render('Line Thickness', 1, WHITE)
        SCREEN.blit(LINE_THICKNESS, (RIGHT_OPTION, TOP_HEIGHT + 280 ))

        #BUTTONS
        CURRENT_FPS = OPTIONS_FONT.render(str(Settings.renderFPS), 1, SETTING_COLOR)
        SCREEN.blit(CURRENT_FPS, (LEFT_OPTION - CURRENT_FPS.get_width(), TOP_HEIGHT + 70))
        Bott_FPS = pygame.Rect( LEFT_OPTION - CURRENT_FPS.get_width()-5, TOP_HEIGHT + 70, CURRENT_FPS.get_width()+10, CURRENT_FPS.get_height())
        #Show AXIS button
        CURRENT_AXIS = OPTIONS_FONT.render(str(Settings.showXaxis), 1, SETTING_COLOR)
        SCREEN.blit(CURRENT_AXIS, (LEFT_OPTION - CURRENT_AXIS.get_width(), TOP_HEIGHT + 140))
        Bott_AXIS = pygame.Rect( LEFT_OPTION - CURRENT_AXIS.get_width()-5, TOP_HEIGHT + 140, CURRENT_AXIS.get_width()+10, CURRENT_AXIS.get_height())
        #Show Point Button
        CURRENT_POINT = OPTIONS_FONT.render(str(Settings.showDrawPoints), 1, SETTING_COLOR)
        SCREEN.blit(CURRENT_POINT, (LEFT_OPTION - CURRENT_POINT.get_width(), TOP_HEIGHT + 210))
        Bott_POINT = pygame.Rect( LEFT_OPTION - CURRENT_POINT.get_width()-5, TOP_HEIGHT + 210, CURRENT_POINT.get_width()+10, CURRENT_POINT.get_height())
        #Show THICKNESS Button
        CURRENT_THICK = OPTIONS_FONT.render(str(Settings.lineThickness), 1, SETTING_COLOR)
        SCREEN.blit(CURRENT_THICK, (LEFT_OPTION - CURRENT_THICK.get_width(), TOP_HEIGHT+ 280))
        Bott_THICK = pygame.Rect( LEFT_OPTION - CURRENT_THICK.get_width()-5, TOP_HEIGHT + 280, CURRENT_THICK.get_width()+10, CURRENT_THICK.get_height())

        #Button detection and call UserSettings for changing user setting
        Buttons = [Bott_FPS, Bott_AXIS, Bott_POINT, Bott_THICK]
        for i, b  in enumerate(Buttons):
            #Draw the hitbox of the button size
            pygame.draw.rect(SCREEN, GRAY, b, width=1)
            if b.collidepoint(pygame.mouse.get_pos()):
                #If mouse in hitbox highlight the hitbox with different color
                pygame.draw.rect(SCREEN, (200, 100, 0), b, width=3)

                #previos click to prevent changing multi times in one click
                if previous_click == True and pygame.mouse.get_pressed(3)[0] == False: previous_click = False
                if previous_click == False and pygame.mouse.get_pressed(3)[0] == True:
                        previous_click = True
                        if i == 0:
                            Settings.changeFPS()
                        elif i == 1:
                            Settings.changeXaxis()
                        elif i == 2:
                            Settings.changePoints()
                        elif i == 3:
                            Settings.changeThickness()



    elif MENU_SECTION == 'INFO':
        pass

        # hitbox for button
        # pygame.draw.rect(SCREEN, (255, 255 , 0), i[1], width=2)



def main():
    last_time , previous_time = time.time(), time.time()
    clock = pygame.time.Clock()
    fps = 0

    cos = Coshape(0, WIDTH, HEIGHT//2, 1, 1)
    cords, piAxis = cos.GetCords()

    pygame.event.post(pygame.event.Event(Value_update))

    run = True
    #game loop --> keeping screen from updating
    while run == True:

        #handling events such as Quit screen when user tap close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #detect only if the buuton is been press down but the previous frame isn't
            if event.type == Value_update:
                if CURRENT_SECTION == 'Draw':
                    #get list of coordinates for the shape
                    print(piAxis)
                    cords, piAxis = cos.GetCords()

            if event.type == QUIT_CALL :
                print('HELLO')
                pygame.quit()


        #keyinputs pass into inpurtState for changing the values for shapes
        keys_pressed = pygame.key.get_pressed()
        inputState(keys_pressed, cos, previous_time , time.time())
        previous_time = time.time()

        #counting the FPS and limit FPS
        clock.tick(Settings.renderFPS)
        #display the FPS every second
        if time.time() - last_time > FPS_REFRESH_RATE :
            fps = round(clock.get_fps(), 1)
            last_time = time.time()

        #pass all value that needs to be drawn
        Draw_window(cords, piAxis, fps, CURRENT_SECTION)

        #update the display every drawing needs to be done above update
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":  
    main()