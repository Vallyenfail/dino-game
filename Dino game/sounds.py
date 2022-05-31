import pygame

pygame.init()

jump_sound = pygame.mixer.Sound('Music/Jump.mp3')
fall_sound = pygame.mixer.Sound('Music/Explosion.mp3')
crash_sound = pygame.mixer.Sound('Music/Ouch.wav')
heart_plus_sound = pygame.mixer.Sound('Music/Pickup.wav')
pygame.mixer.Sound.set_volume(heart_plus_sound, 0.3)
click_sound = pygame.mixer.Sound('Music/Click.wav')
shot_sound = pygame.mixer.Sound('Music/Pew.wav')