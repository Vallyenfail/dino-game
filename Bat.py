# ============================================
# ФАЙЛ: Bat.py (новый файл)
# ============================================

import random
import pygame
from sounds import *
from parameters import *


class Bat:
    '''Класс летучей мыши - нового врага'''

    def __init__(self, away_y):
        self.x = random.randrange(700, 800)  # Начинаем справа
        self.y = random.randrange(200, 400)  # Случайная высота
        self.ay = away_y
        self.width = 40
        self.height = 40
        self.speed_x = 4  # Скорость по горизонтали
        self.speed_y = 2  # Скорость по вертикали
        self.direction_y = 1  # Направление по Y (1 = вниз, -1 = вверх)
        self.img_cnt = 0
        self.come = True
        self.zigzag_counter = 0  # Счетчик для зигзага

    def draw(self, bat_images):
        '''Рисует летучую мышь с анимацией'''
        if self.img_cnt == len(bat_images) * 5:
            self.img_cnt = 0

        display.blit(bat_images[self.img_cnt // 5], (self.x, self.y))
        self.img_cnt += 1

        if self.come:
            return 1
        return 0

    def move_zigzag(self):
        '''Движение зигзагом - особенность летучей мыши'''
        # Двигаемся влево
        self.x -= self.speed_x

        # Зигзаг по вертикали
        self.y += self.speed_y * self.direction_y
        self.zigzag_counter += 1

        # Меняем направление каждые 30 кадров
        if self.zigzag_counter >= 30:
            self.direction_y *= -1  # Меняем направление
            self.zigzag_counter = 0

        # Ограничиваем по Y
        if self.y < 150:
            self.y = 150
            self.direction_y = 1
        elif self.y > 400:
            self.y = 400
            self.direction_y = -1

        # Проверяем, ушла ли за экран
        if self.x < -self.width:
            return False
        return True

    def kill_bat(self, bullet):
        '''Проверка попадания пули'''
        if self.x <= bullet.x <= self.x + self.width:
            if self.y <= bullet.y <= self.y + self.height:
                return True
        return False

    def reset(self):
        '''Возвращает летучую мышь в начальную позицию'''
        self.x = random.randrange(700, 800)
        self.y = random.randrange(200, 400)
        self.come = True
        self.zigzag_counter = 0
        self.direction_y = random.choice([-1, 1])
