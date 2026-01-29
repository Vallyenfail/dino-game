"""
Задание 3.7: Бонус "Щит" (защита от одного удара)

ПРОБЛЕМА:
В игре есть только сердечки для восстановления здоровья. Нет других бонусов.

РЕШЕНИЕ:
Добавить бонус-щит, который защищает от одного столкновения с препятствием.

================================================================================
ШАГ 1: ПОДГОТОВКА КАРТИНКИ ЩИТА
================================================================================

ВАРИАНТ А: Использовать существующую картинку сердечка
--------------------------------------------------------
В images.py добавьте:

# Щит (используем сердечко временно)
shield_img = health_img


ВАРИАНТ Б: Создать собственную картинку
----------------------------------------
1. Найдите или создайте картинку щита (30x30 пикселей)
2. Сохраните как Objects/shield.png
3. В images.py добавьте:

# Щит
shield_img = pygame.image.load('Objects/shield.png')


================================================================================
ШАГ 2: ДОБАВЛЕНИЕ ПЕРЕМЕННОЙ ЩИТА
================================================================================

В game.py, в методе __init__() (строка ~12), добавьте:

    self.has_shield = False  # Флаг наличия щита


================================================================================
ШАГ 3: СОЗДАНИЕ ОБЪЕКТА ЩИТА
================================================================================

В run_game(), после создания сердечка (примерно строка 141):
"""

# После: heart = Object(display_width, 280, 30, health_img, 4)
# Добавьте:
from images import shield_img  # В начале метода
shield = Object(display_width + random.randrange(300, 800), 250, 30, shield_img, 4)


"""
================================================================================
ШАГ 4: ДВИЖЕНИЕ И ПОДБОР ЩИТА
================================================================================

В run_game(), после hearts_plus() (примерно строка 210):
"""

# После: self.hearts_plus(heart)
# Добавьте:

# Движение щита
shield.move()

# Подбор щита
if shield.x <= -shield.width:
    # Щит улетел за экран, создаём новый далеко
    radius = p.display_width + random.randrange(800, 15000)  # Редко появляется
    shield.return_self(radius, shield.y, shield.width, shield.image)

# Проверка подбора щита
if p.usr_x <= shield.x <= p.usr_x + p.usr_height:
    if p.usr_y <= shield.y <= p.usr_y + p.usr_height:
        if not self.has_shield:  # Только если щита ещё нет
            pygame.mixer.Sound.play(heart_plus_sound)
            self.has_shield = True
            # Убираем щит далеко
            radius = p.display_width + random.randrange(800, 15000)
            shield.return_self(radius, shield.y, shield.width, shield.image)


"""
================================================================================
ШАГ 5: ИСПОЛЬЗОВАНИЕ ЩИТА ПРИ СТОЛКНОВЕНИИ
================================================================================

В check_collision() изменить логику:
Найдите метод check_collision() (строка ~359), в начале каждого блока где
вызывается self.check_health(), добавьте проверку щита.

БЫЛО:
"""

if self.check_health():
    self.object_return(barriers, barrier)
    return False
else:
    return True

"""
СТАЛО:
"""

# Проверяем щит
if self.has_shield:
    self.has_shield = False  # Убираем щит
    pygame.mixer.Sound.play(crash_sound)
    self.object_return(barriers, barrier)
    return False
elif self.check_health():
    self.object_return(barriers, barrier)
    return False
else:
    return True


"""
================================================================================
ШАГ 6: ОТОБРАЖЕНИЕ ЩИТА НА ЭКРАНЕ
================================================================================

В show_health() (строка ~462) добавьте отображение щита:
"""

def show_health(self):
    """Показывает здоровье и щит"""
    show = 0
    x = 20
    # Отображаем сердечки
    while show != self.health:
        display.blit(health_img, (x, 20))
        x += 40
        show += 1
    
    # НОВЫЙ КОД: Отображаем щит если есть
    if self.has_shield:
        display.blit(shield_img, (x, 20))  # Рисуем щит после сердечек


