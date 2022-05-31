import pygame

pygame.init()

land = pygame.image.load(r'Effects and background/Land2.jpg')# Загрузили землю

cactus_img = [pygame.image.load('Objects/Cactus1.jpg'), pygame.image.load('Objects/Cactus2.jpg'),
              pygame.image.load('Objects/Cactus3.jpg')]

stone_img = [pygame.image.load('Objects/Rock1.jpg'), pygame.image.load('Objects/Rock2.jpg')]

cloud_img = [pygame.image.load('Objects/Cloud1.jpg'), pygame.image.load('Objects/Cloud2.jpg')]

dino_img = [pygame.image.load('Dino/Dino1.jpg'), pygame.image.load('Dino/Dino3.jpg'),
            pygame.image.load('Dino/Dino2.jpg'), pygame.image.load('Dino/Dino_jump.jpg'),
            pygame.image.load('Dino/Dino_jump2.jpg')]

bird_img = [pygame.image.load('Bird/Bird1.png'), pygame.image.load('Bird/Bird2.png'),
            pygame.image.load('Bird/Bird3.png'), pygame.image.load('Bird/Bird4.png'),
            pygame.image.load('Bird/Bird5.png')]

health_img = pygame.image.load('Objects/heart.png')
# health_img = pygame.transform.scale()  #Трансформация

bullet_img = pygame.image.load('Effects and background/Shot.png')
bullet_img = pygame.transform.scale(bullet_img, (30, 9))

icon = pygame.image.load('Effects and background/CursorAttack.png')


def set_theme(num):
    global land
    land = pygame.image.load(r'Effects and background/Land{}.jpg'.format(num))
