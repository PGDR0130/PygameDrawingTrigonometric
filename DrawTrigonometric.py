import pygame
import math
import time

pygame.font.init()
from pygame import gfxdraw



WIDTH, HEIGHT = 900,500
# WIDTH, HEIGHT = 1920,1080
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK, RED = (0, 0, 0), (255, 0, 0)

FPS_FONT = pygame.font.SysFont('comicsans', 20)

Value_update = pygame.USEREVENT + 1 



class Coshape():

    def __init__(self, xstart, xend, xaxis, xunit, yunit):
        self.xstart = xstart
        self.xend = xend
        self.xaxis = xaxis 
        self.xunit = xunit
        self.yunit = yunit  

    def cosGetCords(self):#xstart: int, xend: int, xaxis: int, xunit: int, yunit: int
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
def inputState(keys_pressed, shape):
    change = False
    if keys_pressed[pygame.K_LEFT] and shape.xunit != 1:
        shape.xunit -= 1
        change = True
    if keys_pressed[pygame.K_RIGHT]:
        shape.xunit += 1
        change = True
    if keys_pressed[pygame.K_UP]:
        shape.yunit += 1
        change = True
    if keys_pressed[pygame.K_DOWN] and shape.yunit != 0:
        shape.yunit -= 1
        change = True

    #new event for updating the cords when values changed
    # + 1 --> ID every event needs to add different number
    if change == True:
        pygame.event.post(pygame.event.Event(Value_update))


    
#function for drawing every thing int the windows : fps, shpaes etc.
def Draw_window(points, FPS):

    #fill background with all white
    SCREEN.fill((255, 255, 255))

    #draw.lines --> draw mutiple lines at same time
    #draw.line only draw one line
    pygame.draw.lines(SCREEN, BLACK, False, points, 1)

    #draw circle to display the points that where been calcualted
    for i in points:
        pygame.gfxdraw.circle(SCREEN, int(i[0]), int(i[1]), 2, RED)

    #display FPS
    FPS_text = FPS_FONT.render(f'FPS : {FPS}', 1, BLACK)
    SCREEN.blit(FPS_text, (WIDTH - FPS_text.get_width() -10, 10))



    



def main():
    last_time = time.time()
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
            if event.type == Value_update:
                #get list of coordinates for the shape
                cords = cos.cosGetCords()


        #keyinputs pass into inpurtState for changing the values for shapes
        keys_pressed = pygame.key.get_pressed()
        inputState(keys_pressed, cos)


        # #draw out coordinates that been passed in
        # cords = cos.cosGetCords() 


        #for counting the FPS
        clock.tick()
        #display the FPS every sencond
        if time.time() - last_time > 1 :
            fps = round(clock.get_fps(), 1)
            last_time = time.time()

        #pass all value that needs to be drawn
        Draw_window(cords, fps)

        #update the display every drawing needs to be done above update()
        pygame.display.update()
    
    pygame.quit()

main()