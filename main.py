import pygame
import sys
import random

class Game:
    def __init__(self):
        pygame.init()

        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Пока что платформер")

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.game_over = False
        self.font = pygame.font.Font(None, 50)

        self.sky_image = pygame.image.load("Sky.png").convert()
        self.ground_image = pygame.image.load("ground.png").convert()
        self.sky_image = pygame.transform.scale(self.sky_image, (self.width, self.height // 2))
        self.ground_image = pygame.transform.scale(self.ground_image, (self.width, self.height // 2))

        self.num_enemies = 2 
        self.enemies = []
        self.enemy_spawn_rate = 3000 
        self.last_enemy_spawn = pygame.time.get_ticks()

        self.player = Player(self.width, self.height)

        self.num_birds = 3
        self.birds = []
        for i in range(self.num_birds):
            bird_x = self.width + random.randint(100, 300)
            is_active = False if i > 0 else True
            self.birds.append(Bird(bird_x, self.height // 3, is_active))

        self.score = 0
        self.time_since_last_score = 0
        self.score_interval = 1000

        self.fps = 60
        self.clock = pygame.time.Clock()

    def reset_game(self):
        self.game_over = False
        self.enemies = []
        self.birds = []
        for i in range(self.num_birds):
            bird_x = self.width + random.randint(100, 300)
            is_active = False if i > 0 else True
            self.birds.append(Bird(bird_x, self.height // 3, is_active))

        self.score = 0
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.time_since_last_score = 0
        self.player.reset()

    def can_spawn_enemy(self, x):
        """Checks if spawning an enemy at x would cause overlap."""
        for enemy in self.enemies:
            if abs(x - enemy.x) < 200:
                return False
        return True
    
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.game_over:
                    self.reset_game()
                else:
                    if event.key == pygame.K_SPACE and not self.player.is_jumping:
                        self.player.jump()
                    if event.key == pygame.K_DOWN:
                        self.player.crouch(True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.player.crouch(False)
    
    def update(self):
        delta_time = self.clock.get_time()  

        if not self.game_over:
            self.player.update()

            now = pygame.time.get_ticks()
            if now - self.last_enemy_spawn > self.enemy_spawn_rate and len(self.enemies) < self.num_enemies:
                self.last_enemy_spawn = now
                enemy_x = self.width + random.randint(100,300) 
                if self.can_spawn_enemy(enemy_x):
                    enemy = Enemy(enemy_x, self.height // 2 - 70)  
                    self.enemies.append(enemy)

            for enemy in self.enemies[:]:
                enemy.update()
                if enemy.x < -enemy.size:
                    self.enemies.remove(enemy)

            for bird in self.birds:
                bird.update()
                if bird.x < -50:
                    bird.is_active = False
                    bird.x = self.width + random.randint(100, 300)

                    next_active_bird = random.randint(0, self.num_birds - 1)
                    self.birds[next_active_bird].is_active = True
                    self.birds[next_active_bird].x = self.width + random.randint(100, 300)

            self.time_since_last_score += delta_time
            if self.time_since_last_score >= self.score_interval:
                self.score += 1
                self.time_since_last_score -= self.score_interval

            player_rect = self.player.get_rect()

            for enemy in self.enemies:
                enemy_rect = enemy.get_rect()

                if player_rect.colliderect(enemy_rect):
                    self.game_over = True
                    break

            for bird in self.birds:
                if bird.is_active:
                    bird_rect = bird.get_rect()
                    if player_rect.colliderect(bird_rect):
                        self.game_over = True
                        break

    def draw(self):
        self.screen.blit(self.sky_image, (0, 0))
        self.screen.blit(self.ground_image, (0, self.height // 2))

        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bird in self.birds:
            if bird.is_active:
                bird.draw(self.screen)

        self.player.draw(self.screen)

        if self.game_over:
            text = self.font.render("Игра окончена! Счет: " + str(self.score), True, self.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            self.screen.blit(text, text_rect)

            text = self.font.render("Нажмите любую клавишу для перезапуска", True, self.WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + 50))
            self.screen.blit(text, text_rect)
        else:
            score_text = self.font.render("Счет: " + str(self.score), True, self.WHITE)
            self.screen.blit(score_text, (10, 10))

        pygame.display.flip()


    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

class Player:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.player_sprite_sheet = pygame.image.load("player.png").convert_alpha()
        self.player_size = 70
        self.x = 50
        self.y = self.height // 2 - self.player_size
        self.speed_y = 0
        self.is_jumping = False
        self.is_crouching = False
        self.num_player_frames = 5
        self.num_player_crouch_frames = 6
        self.frame_index = 0
        self.crouch_frame_index = 0
        self.animation_speed = 10
        self.frame_delay = 1000 // self.animation_speed
        self.last_update = pygame.time.get_ticks()

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed_y = -15

    def crouch(self, is_crouching):
        self.is_crouching = is_crouching

    def update(self):
        if self.is_jumping:
            self.y += self.speed_y
            self.speed_y += 1
            if self.y >= self.height // 2 - self.player_size:
                self.y = self.height // 2 - self.player_size
                self.is_jumping = False

        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            if not self.is_crouching:
                self.frame_index = (self.frame_index + 1) % self.num_player_frames
            else:
                self.crouch_frame_index = (self.crouch_frame_index + 1) % self.num_player_crouch_frames

    def get_sprite(self):
        return self.get_player_sprite(self.crouch_frame_index if self.is_crouching else self.frame_index, self.is_crouching)

    def get_rect(self):
        player_rect_y = self.y
        player_rect_height = self.player_size
        if self.is_crouching:
            player_rect_y += self.player_size // 2
            player_rect_height = self.player_size // 2

        return pygame.Rect(self.x + self.player_size // 4, player_rect_y, self.player_size // 2, player_rect_height // 2)

    def draw(self, screen):
        player_sprite_rendered = self.get_sprite()
        screen.blit(player_sprite_rendered, (self.x, self.y))

    def get_player_sprite(self, frame_index, is_crouching):
        sprite_width = 24
        sprite_height = 22
        if not is_crouching:
            x = (frame_index % self.num_player_frames) * sprite_width
            y = 0
        else:
            x = ((frame_index + 17) % 30) * sprite_width
            y = 0
        player_sprite = self.player_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
        player_sprite = pygame.transform.scale(player_sprite, (self.player_size, self.player_size))
        return player_sprite

    def reset(self):
        self.y = self.height // 2 - self.player_size
        self.speed_y = 0
        self.is_jumping = False
        self.is_crouching = False
        self.frame_index = 0
        self.crouch_frame_index = 0
        self.last_update = pygame.time.get_ticks()

class Bird:
    def __init__(self, x, y, is_active):
        self.x = x
        self.y = y
        self.is_active = is_active
        self.bird_sprite_sheet = pygame.image.load("bird.png").convert_alpha()
        self.num_bird_frames = 4
        self.frame = 0
        self.bird_size = 50
        self.animation_speed = 10
        self.frame_delay = 1000 // self.animation_speed
        self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.is_active:
            self.x -= 5

            now = pygame.time.get_ticks()
            if now - self.last_update > self.frame_delay:
                self.last_update = now
                self.frame = (self.frame + 1) % self.num_bird_frames

    def get_sprite(self):
        sprite_width = 32
        sprite_height = 32
        x = (self.frame % self.num_bird_frames) * sprite_width
        y = 0
        bird_sprite = self.bird_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
        bird_sprite = pygame.transform.scale(bird_sprite, (self.bird_size, self.bird_size))
        bird_sprite = pygame.transform.flip(bird_sprite, True, False)
        return bird_sprite

    def get_rect(self):
        return pygame.Rect(self.x + self.bird_size//4, self.y + self.bird_size//4, self.bird_size // 2, self.bird_size//2 )

    def draw(self, screen):
        bird_sprite = self.get_sprite()
        screen.blit(bird_sprite, (self.x, self.y))


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 70
        self.speed = random.randint(3, 6)  
        self.frame = 0
        self.enemy_sprite_sheet = pygame.image.load("pugame.png").convert_alpha()
        self.num_enemy_frames = 8
        self.animation_speed = 10  
        self.frame_delay = 1000 // self.animation_speed
        self.last_update = pygame.time.get_ticks()

    def update(self):
        self.x -= self.speed 
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_delay:
            self.last_update = now
            self.frame = (self.frame + 1) % self.num_enemy_frames

    def get_sprite(self):
        sprite_width = 32
        sprite_height = 32
        x = (self.frame % self.num_enemy_frames) * sprite_width
        y = 3 * sprite_height
        enemy_sprite = self.enemy_sprite_sheet.subsurface((x, y, sprite_width, sprite_height))
        enemy_sprite = pygame.transform.scale(enemy_sprite, (self.size, self.size))
        enemy_sprite = pygame.transform.flip(enemy_sprite, True, False)
        return enemy_sprite

    def get_rect(self):
        return pygame.Rect(self.x + self.size // 4, self.y + self.size // 4, self.size // 2, self.size // 2)

    def draw(self, screen):
        enemy_sprite = self.get_sprite()
        screen.blit(enemy_sprite, (self.x, self.y))


if __name__ == "__main__":
    game = Game()
    game.run()
