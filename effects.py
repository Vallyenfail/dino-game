from parameters import *
import pygame


def print_text(message, x, y, font_color=(0, 0, 0), font_type='Damn noisy kids.ttf', font_size=30): # TODO как работает?
    font_type = pygame.font.Font(font_type, font_size)
    text = font_type.render(message, True, font_color)  # Код для вывода текста на экран
    display.blit(text, (x, y))
