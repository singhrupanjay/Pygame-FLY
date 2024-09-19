import pygame
from sys import exit
from random import randint

# creating display surface
# set_mode must have atleast one argument

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time # get_ticks()-gives current time in ms --> also it gives time since pygame started and not gonna reset on its own
    # 1sec = 1000 milli sec
    score_surf = test_font.render(f' Score: {current_time}',False,(64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 3

            if obstacle_rect.bottom == 300:screen.blit(snail_srfc,obstacle_rect)
            else:screen.blit(fly_surf,obstacle_rect)


        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return[]

def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf,player_index
    #play walking animation

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk):player_index = 0
        player_surf = player_walk[int(player_index)]
    #display jump surface when player is not on floor


pygame.init() # ---> this line initially starts pygame and initiate all
                # -> subparts of pygame like place images,play sounds

screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Runner") #sets the name of the window

#creating a clock object because it helps with deciding time and setting FPS of the game
clock = pygame.time.Clock()
test_font = pygame.font.Font('Font/Pixeltype.ttf', 50) # arguments(font_type,(font_size))

game_active = True
start_time = 0
score = 0

sky_srfc = pygame.image.load("Graphics/sky.png").convert()
ground_srfc = pygame.image.load("Graphics/ground.png").convert()

snail_srfc = pygame.image.load("Graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_srfc.get_rect(bottomright = (600,300))

fly_surf = pygame.image.load('Graphics/Fly/Fly1.png').convert_alpha()


obstacle_rect_list = []
# score_srfc = test_font.render("score", False,(64,64,64))
# score_rect = score_srfc.get_rect(center = (400,100))


#initially when placed using surfcae there is a gap b/w the player and ground that needs to be bridged
#but it's difficult to do that by using surfcae variables as it just places it at the top bottom
# of the screen ,
# -> That's why we use rectangle
player_walk1 = pygame.image.load("Graphics/Player/player_walk_1.png").convert_alpha()
player_walk2 = pygame.image.load("Graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk1,player_walk2]
player_index = 0
player_jump = pygame.image.load("Graphics/Player/jump.png").convert_alpha()


player_surf = player_walk[player_index]
#Most basic way to create a rectangle
# - > player_rect = pygame.Rect(left,top,width,height)

# but ideally the above method isn't much used while creating rectangle for collision
# what we do is surfc_name.get_rect() to create a rectangle around the surface 
player_rect = player_surf.get_rect(midbottom = (80,300))

player_gravity = 0

#Intro screen
player_stand = pygame.image.load('Graphics/Player/player_stand.png').convert_alpha()
# player_stand = pygame.transform.scale2x(player_stand) just scale the surface twice
player_stand = pygame.transform.rotozoom(player_stand,0,2) # arguments(surface,rotation,scale)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = test_font.render("Pixel Runner",False,(111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))

game_message = test_font.render("Up key to run",False,(111,196,169))
game_message_rect = game_message.get_rect(center = (400,350))


#screen only stays for a second because after line 7 code ends
# and computer stops running pygame code 
# solution for this is a way that keeps our code running for ever
#That's why we use while True: loop

#TIMER

obstacle_timer = pygame.USEREVENT + 1 # we are adding +1 bcz there are some events that are already reserved for pygame itself. And to avoid a conflict
                                        # with those we always have to add +1 to each event we are going to add.
pygame.time.set_timer(obstacle_timer,1500)  # two arguments 1.Event we want to trigger 2.how often we want to trigger in milli second.






while True:
    # checking for player input using event loop
    # this helps in checking event if player click on the close 
    # -- button to close the window

    for event in pygame.event.get():
        # pygame.QUIT resembles the x button of the window
        # so if event is pygame.QUIT we indicate event of closing window 
        if event.type == pygame.QUIT:
            pygame.quit() 
                          #-> Whenever we call pygame.quit() we are doing opposite of
            exit()        #-> pygame.init() i.e pygame.quit() uninitializes everything
                          #-> we may get an error on the terminal saying <video system not initialized>
                          #-> because now we cant run display.update() method 

        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and player_rect.bottom >= 300:
                    player_gravity = -20
        
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                game_active = True
                snail_rect.left = 800
                start_time = int(pygame.time.get_ticks()/1000)

        if event.type == obstacle_timer and game_active:
            if randint(0,2):
                obstacle_rect_list.append(snail_srfc.get_rect(bottomright = (randint(900,1100),300)))
            else:
                obstacle_rect_list.append(fly_surf.get_rect(bottomright = (randint(900,1100),210)))


            
            # exit() command closes all the instructions that are currently running and securely
            # closes pygame instead of using break statement

    # attaching test srfc to display srfc
    # blit(surface, position(x,y)) - block image transfer
        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):print("YES")

    if game_active:
        screen.blit(sky_srfc, (0,0))
        screen.blit(ground_srfc, (0,300))
        #pygame.draw.rect(screen,'Pink',score_rect,6,20)# This line will draw a rounded pink rectangle behind the middle text
        # pygame.draw.rect(screen,'#c0e8ec',score_rect)
        # pygame.draw.rect(screen,'#c0e8ec',score_rect,10)
        # screen.blit(score_srfc, score_rect)
        score = display_score()
        

        snail_rect.x -= 4
        if snail_rect.x<-100:snail_rect.x = 800
        screen.blit(snail_srfc, snail_rect)

        #PLAYER
        player_gravity += 1
        player_rect.y+=player_gravity
        if player_rect.bottom>=300:player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        #obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        
        #COLLISIONS
        game_active = collisions(player_rect,obstacle_rect_list)

        if snail_rect.colliderect(player_rect):
            game_active = False

    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)
        obstacle_rect_list.clear()
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        score_msg = test_font.render(f'your score: {score}',False,(111,196,169))
        score_msg_rect = score_msg.get_rect(center = (400,350))
        screen.blit(game_name,game_name_rect)

        if score == 0:screen.blit(game_message,game_message_rect)
        else:screen.blit(score_msg,score_msg_rect)




        # GAME oVER

       
        
        
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print("jump")
    
    # if player_rect.colliderect(snail_rect):   # this method returns either 0 or 1
    #     print("collision")

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint((mouse_pos)):
    #     print(pygame.mouse.get_pressed()) # to check button pressed


    pygame.display.update() # --> This line updates the display surface that we created
                            # --> on line no 7
    clock.tick(60) # This line tells pygame that the while loop on line 20 mustn't run faster
                    # than 60 times per second(This is the max framerate)

                