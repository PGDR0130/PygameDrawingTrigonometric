import pygame
import math
import time

from pygame import key
from pygame import draw

pygame.font.init()
from pygame import gfxdraw


#== Display values ================================
# WIDTH, HEIGHT = 900,500
WIDTH, HEIGHT = 1920, 1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK, RED, WHITE = (0, 0, 0), (255, 0, 0), (255, 255, 255)
FONT = pygame.font.SysFont('comicsans', 20)
MAX_FPS = math.inf


#== Menu UI values ================================
FPS_REFRESH_RATE = 1 #s

CENTER_WIDTH, CENTER_HEIGHT =  WIDTH//2, HEIGHT//2
MENU_WIDTH, MENU_HEIGHT = 500, 400

GRAY ,YELLOW = (209, 209, 209), (255, 255, 0)

#Corner Circle in menu
CORNER_CIRCLE_COLOR = (180, 180, 180)
MENU_CORNER_RADIUS = 11
MENU_TITLE_FONT = pygame.font.SysFont('comicsans', 35)
MENU_TITLE_SELECT_FONT = pygame.font.SysFont('comicsans', 45)
MENU_OPTION_FONT = pygame.font.SysFont('comicsans', 25)
TOP_HEIGHT = CENTER_HEIGHT - MENU_HEIGHT//2 + 30 


#== Ingame values =================================
VEL, VEL_MUL = 125, 10




#==
#setting up an user event for the renender to know if the metric changes
# (+num) is equal to the ID of the event so every one needs to be different  
Value_update = pygame.USEREVENT + 1 



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


    def cosGetCords(self):#xstart: int, xend: int, xaxis: int, xunit: int, yunit: int

        result = []

        for x in range(self.xstart, self.xend+1, 1):
            #calculate width(x) into angle to feed in cos() and get the height(y)
            #算出弧度後乘以180° (π = 180°) 
            angle = ((x*(1/self.xunit))/math.pi)*180
            #get the height(y)
            y = math.cos(angle)*self.yunit
            #add it to the result list (x, y)
            result.append((x, self.xaxis-y))

        return result


        

#inpurt handling, changing values
#inpurt FPS in order to get delta time for keeping the speed the same in different FPS 
def inputState(keys_pressed, metric, previous_time, now):

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

    SPEED = VEL * dt
    if keys_pressed[pygame.K_LEFT] and metric.xunit - SPEED >= 1:
        metric.xunit -= SPEED
    if keys_pressed[pygame.K_RIGHT]:
        metric.xunit += SPEED
    if keys_pressed[pygame.K_UP]:
        metric.yunit += SPEED
    if keys_pressed[pygame.K_DOWN] and metric.yunit - SPEED >= 0:
        metric.yunit -= SPEED




    
#function for drawing every thing int the windows : fps, shpaes etc.
def Draw_window(points, FPS):

    #fill background with white to cover up previous renender
    SCREEN.fill(WHITE)

    #draw.lines --> draw mutiple lines at same time
    #draw.line only draw one line
    pygame.draw.lines(SCREEN, BLACK, False, points, 1)

    #draw circle to display the points that where been calcualted
    for i in points:
        pygame.gfxdraw.circle(SCREEN, int(i[0]), int(i[1]), 2, RED)

    #display FPS at the top right
    FPS_text = FONT.render(f'FPS : {FPS}', 1, BLACK)
    SCREEN.blit(FPS_text, (WIDTH - FPS_text.get_width() -10, 10))



