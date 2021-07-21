import pygame, sys, time, random

#initial game variables

# Window size
global frame_size_x,frame_size_y
frame_size_x = 720
frame_size_y = 480

#Parameters for Snake
global snake_pos,snake_body
snake_pos = [100, 50]
snake_body = [[100-(2*10), 50], [100-10, 50], [100, 50]]
global snake_length
snake_length = len(snake_body)
snakesurface=[]
global direction,x_change,y_change
x_change=10
y_change=0
direction = 'RIGHT'
change_to = direction

#Parameters for food
food_pos = [0,0]
global food_spawn,x_food,y_food
x_food = 200
y_food = 200
food_spawn = False
score = 0


# Initialise game window
pygame.init()
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))



# FPS (frames per second) controller to set the speed of the game
fps_controller = pygame.time.Clock()




def check_for_events():
    global direction,x_change,y_change
    """
    This should contain the main for loop (listening for events). You should close the program when
    someone closes the window, update the direction attribute after input from users. You will have to make sure
    snake cannot reverse the direction i.e. if it turned left it cannot move right next.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_UP:
                if direction == 'DOWN':
                    continue
                else:
                    direction = 'UP'
                    x_change = 0
                    y_change = -10
            if event.key == pygame.K_DOWN:
                if direction == 'UP':
                    continue
                else:
                    direction = 'DOWN'
                    x_change = 0
                    y_change = 10
            if event.key == pygame.K_LEFT:
                if direction == 'RIGHT':
                    continue
                else:
                    direction = 'LEFT'
                    x_change = -10
                    y_change = 0
            if event.key == pygame.K_RIGHT:
                if direction == 'LEFT':
                    continue
                else:
                    direction = 'RIGHT'
                    x_change = 10
                    y_change = 0













def update_snake():
    global x_change,y_change,x_food,y_food,snake_length,food_spawn,snake_pos,snake_body,frame_size_x,frame_size_y
    """
     This should contain the code for snake to move, grow, detect walls etc.
     """
    # Code for making the snake move in the expected direction
    snake_pos[0] += x_change
    snake_pos[1] += y_change
    snake_body.append([snake_pos[0],snake_pos[1]])
    if (snake_pos[0] == x_food) & (snake_pos[1] == y_food):
        snake_length +=1
        food_spawn = False
    if snake_length < len(snake_body) :
     #print(snake_length,snake_body)
     del snake_body[0]
    
    #pygame.draw.rect(game_window,(100,250,100),[snake_pos[0],snake_pos[1],10,10])
    #pygame.display.update()






    # Make the snake's body respond after the head moves. The responses will be different if it eats the food.
    # Note you cannot directly use the functions for detecting collisions 
    # since we have not made snake and food as a specific sprite or surface.
    




    if snake_pos[0] > frame_size_x-10 :
        time.sleep(0.5)
        game_over()
    if snake_pos[1] > frame_size_y-10 :
        time.sleep(0.5)
        game_over()
    if snake_pos[0] < 0 :
        time.sleep(0.5)
        game_over()
    if snake_pos[1] < 0 :  
        time.sleep(0.5)
        game_over()
    # End the game if the snake collides with the wall or with itself. 
    for k in range (0,len(snake_body)-1):
         if snake_body[k] == snake_pos :
             #print(snake_body[k],snake_pos,k)
             game_over()
         else:
             pass






def create_food():
    """ 
    This function should set coordinates of food if not there on the screen. You can use randrange() to generate
    the location of the food.
    """
    global x_food,y_food,food_spawn       
    if food_spawn == False :
        x_food = round(random.randrange(0,frame_size_x -10)/10)*10
        y_food = round(random.randrange(0,frame_size_y - 10)/10)*10
        food_spawn = True
    else:
        pass


def show_score(pos, color, font, size):
    """
    It takes in the above arguements and shows the score at the given pos according to the color, font and size.
    """
    pygame.font.init()
    myfont = pygame.font.SysFont(font,size)
    mesg= myfont.render("Your Score: "+str(len(snake_body)-3),True,color)
    game_window.blit(mesg,pos)






def update_screen():
    """
    Draw the snake, food, background, score on the screen
    """
    game_window.fill((10,10,0))
    global food_spawn,x_food,y_food,snake_length,snake_body
    for j in snake_body:
        pygame.draw.rect(game_window,(100,250,100),[j[0], j[1], 10, 10])
        #print(j)
    pygame.draw.rect(game_window,(150,50,150),[x_food, y_food,10,10])
    #print(x_food,y_food)
    #food_spawn = True
       # snake_length +=1
    
    show_score([0 , 0],(250,0,0),'Comic Sans MS',25)
    pygame.display.update()




def game_over():
    """ 
    Write the function to call in the end. 
    It should write game over on the screen, show your score, wait for 3 seconds and then exit
    """
    game_window.fill((10,10,0))
    myfont = pygame.font.SysFont('Comic Sans MS',100)
    end_mesg= myfont.render("GAME OVER ",True,(250,10,10))
    game_window.blit(end_mesg,[frame_size_x/9,frame_size_y/3])
    show_score([frame_size_x/4.5, 2*frame_size_y/3],(100,100,250),'Comic Sans MS',64)
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    sys.exit



# Main loop
while True:
    
    # Make appropriate calls to the above functions so that the game could finally run
    check_for_events()
    update_snake()
    create_food()
    update_screen()
    pygame.display.update()


    

    # To set the speed of the screen
    fps_controller.tick(15)