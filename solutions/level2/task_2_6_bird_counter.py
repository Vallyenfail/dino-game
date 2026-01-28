"""
Задание 2.6: Счетчик убитых птиц

БЫЛО: Нет счётчика убийств
СТАЛО: На экране отображается количество убитых птиц

================================================================================
ШАГ 1: ДОБАВЛЕНИЕ ПЕРЕМЕННОЙ СЧЕТЧИКА
================================================================================

Файл: game.py
Метод: __init__()
Строка: примерно 12
"""

# Добавьте в __init__():
self.birds_killed = 0  # Счётчик убитых птиц


"""
================================================================================
ШАГ 2: ИЗМЕНЕНИЕ Bird.py - ВОЗВРАТ ЗНАЧЕНИЯ
================================================================================

Файл: Bird.py
Метод: kill_bird()
Строка: примерно 57
"""

# БЫЛО:
def kill_bird(self, bullet):
    if self.x <= bullet.x <= self.x + self.width:
        if self.y <= bullet.y <= self.y + self.height:
            self.go_away = True


# СТАЛО (добавлен return):
def kill_bird(self, bullet):
    if self.x <= bullet.x <= self.x + self.width:
        if self.y <= bullet.y <= self.y + self.height:
            self.go_away = True
            return True  # ДОБАВЛЕНО
    return False  # ДОБАВЛЕНО


"""
================================================================================
ШАГ 3: ИЗМЕНЕНИЕ check_birds_dmg() В game.py
================================================================================

Файл: game.py
Метод: check_birds_dmg()
Строка: примерно 507
"""

# БЫЛО:
@staticmethod
def check_birds_dmg(bullets, birds):
    for bird in birds:
        for bullet in bullets:
            bird.kill_bird(bullet)


# СТАЛО (убрали @staticmethod и добавили self, увеличиваем счётчик):
def check_birds_dmg(self, bullets, birds):
    for bird in birds:
        for bullet in bullets:
            if bird.kill_bird(bullet):  # ИЗМЕНЕНО: проверяем возврат
                self.birds_killed += 1  # ДОБАВЛЕНО: увеличиваем счётчик


"""
================================================================================
ШАГ 4: ОТОБРАЖЕНИЕ СЧЕТЧИКА НА ЭКРАНЕ
================================================================================

Файл: game.py
Метод: run_game()
Строка: примерно 172 (после отображения счёта)
"""

# После строки:
print_text('Score: ' + str(self.scores), 600, 10)

# Добавьте:
print_text('Birds: ' + str(self.birds_killed), 600, 40, font_size=25)


"""
================================================================================
ШАГ 5: СБРОС СЧЕТЧИКА ПРИ ПЕРЕЗАПУСКЕ
================================================================================

Файл: game.py
Метод: start_game()
Строка: примерно 78
"""

# В start_game() добавьте сброс:
def start_game(self):
    while self.run_game():
        self.scores = 0
        self.make_jump = False
        self.jump_counter = 30
        p.usr_y = p.display_height - p.usr_height - 100
        self.health = 2
        self.cooldown = 0
        self.birds_killed = 0  # ДОБАВЛЕНО: сброс счётчика


"""
================================================================================
ПОЛНЫЙ КОД ДЛЯ КОПИРОВАНИЯ
================================================================================
"""

# 1. В game.py, __init__():
"""
self.birds_killed = 0
"""

# 2. В Bird.py, kill_bird():
"""
def kill_bird(self, bullet):
    if self.x <= bullet.x <= self.x + self.width:
        if self.y <= bullet.y <= self.y + self.height:
            self.go_away = True
            return True
    return False
"""

# 3. В game.py, check_birds_dmg() - ЗАМЕНИТЬ ПОЛНОСТЬЮ:
"""
def check_birds_dmg(self, bullets, birds):
    for bird in birds:
        for bullet in bullets:
            if bird.kill_bird(bullet):
                self.birds_killed += 1
"""

# 4. В run_game(), после отображения счёта:
"""
print_text('Birds: ' + str(self.birds_killed), 600, 40, font_size=25)
"""

# 5. В start_game():
"""
self.birds_killed = 0
"""


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ На экране отображается счётчик убитых птиц
✅ Счётчик увеличивается при каждом попадании
✅ Счётчик сбрасывается при новой игре
✅ Можно отслеживать свой прогресс в убийстве птиц

КАК ПРОВЕРИТЬ:
1. Примените все изменения
2. Запустите игру
3. Дождитесь появления птицы
4. Сбейте её
5. В правом верхнем углу должен увеличиться счётчик "Birds: 1"
6. Сбейте ещё птицу - счётчик увеличится до 2

ДОПОЛНИТЕЛЬНО:
Можно добавить очки за убийство птиц:
"""

# В check_birds_dmg():
"""
if bird.kill_bird(bullet):
    self.birds_killed += 1
    self.scores += 10  # ДОБАВЛЕНО: +10 очков за птицу
"""
