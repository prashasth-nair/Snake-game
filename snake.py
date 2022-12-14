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
snake_size = 30

class Snake():
    def __init__(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.color = (17, 24, 47)
        # Special thanks to YouTubers Mini - Cafetos and Knivens Beast for raising this issue!
        # Code adjustment courtesy of YouTuber Elija de Hoog
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x,y = self.direction
        new = (((cur[0]+(x*snake_size))%screen_width), (cur[1]+(y*snake_size))%screen_height)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0,new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [((screen_width/2), (screen_height/2))]
        self.direction = random.choice([up, down, left, right])
        self.score = 0

    def draw(self,surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (snake_size,snake_size))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93,216, 228), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(up)
                elif event.key == pygame.K_DOWN:
                    self.turn(down)
                elif event.key == pygame.K_LEFT:
                    self.turn(left)
                elif event.key == pygame.K_RIGHT:
                    self.turn(right)

food_x = random.randint(20,screen_width/2)
food_y = random.randint(20,screen_height/2)
class Food():
    def __init__(self):
        self.position = (0,0)
        self.color = red
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, screen_width-1)*snake_size, random.randint(0, screen_height-1)*snake_size)

    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (snake_size, snake_size))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)

def drawGrid(surface):
    for y in range(0, int(grid_height)):
        for x in range(0, int(grid_width)):
            if (x+y)%2 == 0:
                r = pygame.Rect((x*snake_size, y*snake_size), (snake_size,snake_size))
                pygame.draw.rect(surface,(93,216,228), r)
            else:
                rr = pygame.Rect((x*snake_size, y*snake_size), (snake_size,snake_size))
                pygame.draw.rect(surface, (84,194,205), rr)

screen_width = 900
screen_height = 700

gridsize = 20
grid_width = screen_width/gridsize
grid_height = screen_height/gridsize

up = (0,-1)
down = (0,1)
left = (-1,0)
right = (1,0)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])

def main():
    # game specific variables
    exit_game = False
    game_over = False

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snake = Snake()
    food = Food()

    myfont = pygame.font.SysFont("monospace",20)

    #Opening hiscore file
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
            
        clock.tick(10)
        snake.handle_keys()
        drawGrid(surface)
        snake.move()
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
        snake.draw(surface)
        food.draw(surface)
        screen.blit(surface, (0,0))
        text_screen("Score: "+str(snake.score), red, 5, 5)
        text_screen("High Score: "+str(hiscore), red, 600, 5)
        pygame.display.update()

main()