"""
Задание 3.10: Анимация смерти динозавра

ПРОБЛЕМА:
При Game Over игра мгновенно переходит к экрану проигрыша. Нет плавного перехода.

РЕШЕНИЕ:
Добавить анимацию падения динозавра перед показом экрана Game Over.

================================================================================
ВАРИАНТ 1: Простая анимация падения
================================================================================

В check_collision(), перед return True (когда health == 0):
"""

# Найдите в check_collision() конец (где проверяется здоровье)
# БЫЛО:
if self.check_health():
    self.object_return(barriers, barrier)
    return False
else:
    return True  # Game Over


# СТАЛО:
if self.check_health():
    self.object_return(barriers, barrier)
    return False
else:
    # НОВЫЙ КОД: Анимация смерти
    self.death_animation()
    return True


"""
================================================================================
МЕТОД АНИМАЦИИ СМЕРТИ
================================================================================

Добавьте в класс Game новый метод:
"""

def death_animation(self):
    """Анимация смерти динозавра"""
    # Звук смерти (уже воспроизводится в check_health)
    
    # Анимация падения
    for i in range(30):
        display.blit(imgs.land, (0, 0))
        
        # Динозавр падает вниз
        fall_y = p.usr_y + i * 3
        display.blit(dino_img[3], (p.usr_x, fall_y))  # Используем спрайт прыжка
        
        pygame.display.update()
        clock.tick(30)
    
    # Небольшая пауза перед Game Over
    pygame.time.delay(500)


"""
================================================================================
ВАРИАНТ 2: Анимация с вращением
================================================================================

Более сложная анимация с поворотом динозавра:
"""

def death_animation_rotate(self):
    """Анимация смерти с вращением"""
    angle = 0
    fall_speed = 0
    
    for i in range(40):
        display.blit(imgs.land, (0, 0))
        
        # Увеличиваем скорость падения
        fall_speed += 0.5
        fall_y = p.usr_y + fall_speed
        
        # Вращаем динозавра
        angle -= 9  # Поворот на 9 градусов каждый кадр
        rotated_dino = pygame.transform.rotate(dino_img[3], angle)
        
        # Центрируем после поворота
        rect = rotated_dino.get_rect(center=(p.usr_x + p.usr_width // 2, fall_y))
        display.blit(rotated_dino, rect)
        
        pygame.display.update()
        clock.tick(30)
        
        # Останавливаем когда упал на землю
        if fall_y >= p.display_height - 50:
            break
    
    pygame.time.delay(500)


"""
================================================================================
ВАРИАНТ 3: Простое затемнение
================================================================================

Если вращение слишком сложное, можно просто затемнить экран:
"""

def death_animation_fade(self):
    """Анимация затемнения"""
    # Создаём полупрозрачную поверхность
    fade_surface = pygame.Surface((p.display_width, p.display_height))
    fade_surface.fill((0, 0, 0))
    
    # Постепенное затемнение
    for alpha in range(0, 255, 5):
        display.blit(imgs.land, (0, 0))
        display.blit(dino_img[3], (p.usr_x, p.usr_y))
        
        fade_surface.set_alpha(alpha)
        display.blit(fade_surface, (0, 0))
        
        pygame.display.update()
        clock.tick(30)
    
    pygame.time.delay(500)


"""
================================================================================
ВАРИАНТ 4: Комбинированная анимация
================================================================================

Падение + затемнение:
"""

def death_animation_combined(self):
    """Комбинированная анимация смерти"""
    fall_speed = 0
    fade_surface = pygame.Surface((p.display_width, p.display_height))
    fade_surface.fill((0, 0, 0))
    
    for i in range(40):
        display.blit(imgs.land, (0, 0))
        
        # Падение
        fall_speed += 0.8
        fall_y = min(p.usr_y + fall_speed * i, p.display_height - p.usr_height - 100)
        display.blit(dino_img[3], (p.usr_x, fall_y))
        
        # Затемнение (начинается после 20 кадров)
        if i > 20:
            alpha = (i - 20) * 12
            fade_surface.set_alpha(min(alpha, 200))
            display.blit(fade_surface, (0, 0))
        
        pygame.display.update()
        clock.tick(30)
    
    pygame.time.delay(500)


"""
================================================================================
ПРОСТЕЙШИЙ ВАРИАНТ: Мигающий эффект
================================================================================

Если анимация сложная, можно просто сделать мигающий эффект:
"""

def death_animation_simple(self):
    """Простая мигающая анимация"""
    for i in range(6):  # 3 полных мигания
        if i % 2 == 0:
            display.fill((255, 0, 0))  # Красный
        else:
            display.blit(imgs.land, (0, 0))
            display.blit(dino_img[3], (p.usr_x, p.usr_y))
        
        pygame.display.update()
        pygame.time.delay(200)


"""
================================================================================
ПОЛНЫЙ КОД ДЛЯ КОПИРОВАНИЯ
================================================================================
"""

# 1. Добавьте метод в класс Game:
"""
def death_animation(self):
    '''Анимация смерти динозавра'''
    for i in range(30):
        display.blit(imgs.land, (0, 0))
        fall_y = p.usr_y + i * 3
        display.blit(dino_img[3], (p.usr_x, fall_y))
        pygame.display.update()
        clock.tick(30)
    pygame.time.delay(500)
"""

# 2. В check_collision(), перед финальным return True:
"""
else:
    self.death_animation()  # ДОБАВЛЕНО
    return True
"""


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ При столкновении с последним здоровьем динозавр падает вниз
✅ Анимация длится ~1 секунду
✅ После анимации показывается экран Game Over
✅ Игра выглядит более профессионально

КАК ПРОВЕРИТЬ:
1. Запустите игру
2. Специально столкнитесь с кактусами 2 раза
3. При последнем столкновении должна проиграться анимация падения
4. После анимации появится экран Game Over

СОВЕТЫ:
- Для более плавной анимации увеличьте количество кадров (range(30) → range(50))
- Для более быстрой анимации уменьшите (range(30) → range(15))
- Экспериментируйте с разными вариантами анимации!
"""
