import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Пока что платформер")

sky_image = pygame.image.load("Sky.png").convert()
ground_image = pygame.image.load("ground.png").convert() 
sky_image = pygame.transform.scale(sky_image, (width, height // 2))
ground_image = pygame.transform.scale(ground_image, (width, height // 2))

enemy_size = 70  
enemy_sprite_sheet = pygame.image.load("pugame.png").convert_alpha() 
num_enemy_frames = 8 

enemies = []
enemy_y = height // 2 - enemy_size 

for _ in range(2):
    enemy_x = width
    enemy_speed = random.randint(3, 6)  
    enemies.append({"x": enemy_x, "y": enemy_y, "frame": 0, "speed": enemy_speed})


player_sprite_sheet = pygame.image.load("player.png").convert_alpha()
player_size = 70 
player_x = 50  
player_y = height // 2 - player_size 
player_speed_y = 0 
is_jumping = False  

num_player_frames = 5 
player_frame_index = 0 
animation_speed = 10  
frame_delay = 1000 // animation_speed  
last_update_player = pygame.time.get_ticks()  

def get_enemy_sprite(frame_index):
    """Возвращает кадр спрайта врага из спрайт-листа."""
    sprite_width = 32
    sprite_height = 32  
    x = (frame_index % num_enemy_frames) * sprite_width
    y = 3 * sprite_height 
    enemy_sprite = enemy_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
    enemy_sprite = pygame.transform.scale(enemy_sprite, (enemy_size, enemy_size)) 
    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False) 
    return enemy_sprite

def get_player_sprite(frame_index):
    """Возвращает кадр спрайта игрока из спрайт-листа."""
    sprite_width = 24
    sprite_height = 22 
    x = (frame_index % num_player_frames) * sprite_width
    y = 0 
    player_sprite = player_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
    player_sprite = pygame.transform.scale(player_sprite, (player_size, player_size)) 
    return player_sprite


fps = 60
clock = pygame.time.Clock()
last_update_enemy = pygame.time.get_ticks()  

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                is_jumping = True
                player_speed_y = -15  
                
    if is_jumping:
        player_y += player_speed_y
        player_speed_y += 1 
        if player_y >= height // 2 - player_size:  
            player_y = height // 2 - player_size
            is_jumping = False

    for enemy in enemies:
        enemy["x"] -= enemy["speed"] 
        if enemy["x"] < -enemy_size: 
            enemy["x"] = width 
            enemy["y"] = enemy_y 
            enemy["speed"] = random.randint(3, 6)

        now_enemy = pygame.time.get_ticks() 
        if now_enemy - last_update_enemy > frame_delay: 
            last_update_enemy = now_enemy  
            enemy["frame"] = (enemy["frame"] + 1) % num_enemy_frames

    now_player = pygame.time.get_ticks()
    if now_player - last_update_player > frame_delay:
        last_update_player = now_player
        player_frame_index = (player_frame_index + 1) % num_player_frames

    screen.blit(sky_image, (0, 0))
    screen.blit(ground_image, (0, height // 2))

    for enemy in enemies:
        enemy_sprite = get_enemy_sprite(enemy["frame"]) 
        screen.blit(enemy_sprite, (enemy["x"], enemy["y"])) 

    player_sprite_rendered = get_player_sprite(player_frame_index)
    screen.blit(player_sprite_rendered, (player_x, player_y))

    pygame.display.flip()
    clock.tick(fps)

