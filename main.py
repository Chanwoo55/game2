import pygame
import sys
import random

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Пока что платформер")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0) 

game_over = False
font = pygame.font.Font(None, 50)

sky_image = pygame.image.load("Sky.png").convert()
ground_image = pygame.image.load("ground.png").convert()
sky_image = pygame.transform.scale(sky_image, (width, height // 2))
ground_image = pygame.transform.scale(ground_image, (width, height // 2))

enemy_size = 70
enemy_sprite_sheet = pygame.image.load("pugame.png").convert_alpha()
num_enemy_frames = 8
enemies = []
enemy_y = height // 2 - enemy_size
enemy_spawn_rate = 3000  # Increased spawn rate (milliseconds) - now 3 seconds
last_enemy_spawn = pygame.time.get_ticks()
num_enemies = 2  # Limit to 2 enemies

player_sprite_sheet = pygame.image.load("player.png").convert_alpha()
player_size = 70
player_x = 50
player_y = height // 2 - player_size
player_speed_y = 0
is_jumping = False
is_crouching = False
num_player_frames = 5
num_player_crouch_frames = 6
player_frame_index = 0
crouch_frame_index = 0
animation_speed = 10
frame_delay = 1000 // animation_speed
last_update_player = pygame.time.get_ticks()

bird_sprite_sheet = pygame.image.load("bird.png").convert_alpha()
num_bird_frames = 4
birds = []
bird_y_level = height // 3
num_birds = 3
bird_size = 50

for i in range(num_birds):
    bird_x = width + random.randint(100, 300)
    is_active = False if i > 0 else True
    birds.append({"x": bird_x, "y": bird_y_level, "frame": 0, "is_active": is_active})

current_bird_index = 0

score = 0
time_since_last_score = 0
score_interval = 1000 

def get_enemy_sprite(frame_index):
    sprite_width = 32
    sprite_height = 32
    x = (frame_index % num_enemy_frames) * sprite_width
    y = 3 * sprite_height
    enemy_sprite = enemy_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
    enemy_sprite = pygame.transform.scale(enemy_sprite, (enemy_size, enemy_size))
    enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
    return enemy_sprite


def get_player_sprite(frame_index, is_crouching):
    sprite_width = 24
    sprite_height = 22
    if not is_crouching:
        x = (frame_index % num_player_frames) * sprite_width
        y = 0
    else:
        x = ((frame_index + 17) % 30) * sprite_width
        y = 0
    player_sprite = player_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
    player_sprite = pygame.transform.scale(player_sprite, (player_size, player_size))
    return player_sprite


def get_bird_sprite(frame_index):
    sprite_width = 32
    sprite_height = 32
    x = (frame_index % num_bird_frames) * sprite_width
    y = 0
    bird_sprite = bird_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
    bird_sprite = pygame.transform.scale(bird_sprite, (bird_size, bird_size))
    bird_sprite = pygame.transform.flip(bird_sprite, True, False)
    return bird_sprite


def reset_game():
    global game_over, enemies, score, last_enemy_spawn, time_since_last_score, birds
    game_over = False
    enemies = []
    birds = []
    for i in range(num_birds):
        bird_x = width + random.randint(100, 300)
        is_active = False if i > 0 else True
        birds.append({"x": bird_x, "y": bird_y_level, "frame": 0, "is_active": is_active})


    score = 0
    last_enemy_spawn = pygame.time.get_ticks()
    time_since_last_score = 0

def can_spawn_enemy(x):
  """Checks if spawning an enemy at x would cause overlap."""
  for enemy in enemies:
    if abs(x - enemy["x"]) < 200: 
      return False
  return True

fps = 60
clock = pygame.time.Clock()
last_update_enemy = pygame.time.get_ticks()
last_update_bird = pygame.time.get_ticks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if game_over:
                reset_game()
            else:
                if event.key == pygame.K_SPACE and not is_jumping:
                    is_jumping = True
                    player_speed_y = -15
                if event.key == pygame.K_DOWN:
                    is_crouching = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                is_crouching = False

    delta_time = clock.get_time()  

    if not game_over:
        if is_jumping:
            player_y += player_speed_y
            player_speed_y += 1
            if player_y >= height // 2 - player_size:
                player_y = height // 2 - player_size
                is_jumping = False

        now = pygame.time.get_ticks()
        if now - last_enemy_spawn > enemy_spawn_rate and len(enemies) < num_enemies:
            last_enemy_spawn = now
            enemy_x = width + random.randint(100,300) 
            if can_spawn_enemy(enemy_x):
                enemy_speed = random.randint(3, 6)
                enemy_frame = 0
                enemies.append({"x": enemy_x, "y": enemy_y, "frame": enemy_frame, "speed": enemy_speed})
        for enemy in enemies:
            enemy["x"] -= enemy["speed"]
            if enemy["x"] < -enemy_size:
                enemies.remove(enemy)  
                last_enemy_spawn = now - enemy_spawn_rate 
                break


            now_enemy = pygame.time.get_ticks()
            if now_enemy - last_update_enemy > frame_delay:
                last_update_enemy = now_enemy
                enemy["frame"] = (enemy["frame"] + 1) % num_enemy_frames

        for i, bird in enumerate(birds):
            if bird["is_active"]:
                bird["x"] -= 5

                if bird["x"] < -50:
                    bird["is_active"] = False
                    bird["x"] = width + random.randint(100, 300)

                    next_active_bird = random.randint(0, num_birds - 1)
                    birds[next_active_bird]["is_active"] = True
                    birds[next_active_bird]["x"] = width + random.randint(100, 300)

                now_bird = pygame.time.get_ticks()
                if now_bird - last_update_bird > frame_delay:
                    last_update_bird = now_bird
                    bird["frame"] = (bird["frame"] + 1) % num_bird_frames

        now_player = pygame.time.get_ticks()
        if now_player - last_update_player > frame_delay:
            last_update_player = now_player
            if not is_crouching:
                player_frame_index = (player_frame_index + 1) % num_player_frames
            else:
                crouch_frame_index = (crouch_frame_index + 1) % num_player_crouch_frames

        time_since_last_score += delta_time
        if time_since_last_score >= score_interval:
            score += 1
            time_since_last_score -= score_interval

        player_rect_y = player_y
        player_rect_height = player_size
        if is_crouching:
            player_rect_y += player_size // 2
            player_rect_height = player_size // 2

        player_rect = pygame.Rect(player_x + player_size // 4, player_rect_y, player_size // 2, player_rect_height // 2)

        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy["x"] + enemy_size // 4, enemy["y"] + enemy_size // 4, enemy_size // 2, enemy_size // 2)  

            if player_rect.colliderect(enemy_rect):
                game_over = True
                break

        for bird in birds:
            if bird["is_active"]:
                bird_rect = pygame.Rect(bird["x"] + bird_size//4, bird["y"] + bird_size//4, bird_size // 2, bird_size//2 )
                if player_rect.colliderect(bird_rect):
                    game_over = True
                    break
    screen.blit(sky_image, (0, 0))
    screen.blit(ground_image, (0, height // 2))

    for enemy in enemies:
        enemy_sprite = get_enemy_sprite(enemy["frame"])
        screen.blit(enemy_sprite, (enemy["x"], enemy["y"]))

        enemy_rect = pygame.Rect(enemy["x"] + enemy_size // 4, enemy["y"] + enemy_size // 4, enemy_size // 2, enemy_size // 2)
        pygame.draw.rect(screen, RED, enemy_rect, 2)

    for bird in birds:
        if bird["is_active"]:
            bird_sprite = get_bird_sprite(bird["frame"])
            screen.blit(bird_sprite, (bird["x"], bird["y"]))

            bird_rect = pygame.Rect(bird["x"] + bird_size//4, bird["y"] + bird_size//4, bird_size // 2, bird_size//2 )
            pygame.draw.rect(screen, RED, bird_rect, 2)

    player_sprite_rendered = get_player_sprite(crouch_frame_index if is_crouching else player_frame_index, is_crouching)

    screen.blit(player_sprite_rendered, (player_x, player_y))

    player_rect_y = player_y  
    if is_crouching:
        player_rect_y += player_size // 2 
    player_rect = pygame.Rect(player_x + player_size // 4, player_rect_y, player_size // 2, player_rect_height)
    pygame.draw.rect(screen, RED, player_rect, 2)


    if game_over:
        text = font.render("Игра окончена! Счет: " + str(score), True, WHITE)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

        text = font.render("Нажмите любую клавишу для перезапуска", True, WHITE)
        text_rect = text.get_rect(center=(width // 2, height // 2 + 50))
        screen.blit(text, text_rect)
    else:
        score_text = font.render("Счет: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(fps)
