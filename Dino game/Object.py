from parameters import *
import random


class Object:
    def __init__(self, x, y, width, image, speed):  # TODO: причем тут селф? Посмотри в байт оф питон, там было.
        self.x = x
        self.y = y
        self.width = width
        self.image = image
        self.speed = speed

    def move(self):
        if self.x >= -self.width:   # Пока он не исчез с экрана
            display.blit(self.image, (self.x, self.y))  # Передаем изображение в функцию
            # pygame.draw.rect(display, (224, 115, 67), (self.x, self.y, self.width, self.height))
            self.x -= self.speed    # Тупо из-за этого параметра увеличивается сложность игры
            return True
        else:
            self.x = display_width + 50 + random.randrange(-80, 60)
            return False

    def return_self(self, radius, y, width, image):
        self.x = radius
        self.y = y
        self.width = width
        self.image = image
        display.blit(self.image, (self.x, self.y))

