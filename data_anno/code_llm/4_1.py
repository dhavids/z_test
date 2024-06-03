import pygame
import random

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

class Tetris:
    def __init__(self, grid_size, block_size, block_color):
        self.grid_size = grid_size
        self.block_size = block_size
        self.block_color = block_color
        screen_size = self.grid_size * self.block_size
        pygame.init()
        self.screen = pygame.display.set_mode((screen_size, screen_size))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.shapes = [
            [[1, 1, 1, 1]],
            [[1, 1], [1, 1]],
            [[1, 1, 0], [0, 1, 1]],
            [[0, 1, 1], [1, 1, 0]],
            [[1, 1, 1], [0, 1, 0]],
            [[1, 1, 1], [1, 0, 0]],
            [[1, 1, 1], [0, 0, 1]],
        ]
        self.new_shape()

    def new_shape(self):
        self.current_shape = random.choice(self.shapes)
        self.current_x = 4
        self.current_y = 0

    def draw_grid(self):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.block_size, y * self.block_size, self.block_size, self.block_size)
                if self.grid[y][x] == 1:
                    pygame.draw.rect(self.screen, self.block_color, rect)
                pygame.draw.rect(self.screen, black, rect, 1)

    def draw_shape(self):
        for y, row in enumerate(self.current_shape):
            for x, cell in enumerate(row):
                if cell == 1:
                    rect = pygame.Rect((self.current_x + x) * self.block_size, (self.current_y + y) * self.block_size, self.block_size, self.block_size)
                    pygame.draw.rect(self.screen, self.block_color, rect)

    def run(self):
        running = True
        fall_time = 0
        fall_speed = 50  # Milliseconds
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Falling Logic
            delta_time = self.clock.get_rawtime()  # Time since last frame
            fall_time += delta_time
            if fall_time >= fall_speed and self.current_y < self.grid_size - len(self.current_shape):
                self.current_y += 1
                fall_time = 0

            # Draw Everything
            self.screen.fill(white)
            self.draw_grid()
            self.draw_shape()
            pygame.display.flip()
            self.clock.tick(60)


# Grid Dimensions
grid_size = 10
block_size = 40

block_color = (0, 255, 0)  # Green

game = Tetris(grid_size, block_size, block_color)
game.run()
pygame.quit()