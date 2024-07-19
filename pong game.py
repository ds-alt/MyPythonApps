import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Clock for controlling FPS
clock = pygame.time.Clock()

# Paddle settings
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_SPEED = 5

# Ball settings
BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 5

# Initialize paddles and ball
player1_paddle = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ai_paddle = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Ball direction
ball_speed_x = BALL_SPEED_X * random.choice([1, -1])
ball_speed_y = BALL_SPEED_Y * random.choice([1, -1])

# Scores
player_score = 0
player1_score = 0
player2_score = 0
ai_score = 0

# Game state
playing_against_ai = None  # None means mode selection screen
game_over = False

# Function to reset game state
def reset_game():
    global player_score, player1_score, player2_score, ai_score, game_over
    player_score = 0
    player1_score = 0
    player2_score = 0
    ai_score = 0
    game_over = False
    reset_ball()

# Function to reset ball position
def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH // 2, HEIGHT // 2)
    ball_speed_x *= random.choice([1, -1])
    ball_speed_y *= random.choice([1, -1])

# Function to display mode selection menu
def display_mode_menu():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    mode_text = font.render("Press '1' to play against AI", True, WHITE)
    mode_text2 = font.render("Press '2' for two players", True, WHITE)
    screen.blit(mode_text, (WIDTH // 2 - 200, HEIGHT // 2 - 50))
    screen.blit(mode_text2, (WIDTH // 2 - 200, HEIGHT // 2 + 50))
    pygame.display.flip()

# Function to display help menu
def display_help():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    help_text1 = font.render("Controls:", True, WHITE)
    help_text2 = font.render("Player 1 (left paddle): Up/Down arrow keys", True, WHITE)
    help_text3 = font.render("Player 2 (right paddle): 'K'/'M' keys", True, WHITE)
    help_text4 = font.render("Press 'Esc' to return to menu", True, WHITE)
    screen.blit(help_text1, (50, 50))
    screen.blit(help_text2, (50, 100))
    screen.blit(help_text3, (50, 150))
    screen.blit(help_text4, (50, 200))
    pygame.display.flip()

# Main game loop
running = True
mode_selected = False
while running:
    if not mode_selected:
        display_mode_menu()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not mode_selected:
                if event.key == pygame.K_1:
                    playing_against_ai = True
                    mode_selected = True
                    reset_game()
                elif event.key == pygame.K_2:
                    playing_against_ai = False
                    mode_selected = True
                    reset_game()
            else:
                if event.key == pygame.K_ESCAPE:
                    mode_selected = False
                elif event.key == pygame.K_h:
                    display_help()

    if mode_selected:
        if not game_over:
            # Move player1 paddles
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and player1_paddle.top > 0:
                player1_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and player1_paddle.bottom < HEIGHT:
                player1_paddle.y += PADDLE_SPEED

            # Move AI paddle or player2 paddle (two-player mode)
            if playing_against_ai:
                if ai_paddle.centery < ball.centery and ai_paddle.bottom < HEIGHT:
                    ai_paddle.y += PADDLE_SPEED
                if ai_paddle.centery > ball.centery and ai_paddle.top > 0:
                    ai_paddle.y -= PADDLE_SPEED
            else:
                if keys[pygame.K_k] and player2_paddle.top > 0:
                    player2_paddle.y -= PADDLE_SPEED
                if keys[pygame.K_m] and player2_paddle.bottom < HEIGHT:
                    player2_paddle.y += PADDLE_SPEED

            # Move ball
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            # Ball collision with paddles
            if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle) or ball.colliderect(ai_paddle):
                ball_speed_x *= -1

            # Ball collision with top and bottom walls
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed_y *= -1

            # Ball goes out of bounds (scoring)
            if ball.left <= 0:
                ai_score += 1
                if ai_score >= 5:
                    game_over = True
                else:
                    reset_ball()

            if ball.right >= WIDTH:
                if playing_against_ai:
                    player_score += 1
                else:
                    player2_score += 1
                if player_score >= 5 or player2_score >= 5:
                    game_over = True
                else:
                    reset_ball()

        # Draw objects on the screen
        screen.fill(BLACK)
        pygame.draw.rect(screen, (255, 255, 0), player1_paddle)
        if playing_against_ai:
            pygame.draw.rect(screen, WHITE, ai_paddle)
        else:
            pygame.draw.rect(screen, WHITE, player2_paddle)
        pygame.draw.ellipse(screen, (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)), ball)

        # Display scores
        font = pygame.font.Font(None, 36)
        player1_text = font.render(f"Player 1: {player1_score}", True, WHITE)
        if not playing_against_ai:
            player2_text = font.render(f"Player 2: {player2_score}", True, WHITE)
            screen.blit(player2_text, (20, 60))
        ai_text = font.render(f"AI: {ai_score}", True, WHITE)
        screen.blit(player1_text, (20, 20))
        screen.blit(ai_text, (WIDTH - 120, 20))

        # Display game over message
        if game_over:
            winner_text = font.render("Game Over", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))

        # Display mode selection message if help not shown
        if not game_over and not mode_selected:
            mode_text = font.render("Press '1' for AI, '2' for two players", True, WHITE)
            screen.blit(mode_text, (WIDTH // 2 - 240, HEIGHT - 50))

        # Update the display
        pygame.display.flip()

    # Control the FPS
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
