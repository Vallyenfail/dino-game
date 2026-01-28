"""
Класс Bat - новый тип врага (Летучая мышь)

Задание 3.5: Добавление нового типа врага

Особенности летучей мыши:
- Летает зигзагом (меняет направление по Y)
- Не стреляет (проще чем птицы)
- Движется справа налево
- Дает очки при убийстве
"""

import random

from sounds import *
from parameters import *


class Bat:
    """Летучая мышь - враг который летает зигзагом"""
    
    def __init__(self):
        """Инициализация летучей мыши"""
        self.x = random.randrange(display_width, display_width + 100)  # Начинаем справа
        self.y = random.randrange(150, 350)  # Случайная высота
        self.width = 40
        self.height = 40
        self.speed_x = 4  # Скорость по горизонтали
        self.speed_y = 2  # Скорость зигзага
        self.direction_y = random.choice([-1, 1])  # Направление (вверх/вниз)
        self.img_cnt = 0
        self.zigzag_counter = 0
        self.alive = True
    
    def draw(self, bat_images):
        """
        Рисует летучую мышь с анимацией
        
        Args:
            bat_images: Список изображений для анимации
        """
        if not self.alive:
            return
        
        # Анимация (переключение кадров)
        if self.img_cnt == len(bat_images) * 5:
            self.img_cnt = 0
        
        # Отрисовка
        display.blit(bat_images[self.img_cnt // 5], (self.x, self.y))
        self.img_cnt += 1
    
    def move_zigzag(self):
        """
        Движение зигзагом - особенность летучей мыши
        
        Returns:
            bool: True если на экране, False если улетела
        """
        if not self.alive:
            return False
        
        # Движение влево
        self.x -= self.speed_x
        
        # Зигзаг по вертикали
        self.y += self.speed_y * self.direction_y
        self.zigzag_counter += 1
        
        # Меняем направление каждые 30 кадров
        if self.zigzag_counter >= 30:
            self.direction_y *= -1
            self.zigzag_counter = 0
        
        # Ограничиваем по Y чтобы не улетела за края
        if self.y < 100:
            self.y = 100
            self.direction_y = 1
        elif self.y > 400:
            self.y = 400
            self.direction_y = -1
        
        # Проверяем не улетела ли за левый край
        if self.x < -self.width:
            return False
        
        return True
    
    def kill_bat(self, bullet):
        """
        Проверка попадания пули в летучую мышь
        
        Args:
            bullet: Объект пули
        
        Returns:
            bool: True если попали, False если промах
        """
        if not self.alive:
            return False
        
        # Проверка столкновения
        if self.x <= bullet.x <= self.x + self.width:
            if self.y <= bullet.y <= self.y + self.height:
                self.alive = False
                # Звук взрыва при убийстве
                pygame.mixer.Sound.play(explosion_sound)
                return True
        
        return False
    
    def reset(self):
        """Возвращает летучую мышь в начальную позицию"""
        self.x = random.randrange(display_width, display_width + 100)
        self.y = random.randrange(150, 350)
        self.alive = True
        self.zigzag_counter = 0
        self.direction_y = random.choice([-1, 1])
    
    def check_collision_with_player(self, player_x, player_y, player_width, player_height):
        """
        Проверка столкновения с игроком
        
        Args:
            player_x, player_y: Позиция игрока
            player_width, player_height: Размер игрока
        
        Returns:
            bool: True если столкнулись
        """
        if not self.alive:
            return False
        
        # Простая проверка пересечения прямоугольников
        if (self.x < player_x + player_width and
            self.x + self.width > player_x and
            self.y < player_y + player_height and
            self.y + self.height > player_y):
            return True
        
        return False
