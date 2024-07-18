import pygame
import os

class Monster:
    def __init__(self, sprite_paths, position, speed):
        self.sprites = {
            'idle': [self.load_and_scale(os.path.join(sprite_paths['idle'], file)) for file in sprite_paths['idle_files']],
            'run': [self.load_and_scale(os.path.join(sprite_paths['run'], file)) for file in sprite_paths['run_files']],
            'attack': [self.load_and_scale(os.path.join(sprite_paths['attack'], file)) for file in sprite_paths['attack_files']],
            'hurt': [self.load_and_scale(os.path.join(sprite_paths['hurt'], file)) for file in sprite_paths['hurt_files']],
            'die': [self.load_and_scale(os.path.join(sprite_paths['die'], file)) for file in sprite_paths['die_files']]
        }
        self.position = pygame.math.Vector2(position)
        self.speed = speed
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        self.state = 'idle'
        self.direction = pygame.math.Vector2(0, 0)
        self.facing_right = True
        self.hitbox = pygame.Rect(self.position.x, self.position.y, 50, 50)
        self.health = 100
        self.alive = True

    def load_and_scale(self, path):
        sprite = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(sprite, (50, 50))  # Scale as needed

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1
            if self.current_frame >= len(self.sprites[self.state]):
                if self.state == 'die':
                    self.alive = False
                self.current_frame = 0  # Reset frame to loop or to stop at the last frame
        if self.facing_right:
            return self.sprites[self.state][self.current_frame]
        else:
            return pygame.transform.flip(self.sprites[self.state][self.current_frame], True, False)

    def move(self, dt):
        if self.state not in ['die', 'hurt']:
            self.position += self.direction * self.speed * dt

    def update(self, dt):
        if self.alive:
            self.move(dt)
        self.hitbox.topleft = (self.position.x, self.position.y)

    def draw(self, screen, dt):
        if self.alive:
            current_sprite = self.animate(dt)
            screen.blit(current_sprite, (self.position.x, self.position.y))
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)

    def take_damage(self, damage):
        if self.alive:
            self.health -= damage
            if self.health <= 0:
                self.health = 0
                self.state = 'die'
                self.current_frame = 0
            else:
                self.state = 'hurt'
                self.current_frame = 0
