import pygame

# Grid dimensions
GRID_WIDTH = 32
GRID_HEIGHT = 20
TILE_SIZE = 40

# Creating a new map (0 - floor, 1 - wall)
map_data = [
    [1] * GRID_WIDTH,
    *[[1] + [0] * (GRID_WIDTH - 2) + [1] for _ in range(GRID_HEIGHT - 2)],
    [1] * GRID_WIDTH,
]

floor_color = (50, 50, 50)
wall_color = (200, 200, 200)

def draw_map(screen, map_data):
    for y, row in enumerate(map_data):
        for x, tile in enumerate(row):
            if tile == 0:
                color = floor_color
            elif tile == 1:
                color = wall_color
            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def is_solid_tile(grid_x, grid_y):
    if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
        return map_data[grid_y][grid_x] == 1
    return False