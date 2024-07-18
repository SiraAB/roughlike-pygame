import pygame
import os
from map import is_solid_tile, TILE_SIZE

class Character:
    def __init__(self, sprite_paths, position, speed, scale_factor=2.5):
        self.scale_factor = scale_factor
        self.sprites = {
            'idle': [self.load_and_scale(os.path.join(sprite_paths['idle'], file)) for file in sprite_paths['idle_files']],
            'run': [self.load_and_scale(os.path.join(sprite_paths['run'], file)) for file in sprite_paths['run_files']],
            'attack': [self.load_and_scale(os.path.join(sprite_paths['attack'], file)) for file in sprite_paths['attack_files']],
        }
        self.flipped_sprites = {
            'idle': [pygame.transform.flip(sprite, True, False) for sprite in self.sprites['idle']],
            'run': [pygame.transform.flip(sprite, True, False) for sprite in self.sprites['run']],
            'attack': [pygame.transform.flip(sprite, True, False) for sprite in self.sprites['attack']],
        }
        self.position = pygame.math.Vector2(position)
        self.speed = speed
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.state = 'idle'
        self.direction = pygame.math.Vector2(0, 0)
        self.facing_right = True
        self.attacking = False

        # Health and Stamina points
        self.max_health = 100
        self.health_points = self.max_health
        self.max_stamina = 100
        self.stamina_points = self.max_stamina
        self.stamina_regen_rate = 10

        # Define hitbox
        self.update_hitbox()

        self.attack_damage = 10
        self.attacking = False

    def load_and_scale(self, path):
        sprite = pygame.image.load(path).convert_alpha()
        size = sprite.get_size()
        scaled_sprite = pygame.transform.scale(sprite, (int(size[0] * self.scale_factor), int(size[1] * self.scale_factor)))
        return scaled_sprite

    def update_hitbox(self):
        sprite = self.sprites['idle'][0]
        self.hitbox = pygame.Rect(self.position.x, self.position.y, sprite.get_width(), sprite.get_height())

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.sprites[self.state]):
                self.current_frame = 0
                if self.state == 'attack':
                    self.attacking = False
                    self.state = 'idle' if self.direction.length() == 0 else 'run'
        if self.facing_right:
            return self.sprites[self.state][self.current_frame]
        else:
            return self.flipped_sprites[self.state][self.current_frame]

    def move(self, dt):
        if self.attacking:
            return

        keys = pygame.key.get_pressed()
        previous_state = self.state

        if keys[pygame.K_a]:
            self.direction.x = -1
            self.state = 'run'
            self.facing_right = False
        elif keys[pygame.K_d]:
            self.direction.x = 1
            self.state = 'run'
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_w]:
            self.direction.y = -1
            self.state = 'run'
        elif keys[pygame.K_s]:
            self.direction.y = 1
            self.state = 'run'
        else:
            self.direction.y = 0

        if self.direction.length() == 0:
            self.state = 'idle'
        
        if self.state != previous_state:
            self.current_frame = 0

        next_position = self.position + self.direction * self.speed * dt
        if not self.check_collision(next_position):
            self.position = next_position
            self.update_hitbox() 

        # Stamina regeneration
        self.stamina_points = min(self.stamina_points + self.stamina_regen_rate * dt, self.max_stamina)

    def check_collision(self, next_position):
        # Define the new hitbox position
        new_hitbox = self.hitbox.move(next_position - self.position)

        # Get the corners of the character's bounding box
        corners = [
            new_hitbox.topleft,
            new_hitbox.topright,
            new_hitbox.bottomleft,
            new_hitbox.bottomright,
        ]
        for corner in corners:
            grid_x = int(corner[0] // TILE_SIZE)
            grid_y = int(corner[1] // TILE_SIZE)
            if is_solid_tile(grid_x, grid_y):
                return True
        return False

    def attack(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.attacking and self.stamina_points >= 20:
            self.state = 'attack'
            self.current_frame = 0
            self.attacking = True
            self.stamina_points -= 20

    def update(self, dt):
        self.attack()
        self.move(dt)

    def draw(self, screen, dt):
        current_sprite = self.animate(dt)
        screen.blit(current_sprite, (self.position.x, self.position.y))

        # Draw hitbox for visualization
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

        # Draw health and stamina bars
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(10, 10, self.health_points, 10))
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(10, 25, self.stamina_points, 10))
