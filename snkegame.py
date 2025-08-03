import pygame
import random
import sys
import os

# Initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# Game window size
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
FPS = 10

# Colors
WHITE = (300, 300, 300)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 155, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


# Fonts
font = pygame.font.SysFont("comicsansms", 30)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Load sound safely
try:
    eat_sound = pygame.mixer.Sound('beep.wav')
except pygame.error:
    print("Sound file not found or failed to load.")
    eat_sound = None

clock = pygame.time.Clock()

# Draw the snake
def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, DARK_GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])
        pygame.draw.rect(screen, GREEN, [block[0]+2, block[1]+2, BLOCK_SIZE-4, BLOCK_SIZE-4])

# Display message
def message(msg, color, y_offset=0):
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(text, text_rect)

# Main game loop
def game_loop():
    game_over = False
    game_close = False

    x = WIDTH // 2
    y = HEIGHT // 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    score = 0
    speed = FPS

    while not game_over:

        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press R to Restart or Q to Quit", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -BLOCK_SIZE
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = BLOCK_SIZE
                    dx = 0

        x += dx
        y += dy

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        draw_snake(snake_list)

        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()

        # Eat food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1
            score += 10
            if eat_sound:
                eat_sound.play()
            if score % 50 == 0:
                speed += 1

        clock.tick(speed)

    pygame.quit()
    sys.exit()

# Start screen
def start_screen():
    screen.fill(BLACK)
    message("Press any key to start", BLUE)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Main
if __name__ == "__main__":
    start_screen()
    game_loop()
#new line add



