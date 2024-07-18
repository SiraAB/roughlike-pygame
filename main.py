import pygame
import sys

from map import draw_map, map_data
from mainchar import Character
from monster import Monster

# Initialize Pygame
pygame.init()

# Screen Dimensions
SCREEN_WIDTH = 1270
SCREEN_HEIGHT = 800

# Sprite paths MainChar
mainchar_sprite_paths = {
    'idle': 'RawAsset/MainChar/idle',
    'idle_files': ['Warrior_Idle_1.png', 'Warrior_Idle_2.png', 'Warrior_Idle_3.png',
                    'Warrior_Idle_4.png', 'Warrior_Idle_5.png', 'Warrior_Idle_6.png'],
    'run': 'RawAsset/MainChar/run',
    'run_files': ['Warrior_Run_1.png', 'Warrior_Run_2.png', 'Warrior_Run_3.png', 'Warrior_Run_4.png',
                   'Warrior_Run_5.png', 'Warrior_Run_6.png', 'Warrior_Run_7.png', 'Warrior_Run_8.png'],
    'attack': 'RawAsset/MainChar/attack',
    'attack_files': ['Warrior_Attack_1.png', 'Warrior_Attack_2.png', 'Warrior_Attack_3.png', 'Warrior_Attack_4.png', 
                     'Warrior_Attack_5.png', 'Warrior_Attack_6.png', 'Warrior_Attack_7.png', 'Warrior_Attack_8.png', 
                     'Warrior_Attack_9.png', 'Warrior_Attack_10.png', 'Warrior_Attack_11.png', 'Warrior_Attack_12.png',]
}

# Sprite paths Monster
monster_sprite_paths = {
    'idle': 'RawAsset/Monster1/idle',
    'idle_files': ['slime-idle-0.png', 'slime-idle-1.png', 'slime-idle-2.png', 'slime-idle-3.png'],

    'run': 'RawAsset/Monster1/run',
    'run_files': ['slime-move-0.png', 'slime-move-1.png', 'slime-move-2.png', 'slime-move-3.png'],

    'attack': 'RawAsset/Monster1/attack',
    'attack_files': ['slime-attack-0.png', 'slime-attack-1.png', 'slime-attack-2.png', 'slime-attack-3.png', 'slime-attack-4.png'],

    'hurt': 'RawAsset/Monster1/hurt',
    'hurt_files': ['slime-hurt-0.png', 'slime-hurt-1.png', 'slime-hurt-2.png', 'slime-hurt-3.png'],

    'die': 'RawAsset/Monster1/die',
    'die_files': ['slime-die-0.png', 'slime-die-1.png', 'slime-die-2.png', 'slime-die-3.png']
}

# Screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

mainchar = Character(mainchar_sprite_paths, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), 100)
monster = Monster(monster_sprite_paths, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2), 50)

# Title and Icon
pygame.display.set_caption("Roughlike")

# Main Loop
running = True
clock = pygame.time.Clock()

while running:
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    draw_map(screen, map_data)
    
    # Update and draw the character
    mainchar.update(dt)
    mainchar.draw(screen, dt)

    # Update and draw the monster
    monster.update(dt)
    monster.draw(screen, dt)

    # Check for attack collision
    if mainchar.attacking and monster.hitbox.colliderect(mainchar.hitbox):
        monster.take_damage(mainchar.attack_damage)
    
    # Update and draw the monster if it's still alive
    if monster.alive:
        monster.update(dt)
        monster.draw(screen, dt)

        # Check for attack collision
        if mainchar.attacking and monster.hitbox.colliderect(mainchar.hitbox):
            monster.take_damage(mainchar.attack_damage)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
