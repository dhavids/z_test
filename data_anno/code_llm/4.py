import pygame
import random

# Initialize Pygame
pygame.init()

# Game Dimensions
grid_size = 10
block_size = 40
screen_width = block_size * grid_size
screen_height = block_size * grid_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
block_color = (0, 255, 0)  # Green

# Block Shapes (Tetrominoes)
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
]

# Game Variables
grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
current_shape = None
current_x = 4
current_y = 0

# Game Functions
def new_shape():
    global current_shape, current_x, current_y
    current_shape = random.choice(shapes)
    current_x = 4
    current_y = 0

def draw_grid():
    for y in range(grid_size):
        for x in range(grid_size):
            rect = pygame.Rect(x * block_size, y * block_size, block_size, block_size)
            if grid[y][x] == 1:
                pygame.draw.rect(screen, block_color, rect)
            pygame.draw.rect(screen, black, rect, 1)

def draw_shape():
    for y, row in enumerate(current_shape):
        for x, cell in enumerate(row):
            if cell == 1:
                rect = pygame.Rect((current_x + x) * block_size, (current_y + y) * block_size, block_size, block_size)
                pygame.draw.rect(screen, block_color, rect)

# Main Game Loop
new_shape()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game Logic (Movement, Collisions, etc.)

    # Draw Everything
    screen.fill(white)
    draw_grid()
    draw_shape()
    pygame.display.flip()

pygame.quit()