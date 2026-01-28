"""
Задание 1.5: Изменение скорости кактусов

БЫЛО: Скорость = 4
СТАЛО: Скорость = 2 (легче) или 6 (сложнее)

================================================================================
ЧТО НУЖНО ИЗМЕНИТЬ
================================================================================

Файл: game.py
Метод: create_cactus_arr()
Строка: примерно 248-265 (последний параметр в Object)
"""

# БЫЛО (3 раза в методе):
def create_cactus_arr(self, array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))  # ← 4 это скорость
    
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))  # ← ИЗМЕНИТЬ
    
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))  # ← ИЗМЕНИТЬ


"""
================================================================================
ВАРИАНТЫ СКОРОСТИ
================================================================================

Очень медленно (для детей):
    Object(..., 2)

Медленно:
    Object(..., 3)

Обычно (по умолчанию):
    Object(..., 4)

Быстро:
    Object(..., 6)

Очень быстро:
    Object(..., 8)

Безумие:
    Object(..., 12)


================================================================================
РАЗНАЯ СКОРОСТЬ ДЛЯ КАЖДОГО КАКТУСА
================================================================================

Можно сделать чтобы кактусы двигались с разной скоростью:
"""

def create_cactus_arr(self, array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 3))  # Медленный
    
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))  # Средний
    
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 6))  # Быстрый


"""
Это сделает игру более разнообразной!


================================================================================
СЛУЧАЙНАЯ СКОРОСТЬ
================================================================================

Можно добавить случайную скорость для каждого кактуса:
"""

def create_cactus_arr(self, array):
    choice = random.randrange(0, 3)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    speed = random.randrange(3, 7)  # Случайная скорость от 3 до 6
    array.append(Object(display_width + 20, height, width, img, speed))
    
    # То же для остальных кактусов...


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

С МЕДЛЕННОЙ СКОРОСТЬЮ (2-3):
✅ Кактусы движутся медленнее
✅ Легче перепрыгивать
✅ Игра подходит для начинающих

С БЫСТРОЙ СКОРОСТЬЮ (6-8):
✅ Кактусы летят быстро
✅ Сложнее играть
✅ Требуется быстрая реакция

КАК ПРОВЕРИТЬ:
1. Откройте game.py
2. Найдите метод create_cactus_arr()
3. Найдите 3 строки с Object(..., 4)
4. Измените последний параметр (4) на желаемую скорость
5. Запустите игру
6. Кактусы должны двигаться с новой скоростью

ПРИМЕЧАНИЕ:
Изменяйте ВСЕ ТРИ кактуса для одинаковой скорости!
"""
