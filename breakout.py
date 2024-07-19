import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_COLOR = (0, 255, 0)
BALL_RADIUS = 10
BALL_COLOR = (255, 0, 0)
BRICK_WIDTH = 80
BRICK_HEIGHT = 20
BRICK_COLOR = (0, 0, 255)
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_PADDING = 5
BRICK_OFFSET_TOP = 50

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Breakout Game')

clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect((SCREEN_WIDTH - PADDLE_WIDTH) // 2, SCREEN_HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed_x = 5 * random.choice([-1, 1])
ball_speed_y = 5

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
        brick_y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_OFFSET_TOP
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle.x -= 7
    if keys[pygame.K_RIGHT]:
        paddle.x += 7

    # Keep the paddle inside the screen
    if paddle.left < 0:
        paddle.left = 0
    if paddle.right > SCREEN_WIDTH:
        paddle.right = SCREEN_WIDTH

    # Move the ball
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed_x = -ball_speed_x
    if ball.top <= 0:
        ball_speed_y = -ball_speed_y

    # Ball collision with paddle
    if ball.colliderect(paddle) and ball_speed_y > 0:
        ball_speed_y = -ball_speed_y

    # Ball collision with bricks
    for brick in bricks:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            break

    # Check if ball falls off the screen
    if ball.top > SCREEN_HEIGHT:
        running = False  # Game over

    # Draw everything
    screen.fill((0, 0, 0))  # Clear the screen
    pygame.draw.rect(screen, PADDLE_COLOR, paddle)
    pygame.draw.circle(screen, BALL_COLOR, ball.center, BALL_RADIUS)

    for brick in bricks:
        pygame.draw.rect(screen, BRICK_COLOR, brick)

    pygame.display.flip()  # Update the display

    clock.tick(60)  # Limit to 60 frames per second

pygame.quit()