#draw menu when startup
def draw_menu():
    #rectangle backround of main menu
    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2, MENU_WIDTH, MENU_HEIGHT))
    pygame.draw.rect(SCREEN, GRAY, pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2, MENU_WIDTH, MENU_HEIGHT), width=5)

    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2), MENU_CORNER_RADIUS) #top_left
    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH + MENU_WIDTH//2, CENTER_HEIGHT - MENU_HEIGHT//2), MENU_CORNER_RADIUS) #top_right
    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH - MENU_WIDTH//2, CENTER_HEIGHT + MENU_HEIGHT//2), MENU_CORNER_RADIUS) #botten_left 
    pygame.draw.circle(SCREEN, CORNER_CIRCLE_COLOR, (CENTER_WIDTH + MENU_WIDTH//2, CENTER_HEIGHT + MENU_HEIGHT//2), MENU_CORNER_RADIUS) #botten_right


    #menu Title and options

    #TITLE - MY PROJECT
    MENU_TITLE = MENU_TITLE_FONT.render("MY PROJECT", 1, WHITE)
    SCREEN.blit(MENU_TITLE, (CENTER_WIDTH - MENU_TITLE.get_width()//2, TOP_HEIGHT))
    #START
    MENU_START = MENU_OPTION_FONT.render('START', 1, WHITE)
    SCREEN.blit(MENU_START, (CENTER_WIDTH - MENU_START.get_width()//2, TOP_HEIGHT + 70))
    bt1 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT + 70, MENU_WIDTH, 35)
    #OPTION
    MENU_OPTIONS = MENU_OPTION_FONT.render('OPTIONS', 1, WHITE)
    SCREEN.blit(MENU_OPTIONS, (CENTER_WIDTH - MENU_OPTIONS.get_width()//2, TOP_HEIGHT + 120))
    bt2 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT + 120, MENU_WIDTH, 35)
    #CREDIT
    MENU_CREDIT = MENU_OPTION_FONT.render('CREDIT', 1, WHITE)
    SCREEN.blit(MENU_CREDIT, (CENTER_WIDTH - MENU_CREDIT.get_width()//2, TOP_HEIGHT + 170))
    bt3 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT+ 170, MENU_WIDTH, 35)

    MENU_QUIT = MENU_OPTION_FONT.render('QUIT', 1, WHITE)
    SCREEN.blit(MENU_QUIT, (CENTER_WIDTH - MENU_CREDIT.get_width()//2, TOP_HEIGHT + 220))
    bt4 = pygame.Rect(CENTER_WIDTH - MENU_WIDTH//2, TOP_HEIGHT +220, MENU_WIDTH, 35)

    #options check boxes

    #detecting mouse collion with the button hitbox
    MENU_BUTTON_HITBOX = [bt1, bt2, bt3, bt4]
    #get index to identify which botton it is 
    for i in enumerate(MENU_BUTTON_HITBOX):
        if i[1].collidepoint(pygame.mouse.get_pos()):
            SELECTED = MENU_TITLE_SELECT_FONT.render('*', 1, YELLOW)
            SCREEN.blit(SELECTED, (CENTER_WIDTH - i[1].width//2 + MENU_WIDTH//3, TOP_HEIGHT + 70 + 50*i[0]))
            

        # hitbox for button
        # pygame.draw.rect(SCREEN, (255, 255 , 0), i[1], width=2)

    


#Pop up pause menu when press ESC
def draw_pause():
    pass







def main():
    last_time , previous_time = time.time(), time.time()
    clock = pygame.time.Clock()
    fps = 0

    cos = Coshape(0, WIDTH, HEIGHT//2, 1, 1)

    pygame.event.post(pygame.event.Event(Value_update))

    run = True
    #game loop --> keeping surface from updating
    while run == True:

        #handling events such as Quit screen when user tap close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #detect only if the buuton is been press down but the previous frame isn't
            if event.type == Value_update:
                #get list of coordinates for the shape
                cords = cos.cosGetCords()


        #keyinputs pass into inpurtState for changing the values for shapes
        keys_pressed = pygame.key.get_pressed()
        inputState(keys_pressed, cos, previous_time , time.time())
        previous_time = time.time()

        #counting the FPS and limit FPS
        clock.tick(MAX_FPS)
        #display the FPS every sencond
        if time.time() - last_time > FPS_REFRESH_RATE :
            fps = round(clock.get_fps(), 1)
            last_time = time.time()

        #pass all value that needs to be drawn
        Draw_window(cords, fps)

        draw_menu()

        #update the display every drawing needs to be done above update
        pygame.display.update()
    
    pygame.quit()


if __name__ == "__main__":  
    main()