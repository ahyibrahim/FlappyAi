import pygame
import random

# Constants for screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200

# Bird constants
BIRD_RADIUS = 30
BIRD_GRAVITY = 1200
BIRD_LIFT = -450
BIRD_COLOR = (255, 165, 0)


# Pipe constants
PIPE_WIDTH = 150
PIPE_GAP = 350
PIPE_SPEED = 250
DISTANCE_TO_NEXT_PIPE = 300

# Coin constants
COIN_RADIUS = 10

# unused Constants
BACKGROUND_COLOR = (135, 206, 235)
# BIRD_GRAVITY = 0.002


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


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BIRD_RADIUS
        self.vel = 0
        self.gravity = BIRD_GRAVITY
        self.lift = BIRD_LIFT
        self.jumping = False
        self.score = 0

    def jump(self, dt):
        self.vel = self.lift

    def update(self, dt):
        self.vel += self.gravity * dt
        self.y += self.vel * dt
        if self.y < 0:
            self.y = 0
            self.vel = 0

    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.vel = 0

    def increase_score(self, value):
        self.score += value

    def draw(self, screen):
        pygame.draw.circle(screen, BIRD_COLOR,
                           (self.x, self.y), self.radius)


class Pipe:
    def __init__(self, x):
        self.x = x + DISTANCE_TO_NEXT_PIPE
        self.width = PIPE_WIDTH
        self.height = random.randint(150, SCREEN_HEIGHT - 350)
        self.gap = PIPE_GAP
        self.speed = PIPE_SPEED
        self.coin = Coin(self.x + self.width // 2, self.height +
                         self.gap // 2, COIN_RADIUS)

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 0),
                         (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, (0, 128, 0), (self.x, self.height +
                         self.gap, self.width, SCREEN_HEIGHT - self.height - self.gap))
        self.coin.draw(screen)

    def update(self, dt):
        self.x -= self.speed * dt
        self.coin.x -= self.speed * dt

    def reset(self, x):
        self.x = x
        self.height = random.randint(150, SCREEN_HEIGHT - 150)
        self.coin.x = self.x + self.width // 2
        self.coin.y = self.height + self.gap // 2


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


class FlappyBirdEnv:
    def __init__(self):
        self.bird = Bird(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.last_pipe_spawn = 0
        self.dt = 0
        self.action_space = type(
            'ActionSpace', (), {'n': 2})  # Define action space

    def get_state(self):
        return [self.bird.y, self.bird.vel]

    # def handle_events(self):
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             done = True
    #             return done
    #         # Handle key presses here
    #         if event.type == pygame.KEYDOWN:
    #             if event.key == pygame.K_SPACE:
    #                 self.action(1, self.dt)  # Flap action
    #     return False

    def create_pipe(self):
        x = SCREEN_WIDTH
        self.pipes.append(Pipe(x))

    # UNUSED-UNUSED-UNUSED-UNUSED-UNUSED-UNUSED Function to check collision between bird and pipes
    def check_collision(self, bird, pipe):
        if bird.x + bird.radius > pipe.x and bird.x - bird.radius < pipe.x + pipe.width:
            if bird.y - bird.radius < pipe.height or bird.y + bird.radius > pipe.height + pipe.gap:
                return True
        return False

    def check_coin_collision(self, coin):
        distance = ((self.bird.x - coin.x)**2 + (self.bird.y - coin.y)**2)**0.5
        return distance < self.bird.radius + coin.radius

    # Function to check if bird goes outside of screen's height
    def check_oob(self):
        if self.bird.y < 0 or self.bird.y > SCREEN_HEIGHT:
            self.bird.reset()
            self.pipes.clear()
            return True
        return False

    def action(self, action, dt):
        if action == 1:  # Flap
            print(self.bird.y)
            self.bird.jump(dt)

    # This function executes every frame (an update loop)
    def step(self, action, dt):
        self.dt = dt
        self.action(action, self.dt)
        self.bird.update(self.dt)

        # Create a new pipe at the edge of the screen after some distance
        if len(self.pipes) == 0 or self.pipes[-1].x < SCREEN_WIDTH - DISTANCE_TO_NEXT_PIPE:
            self.create_pipe()

        if self.check_oob():
            self.reset()

        # Loop to update the pipes and check pipe and coin status
        for pipe in self.pipes:
            pipe.update(dt)

            if self.check_collision(self.bird, pipe):
                self.reset()

            if not pipe.coin.collected and self.check_coin_collision(pipe.coin):
                self.bird.increase_score(10)
                pipe.coin.collected = True
                print(self.bird.score)

        done = False
        return None, 1, done

    def reset(self):
        self.bird.reset()
        self.pipes.clear()
        self.score = 0
        self.last_pipe_spawn = 0
        self.create_pipe()

    def render(self, screen):
        # Fill background with sky blue color
        screen.fill((135, 206, 235))
        # Draw the bird
        self.bird.draw(screen)
        # Draw the pipes
        for pipe in self.pipes:
            pipe.draw(screen)
