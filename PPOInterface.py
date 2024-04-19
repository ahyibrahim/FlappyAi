import pygame
import numpy as np
import tensorflow as tf
from Env import FlappyBirdEnv, Button, SCREEN_HEIGHT, SCREEN_WIDTH

# Initialize environment
env = FlappyBirdEnv()

# Initialize TensorFlow model (you can replace this with your PPO model)
# For simplicity, let's assume a basic neural network model
model = tf.keras.Sequential([
    # input shape depends on your state representation
    tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    # assuming a discrete action space
    tf.keras.layers.Dense(env.action_space.n, activation='softmax')
])

# Load model weights (you can replace 'model_weights.h5' with your model's file)
model.load_weights('model_weights.h5')

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Main loop
done = False
while not done:
    dt = clock.tick(144) / 1000  # Delta time in seconds

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # Get current state
    state = env.get_state()

    # Predict action using the model
    # For now, let's assume the model expects a batch of states
    # and returns a batch of action probabilities
    action_probs = model.predict(np.array([state]))

    # Sample action from action probabilities
    action = np.random.choice(env.action_space.n, p=action_probs[0])

    # Step environment
    observation, reward, done = env.step(action, dt)

    # Render environment
    env.render(screen)
    pygame.display.flip()

pygame.quit()
