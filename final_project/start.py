#make racoon skeleton head
import pygame
import sys
from char_helper import *

pygame.display.init()
pygame.init()

def start_screen(screen):
    clock = pygame.time.Clock()
    sw, sh = screen.get_size()

    text_font = pygame.font.SysFont("Arial", 40, bold=True)
    text = text_font.render("Will you catch the train to Hamburg?", False, (200, 200, 200))
    text_rect = text.get_rect(center = (sw // 2, sh // 6))

    startscreen = pygame.image.load("pictures/startscreen.png").convert_alpha()
    startscreen = pygame.transform.scale(startscreen, (sw, sh))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                return
        screen.fill((0, 0, 0))
        screen.blit(startscreen, (0, 0))
        screen.blit(text, text_rect)
        pygame.display.flip()
        clock.tick(60)

