"""
Задание 2.3: Добавление 4-го типа кактуса

БЫЛО: 3 вида кактусов
СТАЛО: 4 вида кактусов

================================================================================
ШАГ 1: ПОДГОТОВКА КАРТИНКИ
================================================================================

ВАРИАНТ А: Найти/нарисовать картинку
1. Найдите картинку кактуса (~30x50 пикселей)
2. Сохраните как Objects/Cactus4.jpg

ВАРИАНТ Б: Временно использовать существующий
1. Скопируйте Objects/Cactus1.jpg
2. Переименуйте копию в Cactus4.jpg


================================================================================
ШАГ 2: ЗАГРУЗКА В images.py
================================================================================

Файл: images.py
Найдите список cactus_img (примерно строка 29-33)
"""

# БЫЛО:
cactus_img = [
    pygame.image.load('Objects/Cactus1.jpg'),
    pygame.image.load('Objects/Cactus2.jpg'),
    pygame.image.load('Objects/Cactus3.jpg')
]

# СТАЛО:
cactus_img = [
    pygame.image.load('Objects/Cactus1.jpg'),
    pygame.image.load('Objects/Cactus2.jpg'),
    pygame.image.load('Objects/Cactus3.jpg'),
    pygame.image.load('Objects/Cactus4.jpg')  # ДОБАВЛЕНО
]


"""
================================================================================
ШАГ 3: ПАРАМЕТРЫ КАКТУСА В game.py
================================================================================

Файл: game.py
Строка: 19 (в __init__)
"""

# БЫЛО:
self.cactus_options = [20, 430, 30, 450, 25, 420]

# СТАЛО (добавили параметры для 4-го кактуса):
self.cactus_options = [20, 430, 30, 450, 25, 420, 35, 440]
#                                                  ↑     ↑
#                                              ширина высота


"""
ОБЪЯСНЕНИЕ:
Массив cactus_options хранит пары [ширина, высота] для каждого кактуса:
- 20, 430 - кактус 1
- 30, 450 - кактус 2
- 25, 420 - кактус 3
- 35, 440 - кактус 4 (НОВЫЙ)

================================================================================
ШАГ 4: ИЗМЕНЕНИЕ ДИАПАЗОНА ВЫБОРА
================================================================================

Файл: game.py
Метод: create_cactus_arr() (примерно строка 248)

Найдите ВСЕ строки с random.randrange(0, 3) в этом методе и измените на (0, 4):
"""

# БЫЛО (3 раза в методе):
def create_cactus_arr(self, array):
    choice = random.randrange(0, 3)  # ← ИЗМЕНИТЬ НА (0, 4)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 3)  # ← ИЗМЕНИТЬ НА (0, 4)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 3)  # ← ИЗМЕНИТЬ НА (0, 4)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


# СТАЛО:
def create_cactus_arr(self, array):
    choice = random.randrange(0, 4)  # ИЗМЕНЕНО
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 20, height, width, img, 4))

    choice = random.randrange(0, 4)  # ИЗМЕНЕНО
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 300, height, width, img, 4))

    choice = random.randrange(0, 4)  # ИЗМЕНЕНО
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]
    array.append(Object(display_width + 600, height, width, img, 4))


"""
================================================================================
ШАГ 5: ИЗМЕНЕНИЕ В object_return()
================================================================================

Файл: game.py
Метод: object_return() (примерно строка 292)
"""

# БЫЛО:
def object_return(self, objects, obj):
    radius = self.find_radius(objects)

    choice = random.randrange(0, 3)  # ← ИЗМЕНИТЬ НА (0, 4)
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


# СТАЛО:
def object_return(self, objects, obj):
    radius = self.find_radius(objects)

    choice = random.randrange(0, 4)  # ИЗМЕНЕНО
    img = cactus_img[choice]
    width = self.cactus_options[choice * 2]
    height = self.cactus_options[choice * 2 + 1]

    obj.return_self(radius, height, width, img)


"""
================================================================================
ИТОГО: ЧТО НУЖНО ИЗМЕНИТЬ
================================================================================

1. images.py:
   - Добавить pygame.image.load('Objects/Cactus4.jpg') в список

2. game.py, __init__:
   - self.cactus_options = [20, 430, 30, 450, 25, 420, 35, 440]

3. game.py, create_cactus_arr():
   - 3 раза: random.randrange(0, 3) → random.randrange(0, 4)

4. game.py, object_return():
   - 1 раз: random.randrange(0, 3) → random.randrange(0, 4)


================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ В игре появляется 4-й вид кактуса
✅ Он может быть выбран случайным образом
✅ Больше разнообразия препятствий

КАК ПРОВЕРИТЬ:
1. Примените все изменения
2. Запустите игру
3. Играйте несколько минут
4. Вы должны увидеть новый вид кактуса

ПРИМЕЧАНИЕ:
Можно добавить ещё больше кактусов (5, 6, 7...) аналогичным способом!
"""
