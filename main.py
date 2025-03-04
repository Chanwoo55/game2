import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Пока что платформер")

sky_image = pygame.image.load("Sky.png")
ground_image = pygame.image.load("ground.png")

sky_image = pygame.transform.scale(sky_image, (width, height // 2))
ground_image = pygame.transform.scale(ground_image, (width, height // 2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(sky_image, (0, 0)) 
    screen.blit(ground_image, (0, height // 2))  

    font = pygame.font.Font(None, 74)
    text = font.render("Пока что платформер", True, (255, 255, 255))
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    pygame.display.flip() 
