import pygame
# Import FlappyBirdEnv class and Button class
from Env import FlappyBirdEnv, Button, PIPE_WIDTH, PIPE_GAP, COIN_RADIUS, PIPE_GAP, SCREEN_HEIGHT, SCREEN_WIDTH

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
env = FlappyBirdEnv()
done = False

while not done:
    dt = clock.tick(144) / 500  # Delta time in seconds
    # done = env.handle_events()  # Check for user input and        done flag
    if not done:
        action = 0  # No action by default
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Handle key presses here
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    action(1, dt)  # Flap action
        observation, reward, done = env.step(action, dt)
        env.render(screen)
        pygame.display.flip()

pygame.quit()
