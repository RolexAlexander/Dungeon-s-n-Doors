import pygame
import pygame.freetype
import random
import asyncio
import copy

# initialise pygame
pygame.init()

pygame.font.init()

# define font
fonts = pygame.font.get_fonts()
print(fonts)
font1 = pygame.font.SysFont(fonts[0], 20) #pygame.freetype.Font('assets/orange_juice2.0.ttf', 150)
font2 = pygame.font.SysFont(fonts[0], 20)
font3 = pygame.font.SysFont(fonts[0], 30)

# define screen size
width, height = 1500, 800
screen = pygame.display.set_mode((width, height))

# update display
pygame.display.update() 

# set caption
pygame.display.set_caption("Dungeons n' Doors")

# define our clock
clock = pygame.time.Clock()

# define the path for all our music
won = pygame.mixer.Sound("assets/win.wav") # pygame.mixer.Sound("win.wav")
key = pygame.mixer.Sound("assets/key.wav")
lost = pygame.mixer.Sound("assets/lose.wav")
jumping = pygame.mixer.Sound("assets/jump.wav")
background = "assets/sound.wav"
 
# define function to start game
async def main():
    """
    Function that starts our game
    """
    
    # define variables to determine if user win, loses or meets a disaster
    win = False
    lose = False
    disaster = False
    awaiting_user = False

    # define player location
    player_x = 100
    player_y = 100

    # define velocity
    speed = 5
    player_y_vel = 2
    player_x_vel = 0

    # player variable to control character changes
    player = 1
    
    # define how the character looks when running
    running1 = pygame.transform.scale(pygame.image.load(f"assets/player{player}_left.png"), (width*0.045,height*0.045))
    running2 = pygame.transform.scale(pygame.image.load(f"assets/player{player}_right.png"), (width*0.045,height*0.045))
    standing = pygame.transform.scale(pygame.image.load(f"assets/player{player}_standing.png"), (width*0.045,height*0.045))
    door_surface = pygame.image.load("assets/door.png")
    key_surface = pygame.image.load("assets/key.png")
    background_surface = pygame.image.load("assets/background.gif")
    diamond_surface = pygame.image.load("assets/diamond.png")
    win_screen = pygame.image.load("assets/win.png")
    disaster_screen = pygame.image.load("assets/disaster.png")
    nowhere_screen = pygame.image.load("assets/nowhere.png")

    # define how character looks when running backwards
    running_left1 = pygame.transform.flip(running1, True, False)
    running_left2 = pygame.transform.flip(running2, True, False)

    # define the direction the character is facing
    direction = "standing"

    # define how character looks when running
    running_list = [running1, running2]
    counter = 1

    # initialise character variable
    character = None

    # know if the user has jumped
    jump = False

    # define gravity
    gravity = 5

    # define key found
    key_found = False

    # define door found
    door_found = False

    # add sound
    pygame.mixer.music.load(background)
    pygame.mixer.music.play(-1)

    # set run true so the game will operate
    run = True

    # levels doors and key coordinates. This is done randomly so that we can have multiple levels
    # keys we add 20 and -25 pixels.
    # for doors we just y -75
    platform_locations = [  (30, 500),
                            (200, 450),
                            (380, 400),
                            (680, 500), 
                            (550, 450),
                            (200, 350),
                            (550, 350),
                            (680, 300),
                            (550, 250),
                            (380, 300),
                            (1380, 500),
                            (1230, 450),
                            (1080, 400),
                            (820, 450),
                            (820, 350),
                            (1290, 310),
                            (950, 280),
                            (1000, 530),
                            (920, 110),
                            (30, 210),
                            (750, 180),
                            (1120, 200),
                        ] 
    current_locations = copy.deepcopy(platform_locations)
    # declare door locations x and y
    door1 = None
    door2 = None
    door3 = None

    # declare variables for 5 keys
    key1 = None
    key2 = None
    key3 = None
    key4 = None
    key5 = None

    key1_found = False # check if key has been found
    key2_found = False # check if key has been found
    key3_found = False # check if key has been found
    key4_found = False # check if key has been found
    key5_found = False # check if key has been found

    key1_updated_found = False # check if key has been found
    key2_updated_found = False # check if key has been found
    key3_updated_found = False # check if key has been found
    key4_updated_found = False # check if key has been found
    key5_updated_found = False # check if key has been found

    # declare score and level
    score = 0
    level = 1

    # declare variable to know if we displyed result
    display_result = False
    
    # variable for the diamond
    diamond_found = False
    diamond_location = None
    diamond = None

    # main menu
    main_menu = True

    # pause screen
    pause = False

    r = 0
    b = 0
    g = 0

    # Load images
    background_image = pygame.image.load("assets/back.png")
    play_button_image = pygame.image.load("assets/button1.png")
    quit_button_image = pygame.image.load("assets/button2.png")

    # Resize images
    background_image = pygame.transform.scale(background_image, (width, height))
    play_button_image = pygame.transform.scale(play_button_image, (200, 100))
    quit_button_image = pygame.transform.scale(quit_button_image, (200, 100))

    # Define button positions
    play_button_pos = (width // 2 - 100, height // 2 - 50)
    quit_button_pos = (width // 2 - 100, height // 2 + 100)

    # set can exit true
    can_exit = True

    # game loop
    while run: 
        # interate over events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # pygame.exit()
                pass
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    player_x_vel = -speed
                if event.key == pygame.K_RIGHT:
                    direction = "right"
                    player_x_vel = speed
                if event.key == pygame.K_UP:
                    # change the player
                    if main_menu or pause:
                        if player == 6:
                            player = 1
                        else: player+=1
                        running1 = pygame.transform.scale(pygame.image.load(f"assets/player{player}_left.png"), (width*0.045,height*0.045))
                        running2 = pygame.transform.scale(pygame.image.load(f"assets/player{player}_right.png"), (width*0.045,height*0.045))
                        standing = pygame.transform.scale(pygame.image.load(f"assets/player{player}_standing.png"), (width*0.045,height*0.045))
                        running_left1 = pygame.transform.flip(running1, True, False)
                        running_left2 = pygame.transform.flip(running2, True, False)
                        running_list = [running1, running2]
                if event.key == pygame.K_DOWN:
                    # change the player
                    if main_menu or pause:
                        if player == 1:
                            player = 6
                        else: player-=1
                    running1 = pygame.transform.scale(pygame.image.load(f"assets/player{player}_left.png"), (width*0.045,height*0.045))
                    running2 = pygame.transform.scale(pygame.image.load(f"assets/player{player}_right.png"), (width*0.045,height*0.045))
                    standing = pygame.transform.scale(pygame.image.load(f"assets/player{player}_standing.png"), (width*0.045,height*0.045))
                    running_left1 = pygame.transform.flip(running1, True, False)
                    running_left2 = pygame.transform.flip(running2, True, False)
                    running_list = [running1, running2]
                if event.key == pygame.K_SPACE:
                    # check if player jumped and then we proceed if not and jump
                    if jump == False:
                        jump = True
                        player_y_vel = -15 # jump height in pixels

                        # play music
                        jumping.play() 

                if event.key == pygame.K_TAB: # reset game for the next level
                    if win:
                        level += 1
                        score += 50
                    
                    if awaiting_user == True:
                        door_found = False
                        key_found = False
                        awaiting_user = False
                        current_locations = copy.deepcopy(platform_locations)
                        door1 = None
                        door2 = None
                        door3 = None
                        win = False
                        lose = False
                        diamond_found = False
                        diamond_location = None
                        diamond = None
                        disaster = False
                        key1 = None
                        key2 = None
                        key3 = None
                        key4 = None
                        key5 = None
                        key1_found = False # check if key has been found
                        key2_found = False # check if key has been found
                        key3_found = False # check if key has been found
                        key4_found = False # check if key has been found
                        key5_found = False # check if key has been found
                        key1_updated_found = False # check if key has been found
                        key2_updated_found = False # check if key has been found
                        key3_updated_found = False # check if key has been found
                        key4_updated_found = False # check if key has been found
                        key5_updated_found = False # check if key has been found
                        display_result = False
                        player_y = 100
                        player_x = 150

                if event.key == pygame.K_ESCAPE:
                    # set pause equal true
                    pause = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player_y_vel = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    direction = "standing"
                    player_x_vel = 0
            if event.type == pygame.MOUSEBUTTONDOWN:
                can_exit = True
        if main_menu or pause:
            # fill the screen with a nice color
            screen.fill((255,255,255))

            # add background image
            new_background = pygame.transform.scale(background_image,(width,height))
            screen.blit(new_background, (0,0))

            # draw stick men
            # Draw stickman characters
            player_character = screen.blit(pygame.transform.scale(pygame.image.load(f"assets/player{player}_standing.png"), (width*0.2,height*0.2)),(0,410))

            # blit the stuff to the screen
            # Draw buttons on the screen
            scaled_play_button = pygame.transform.scale(play_button_image, (width*0.2,height*0.2))
            scaled_exit_button = pygame.transform.scale(quit_button_image, (width*0.2,height*0.2))
            play_game = screen.blit(scaled_play_button, play_button_pos)
            exit_game = screen.blit(scaled_exit_button, quit_button_pos)

            # logic to check if mouse click the buttons
            # Get the mouse position and button state
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_left, mouse_middle, mouse_right = pygame.mouse.get_pressed()

            # check if collede point and clicked
            # Check if the left mouse button is pressed and the mouse is over the rectangle
            if mouse_left and play_game.collidepoint(mouse_x, mouse_y):
                # exit main menu
                if main_menu:
                    main_menu = False
                elif pause:
                    pause = False
            if mouse_left and exit_game.collidepoint(mouse_x, mouse_y):
                if can_exit: 
                    # exit main menu
                    if main_menu and not pause:
                        # pygame.quit()
                        can_exit = False
                    elif pause:
                        main_menu = True
                        score = 0
                        level = 1
                        can_exit = False
            pygame.display.update() # update display to show changes

        # finish game if player found the door
        elif door_found == True:
            # if the user lost we display lost message
            if lose:
                if not display_result:
                    display_result = True

                    # display lose screen
                    game_result = pygame.transform.scale(disaster_screen,(1500,800))
                    screen.blit(game_result, (0,0))

                    # display text to let the user know what to click to continue
                    text = font3.render("Click TAB to continue ....", False, (255,0,0))
                    screen.blit(text, (10,10))

                    # update the display
                    pygame.display.update()
                    awaiting_user = True # set awaiting user to true
                    lost.play() # play sound effect
            if win:
                if not display_result:
                    # reset variables
                    display_result = True
                    win = True

                    # display lose screen
                    game_result = pygame.transform.scale(win_screen,(1500,800))
                    screen.blit(game_result, (0,0))

                    # display text to let the user know what to click to continue
                    text = font3.render("Click TAB to continue ....", False, (255,0,0))
                    screen.blit(text, (10,10))

                    pygame.display.update() # update the display
                    awaiting_user = True # set awaiting user to true
                    won.play() # play sound effect
            else: 
                if not display_result:
                    display_result = True
                    # utilise randomint to decide the users fate
                    fate = random.randint(1, 3) # random int between 1 and 3
                    print(f"This is the fate {fate}")
                    if fate == 1:
                        # user wins
                        win = True

                        # display lose screen
                        game_result = pygame.transform.scale(win_screen,(1500,800))
                        screen.blit(game_result, (0,0))

                        # display text to let the user know what to click to continue
                        text = font3.render("Click TAB to continue ....", False, (255,0,0))
                        screen.blit(text, (10,10))

                        pygame.display.update() # update the display
                        awaiting_user = True # set awaiting user to true
                        won.play() # play sound effect
                    elif fate == 2:
                        # user experiences nowhere for a few seconds
                        # display nowhere screen
                        game_result = pygame.transform.scale(nowhere_screen,(1500,800))
                        screen.blit(game_result, (0,0))

                        # display text to let the user know what to click to continue
                        text = font3.render("Click TAB to continue ....", False, (255,0,0))
                        screen.blit(text, (10,10))

                        pygame.display.update() # update the display
                        awaiting_user = True # set awaiting user to true
                        lost.play() # play sound effect
                    else:
                        # user experience disaster
                        disaster = True

                        # display lose screen
                        game_result = pygame.transform.scale(disaster_screen,(1500,800))
                        screen.blit(game_result, (0,0))

                        # display text to let the user know what to click to continue
                        text = font3.render("Click TAB to continue ....", False, (255,0,0))
                        screen.blit(text, (10,10))

                        pygame.display.update() # update the display
                        awaiting_user = True # set awaiting user to true
                        lost.play() # play sound effect
        else:
            # move character
            player_x += player_x_vel
            player_y = player_y + player_y_vel

            # fill the screen with a nice color
            screen.fill((255,255,255))

            # add background image
            new_background = pygame.transform.scale(background_surface,(1500,800))
            screen.blit(new_background, (0,0))

            # add score and level to screen
            text = font2.render(f"Score: {score}      Level: {level}", False, (255,255,255))
            screen.blit(text, (10,10))


            # draw the platform for character to stand on
            pygame.draw.rect(screen, (100,100,100), (30, 500, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (200, 450, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (380, 400, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (680, 500, 100, 10)) ####
            pygame.draw.rect(screen, (100,100,100), (550, 450, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (200, 350, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (550, 350, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (680, 300, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (550, 250, 100, 10))
            lava = pygame.draw.rect(screen, (255,0,0), (0, 550, width, height))
            pygame.draw.rect(screen, (100,100,100), (380, 300, 100, 10))

            pygame.draw.rect(screen, (100,100,100), (1380, 500, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (1230, 450, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (1080, 400, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (820, 450, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (820, 350, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (1290, 310, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (950, 280, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (1000, 530, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (920, 110, 200, 10))
            pygame.draw.rect(screen, (100,100,100), (30, 210, 300, 10))
            pygame.draw.rect(screen, (100,100,100), (750, 180, 100, 10))
            pygame.draw.rect(screen, (100,100,100), (1120, 200, 100, 10))

            # # draw doors and keys
            if door_found == False:
                if not door1:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[1] -= 75
                    door1 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                if not door2:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[1] -= 75
                    door2 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                if not door3:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[1] -= 75
                    door3 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                door_1 = screen.blit(door_surface, door1)
                door_2 = screen.blit(door_surface, door2)
                door_3 = screen.blit(door_surface, door3)

            # # add the key
            if key1_found == False:
                if not key1:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[0] += 20
                    tmp[1] -= 25
                    key1 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                key_1 = screen.blit(key_surface, key1)
            if key2_found == False:
                if not key2:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[0] += 20
                    tmp[1] -= 25
                    key2 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                key_2 = screen.blit(key_surface, key2)
            if key3_found == False:
                if not key3:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[0] += 20
                    tmp[1] -= 25
                    key3 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                key_3 = screen.blit(key_surface, key3)
            if key4_found == False:
                if not key4:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[0] += 20
                    tmp[1] -= 25
                    key4 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                key_4 = screen.blit(key_surface, key4)
            if key5_found == False:
                if not key5:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[0] += 20
                    tmp[1] -= 25
                    key5 = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                key_5 = screen.blit(key_surface, key5)

            # draw diamond on screen
            if diamond_found == False:
                if not diamond_location and level%2 == 0:
                    loc = current_locations[random.randint(0, len(current_locations)-1)]
                    tmp = list(loc)
                    tmp[0] += 20
                    tmp[1] -= 33
                    diamond_location = tuple(tmp)
                    current_locations.pop(current_locations.index(loc))
                if diamond_location:
                    diamond = screen.blit(diamond_surface, diamond_location)
                else: diamond = False # reset to not cause errors

            # draw the character
            if direction == "left":
                if counter%2==0:
                    character = screen.blit(running_left2, (player_x, player_y))
                else:
                    character = screen.blit(running_left1, (player_x, player_y))
            if direction == "right":
                if counter%2==0:
                    character = screen.blit(running2, (player_x, player_y))
                else:
                    character = screen.blit(running1, (player_x, player_y))
            if direction == "standing":
                character = screen.blit(standing, (player_x, player_y))
            counter+=1 # increment counter to make the moster run

            # # define event to handle when character and key collides
            if character.colliderect(key_1):
                key1_found = True # know if de player pick up the key
                if key1_found and not key1_updated_found:
                    score += 5 # add score
                    key1_updated_found = True
                    key.play()
            if character.colliderect(key_2):
                key2_found = True
                if key2_found and not key2_updated_found:
                    score += 10
                    key2_updated_found = True
                    key.play()
            if character.colliderect(key_3):
                key3_found = True
                if key3_found and not key3_updated_found:
                    score += 15
                    key3_updated_found = True
                    key.play()
            if character.colliderect(key_4):
                key4_found = True
                if key4_found and not key4_updated_found:
                    score += 20
                    key4_updated_found = True
                    key.play()
            if character.colliderect(key_5):
                key5_found = True
                if key5_found and not key5_updated_found:
                    score += 25
                    key5_updated_found = True
                    key.play()

            if (character.colliderect(door_1) or character.colliderect(door_2) or character.colliderect(door_3)):
                if key1_found and key2_found and key3_found and key4_found and key5_found:
                    door_found = True # know if de player found the door

            # code if the user lost
            if character.colliderect(lava):
                lose = True
                door_found = True

            # add platform for player to stand on based on color
            if screen.get_at((character.left, character.bottom)) == (100,100,100) or screen.get_at((character.right, character.bottom)) == (100,100,100): 
                player_y_vel = 0
                jump = False
            else:
                if jump == False:
                    player_y_vel = 2 # make them fall

            # code to control jumping
            if jump == True:
                # add gravity to pull player down
                player_y_vel += gravity
                # added double jump for the kings mu oo ha ha evil laugh
                jump = False

            # code to know if the person collided with the diamond
            if diamond:
                if character.colliderect(diamond):
                    door_found = True # know if de player pick up the key
                    win = True
                    score += 30 # add score
                    key.play()
            clock.tick(30) # update clock to 60 fps
            pygame.display.update() # update display to show changes

        await asyncio.sleep(0)

asyncio.run(main())