import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
screen_width = 800
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.SysFont('comicsans', 30)


# Define colors
background_color = (135, 206, 235)  # Sky Blue color

# Bird Settings
bird_color = (255, 165, 0)
bird_lift = -0.5
bird_radius = 25
bird_gravity = 0.002

# Coin Settings
coin_radius = 20


# Bird class
class Bird:
    def __init__(self, x, y, radius, gravity, lift):
        self.x = x
        self.y = y
        self.radius = radius
        self.vel = 0
        self.gravity = gravity
        self.lift = lift
        self.score = 0
        self.jumping = False

    def draw(self, screen):
        pygame.draw.circle(screen, bird_color, (self.x, self.y), self.radius)

    def jump(self):
        if not self.jumping:
            self.vel = self.lift
            self.jumping = True

    def update(self):
        self.vel += self.gravity
        self.y += self.vel

        if self.y < 0:
            self.y = 0
            self.vel = 0
        # Reset jumping flag when bird starts falling after jump
        if self.vel > 0:
            self.jumping = False

    def reset(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.vel = 0
        self.score = 0

    def increase_score(self, value):
        self.score += value

# Coin class


class Coin:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            pygame.draw.circle(screen, (255, 215, 0),
                               (self.x, self.y), self.radius)

# Pipe class


class Pipe:
    def __init__(self, x, width, gap, speed):
        self.x = x
        self.width = width
        self.height = random.randint(150, screen_height - 150)
        self.gap = gap
        self.speed = speed
        self.coin = Coin(self.x + self.width // 2,
                         self.height + self.gap // 2, coin_radius)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 0),
                         (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, (0, 128, 0), (self.x, self.height +
                         self.gap, self.width, screen_height - self.height - self.gap))
        self.coin.draw(screen)

    def update(self):
        self.x -= self.speed
        self.coin.x -= self.speed

    def reset(self, x):
        self.x = x
        self.height = random.randint(150, screen_height - 150)
        self.coin.x = self.x + self.width // 2
        self.coin.y = self.height + self.gap // 2

# Button class


class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, screen):
        pygame.draw.rect(screen, self.color,
                         (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render(self.text, 1, (0, 0, 0))
        screen.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                    self.y + (self.height/2 - text.get_height()/2)))

    def is_clicked(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


# Initialize bird and game variables
bird = Bird(screen_width // 2, screen_height // 2,
            bird_radius, bird_gravity, bird_lift)
start_button = Button(screen_width // 2 - 50, screen_height //
                      2 - 25, 100, 50, (0, 255, 0), 'Start')
game_started = False
pipes = []
coins = []


# Function to check collision between bird and pipes
def check_collision(bird, pipe):
    if bird.x + bird.radius > pipe.x and bird.x - bird.radius < pipe.x + pipe.width:
        if bird.y - bird.radius < pipe.height or bird.y + bird.radius > pipe.height + pipe.gap:
            return True
    return False


# Function to check collision between bird and coin
def check_coin_collision(bird, coin):
    distance = ((bird.x - coin.x)**2 + (bird.y - coin.y)**2)**0.5
    return distance < bird.radius + coin.radius


# Game loop --------------------------------------------------------------------------------------
running = True
# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if not game_started and start_button.is_clicked(pos):
                game_started = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        bird_color = (0, 0, 255)
        bird.jump()

    if game_started:
        # ... (rest of the game logic)

        # Update bird
        bird.update()

        # Check if bird goes outside of screen's height
        if bird.y < 0 or bird.y > screen_height:
            bird.reset()
            game_started = False
            pipes.clear()

        # Spawn pipes
        NEXT_PIPE_DISTANCE = 700
        if len(pipes) == 0 or pipes[-1].x < screen_width - NEXT_PIPE_DISTANCE:
            pipes.append(Pipe(screen_width, 150, 200, 0.2))

        # Update pipes and coins
        for pipe in pipes:
            pipe.update()

            # Check for pipe collision
            if bird.x + bird.radius > pipe.x and bird.x - bird.radius < pipe.x + pipe.width:
                if bird.y - bird.radius < pipe.height or bird.y + bird.radius > pipe.height + pipe.gap:
                    bird.reset()
                    game_started = False
                    pipes.clear()

            # Check for coin collision
            if not pipe.coin.collected and check_coin_collision(bird, pipe.coin):
                bird.increase_score(10)
                pipe.coin.collected = True

    # Render score
    score_text = font.render("Score: " + str(bird.score), 1, (0, 0, 0))

    # Fill the screen with the background color
    screen.fill(background_color)

    # Draw pipes and coins
    for pipe in pipes:
        pipe.draw(screen)

    # Draw the bird
    bird.draw(screen)

    # Draw score counter
    screen.blit(score_text, (screen_width - score_text.get_width() - 10, 10))

    # Draw start button if game not started
    if not game_started:
        start_button.draw(screen)

    pygame.display.update()

pygame.quit()
