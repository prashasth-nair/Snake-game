import pygame
import random
import sys

# initialize pygame
pygame.init()

# colors
white = (255, 255, 255) 
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0,255,0)
black =(0, 0, 0)

# creating windows
screen_width = 900
screen_height = 700
gameWindow = pygame.display.set_mode((screen_width,screen_height))

# Game Title/icon
pygame.display.set_caption("Snake Game")
icon = pygame.image.load("snake.png")
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
pygame.display.update()


font = pygame.font.SysFont("monospace", 30)
fps = 40

#Functions
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game= False
    while not exit_game:
        gameWindow.fill(black)
        text_screen("Welcome to Snakes", white,screen_width/3,screen_height/6)
        text_screen("Press Enter To Start", white,300,500)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
                pygame.quit()
                
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit_game = True
                    game_loop()
        # clock.tick(fps)
            



#Game Loop
def game_loop():
    # game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    food_x = random.randint(20,screen_width/2)
    food_y = random.randint(20,screen_height/2)
    score = 0
    init_velocity = 5
    snake_size = 30
    snk_list = []
    snk_length = 1 #increase the size of snake

    with open("high-score.txt","r") as f:
        hiscore = f.read()

    while not exit_game:
        if game_over:
            with open("high-score.txt","wt") as f:
                f.write(str(hiscore))
            gameWindow.fill(black)
            text_screen("Game over! Press Enter To continue", red, 200, 180)
            text_screen(f"Total Score: {score}", green , 350, 240)
            text_screen(f"High Score: {hiscore}", red , 350, 280)
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game = True 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()
        else:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    exit_game = True 
                if event.type==pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = 5
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -5
                        velocity_y = 0


                    if event.key == pygame.K_UP:
                        velocity_x = 0
                        velocity_y = -5

                    
                    if event.key == pygame.K_DOWN:
                        velocity_x = 0
                        velocity_y = 5
                    # TODO:add pause screen.
                    if event.key == pygame.K_ESCAPE:
                        pass
            
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y
            
            #printing score/high score in screen and making food display in screen
            if abs(snake_x - food_x)<20 and abs(snake_y-food_y)<20:
                score += 1
                food_x = random.randint(20,screen_width/2)
                food_y = random.randint(20,screen_height/2)
                snk_length += 5
                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(black)
            text_screen("Score: "+str(score), red, 5, 5)
            text_screen("High Score: "+str(hiscore), red, 630, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]

            
            for i in range(1,len(snk_list)):

                if head in snk_list[:1]:
                    continue
                elif head in snk_list[:-2]:
                    game_over = True
                else:
                    continue
            
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_width:
                game_over = True
            
            plot_snake(gameWindow, white, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    # quit()

welcome()