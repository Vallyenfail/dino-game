"""
Решение для Задания 3.5: Добавление нового типа врага (Летучая мышь)

Этот файл показывает, как создать нового врага по образцу Bird.py
"""

# ============================================
# ФАЙЛ: Bat.py (новый файл)
# ============================================

"""
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
"""

# ============================================
# ФАЙЛ: images.py (добавить загрузку спрайтов)
# ============================================

"""
# В конец файла images.py добавить:

# Загружаем летучих мышей (нужно создать папку Bat/ с картинками)
bat_img = [
    pygame.image.load('Bat/Bat1.png'),
    pygame.image.load('Bat/Bat2.png'),
    pygame.image.load('Bat/Bat3.png')
]

# Если картинок нет, можно временно использовать картинки птиц:
# bat_img = bird_img
"""

# ============================================
# ФАЙЛ: game.py (добавить летучих мышей в игру)
# ============================================

"""
В функции run_game() класса Game:

1. Импортировать класс в начале файла:
   from Bat import *

2. Создать летучих мышей после создания птиц (строка ~147):

   bird1 = Bird(-80)
   bird2 = Bird(-40)
   all_birds = [bird1, bird2]
   
   # НОВЫЙ КОД: Создаем летучих мышей
   bat1 = Bat(0)
   bat2 = Bat(0)
   all_bats = [bat1, bat2]

3. В игровом цикле добавить отрисовку и движение летучих мышей:

   # После строки с draw_birds (примерно строка 225):
   self.draw_birds(all_birds)
   self.check_birds_dmg(all_mouse_bullets, all_birds)
   
   # НОВЫЙ КОД: Рисуем и двигаем летучих мышей
   self.draw_bats(all_bats, all_mouse_bullets)
   
4. Добавить новые методы в класс Game:

   def draw_bats(self, bats, bullets):
       '''Рисует летучих мышей и проверяет столкновения'''
       from images import bat_img  # Импортируем картинки
       
       for bat in bats:
           bat.draw(bat_img)
           
           # Двигаем зигзагом
           if not bat.move_zigzag():
               bat.reset()  # Возвращаем на старт
           
           # Проверяем попадания пуль
           for bullet in bullets:
               if bat.kill_bat(bullet):
                   bat.reset()
                   bullets.remove(bullet)
                   # Можно добавить очки за убийство
                   self.scores += 5
                   break
"""

# ============================================
# СОЗДАНИЕ СПРАЙТОВ ЛЕТУЧЕЙ МЫШИ
# ============================================

"""
Варианты получения спрайтов:

1. Нарисовать самому в Piskel (https://www.piskelapp.com/)
   - Размер: 40x40 пикселей
   - 2-3 кадра анимации
   - Сохранить как Bat1.png, Bat2.png, Bat3.png

2. Скачать готовые с сайтов:
   - OpenGameArt.org
   - itch.io/game-assets/free
   - CraftPix.net/freebies

3. Использовать временно картинки птиц (для тестирования):
   В images.py написать: bat_img = bird_img

Создай папку Bat/ в корне проекта и положи туда картинки.
"""

# ============================================
# ТЕСТИРОВАНИЕ
# ============================================

"""
После добавления кода:

1. Создай папку Bat/ с 2-3 картинками летучей мыши
2. Запусти игру
3. Летучие мыши должны появляться справа и лететь зигзагом влево
4. Попробуй сбить их - должны давать 5 очков
5. Летучие мыши должны возвращаться после выхода за экран

Особенности летучей мыши:
- Летает зигзагом (не прямо как птицы)
- Не стреляет (проще чем птицы)
- Движется слева направо (как кактусы)
- Дает очки при убийстве
"""

print("Решение для Задания 3.5 загружено!")
print("Смотри комментарии в этом файле для реализации.")
print("Не забудь создать папку Bat/ с картинками!")
