import pygame
import sys
from char_helper import *

def start_screen(screen):
    clock = pygame.time.Clock()
    sw, sh = screen.get_size()

    text_font = pygame.font.SysFont("Arial", 40, bold=True)
    text = text_font.render("Will you catch the train to Hamburg?", False, (200, 200, 200))
    text_rect = text.get_rect(center = (sw // 2, sh // 6))

    startscreen_img = pygame.image.load("media/pictures/startscreen.png").convert_alpha()
    startscreen = pygame.transform.scale(startscreen_img, (sw, sh))

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

def game_over_screen(screen):
    clock = pygame.time.Clock()
    sw, sh = screen.get_size()

    overscreen_img= pygame.image.load("media/pictures/game_over.png").convert_alpha()
    overscreen = pygame.transform.scale(overscreen_img, (sw, sh))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                return
        screen.fill((0, 0, 0))
        screen.blit(overscreen, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def win_screen(screen, score = None, time_taken = None):
    clock = pygame.time.Clock()
    sw, sh = screen.get_size()
    winscreen_img = pygame.image.load("media/pictures/win_screen.png").convert_alpha()
    winscreen = pygame.transform.scale(winscreen_img, (sw, sh))
    score_font = pygame.font.SysFont("Arial", 30, bold=True)

    lines = []
    if time_taken is not None:
        minutes, seconds = divmod(int(time_taken), 60)
        lines.append(f"Time taken: {minutes:02d}:{seconds:02d} minutes")
    if score is not None:
        lines.append(f"Lifes left: {score}")

    rendered_lines = []
    for i, line in enumerate(lines):
        rendered = score_font.render(line, True, (255, 255, 255))
        rect = rendered.get_rect(center=(sw // 2, sh - 80 + i * 35))
        rendered_lines.append((rendered, rect))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                return
        screen.fill((0, 0, 0))
        screen.blit(winscreen, (0, 0))
        for rendered, rect in rendered_lines:
            screen.blit(rendered, rect)
        pygame.display.flip()
        clock.tick(60)


def welcome_box(screen):
    sw, sh = screen.get_size()
    textbox_img = pygame.image.load("media/pictures/text_box.png").convert_alpha()
    text_box_img = pygame.transform.scale(textbox_img, (sw * 0.8, sh * 0.8))
    box_rect = text_box_img.get_rect(center=(sw // 2, sh // 2))
    screen.blit(text_box_img, box_rect)

    welcome_font = pygame.font.SysFont("Arial", 40, bold=True)
    message = (
        "Good morning!\n"
        "It's time to go to Hamburg for class -\n"
        "you need to hurry!\n"
        "But first:\n"
        "get some food to get your health up\n"
        "(top left of screen)")
    lines = message.split("\n")
    line_height = welcome_font.get_linesize()
    total_height = line_height * len(lines)
    start_y = box_rect.centery - total_height // 2

    for i, line in enumerate(lines):
        rendered = welcome_font.render(line, True, (200, 200, 200))
        line_rect = rendered.get_rect(
            center=(box_rect.centerx, start_y + i * line_height + line_height // 2))
        screen.blit(rendered, line_rect)