"""
================================================================================
ШАГ 7: СБРОС ЩИТА ПРИ ПЕРЕЗАПУСКЕ
================================================================================

В start_game() (строка ~78):
"""

def start_game(self):
    while self.run_game():
        self.scores = 0
        self.make_jump = False
        self.jump_counter = 30
        p.usr_y = p.display_height - p.usr_height - 100
        self.health = 2
        self.cooldown = 0
        self.has_shield = False  # ДОБАВЛЕНО: сброс щита


"""
================================================================================
РАСШИРЕННАЯ ВЕРСИЯ: Временный щит
================================================================================

Щит может действовать ограниченное время вместо одного удара:
"""

# В __init__():
"""
self.has_shield = False
self.shield_timer = 0  # Таймер щита
"""

# В run_game(), после подбора щита:
"""
if not self.has_shield:
    self.has_shield = True
    self.shield_timer = 300  # 300 кадров = ~4 секунды при 80 FPS
"""

# В игровом цикле:
"""
# Уменьшаем таймер щита
if self.has_shield:
    self.shield_timer -= 1
    if self.shield_timer <= 0:
        self.has_shield = False
    
    # Мигающий эффект когда заканчивается
    if self.shield_timer < 60 and self.shield_timer % 20 < 10:
        # Не рисуем щит (эффект мигания)
        pass
    else:
        # Рисуем щит вокруг игрока
        pygame.draw.circle(display, (0, 200, 255), 
                          (p.usr_x + p.usr_width//2, p.usr_y + p.usr_height//2), 
                          55, 3)
"""


"""
================================================================================
ПОЛНЫЙ КОД ДЛЯ КОПИРОВАНИЯ
================================================================================
"""

# 1. В images.py:
"""
shield_img = health_img  # Используем сердечко как щит временно
"""

# 2. В game.py, __init__():
"""
self.has_shield = False
"""

# 3. В run_game(), после создания heart:
"""
from images import shield_img
shield = Object(display_width + random.randrange(300, 800), 250, 30, shield_img, 4)
"""

# 4. В run_game(), после hearts_plus():
"""
# Щит
shield.move()
if shield.x <= -shield.width:
    radius = p.display_width + random.randrange(800, 15000)
    shield.return_self(radius, shield.y, shield.width, shield.image)

if p.usr_x <= shield.x <= p.usr_x + p.usr_height:
    if p.usr_y <= shield.y <= p.usr_y + p.usr_height:
        if not self.has_shield:
            pygame.mixer.Sound.play(heart_plus_sound)
            self.has_shield = True
            radius = p.display_width + random.randrange(800, 15000)
            shield.return_self(radius, shield.y, shield.width, shield.image)
"""

# 5. В check_collision(), перед каждым check_health():
"""
if self.has_shield:
    self.has_shield = False
    pygame.mixer.Sound.play(crash_sound)
    self.object_return(barriers, barrier)
    return False
elif self.check_health():
    # ... остальной код
"""

# 6. В show_health():
"""
if self.has_shield:
    display.blit(shield_img, (x, 20))
"""

# 7. В start_game():
"""
self.has_shield = False
"""


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ Щит редко появляется на экране
✅ При подборе щита он отображается рядом с сердечками
✅ При столкновении с кактусом щит поглощает удар
✅ Здоровье не уменьшается если есть щит
✅ После использования щит пропадает

КАК ПРОВЕРИТЬ:
1. Запустите игру
2. Дождитесь появления щита (может потребоваться время)
3. Подберите щит - должна появиться иконка рядом с сердечками
4. Специально столкнитесь с кактусом
5. Щит должен пропасть, но здоровье не уменьшится
6. Следующее столкновение уже отнимет здоровье

СОВЕТЫ ПО БАЛАНСУ:
- Частота: random.randrange(800, 15000) - чем больше второе число, тем реже
- Можно сделать щит чаще: (500, 5000)
- Или добавить несколько щитов одновременно
"""
