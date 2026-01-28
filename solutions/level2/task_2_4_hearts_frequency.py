"""
Задание 2.4: Изменение частоты появления сердечек

БЫЛО: Сердечки появляются редко (каждые 500-10000 пикселей)
СТАЛО: Сердечки появляются чаще (каждые 300-3000 пикселей)

================================================================================
ЧТО НУЖНО ИЗМЕНИТЬ
================================================================================

Файл: game.py
Метод: hearts_plus()
Строка: примерно 482
"""

# БЫЛО:
def hearts_plus(self, heart):
    if heart.x <= -heart.width:
        radius = p.display_width + random.randrange(500, 10000)  # ← ИЗМЕНИТЬ
        heart.return_self(radius, heart.y, heart.width, heart.image)

    if p.usr_x <= heart.x <= p.usr_x + p.usr_height:
        if p.usr_y <= heart.y <= p.usr_y + p.usr_height:
            pygame.mixer.Sound.play(heart_plus_sound)
            if self.health < 2:
                self.health += 1

            radius = p.display_width + random.randrange(500, 10000)  # ← ИЗМЕНИТЬ
            heart.return_self(radius, heart.y, heart.width, heart.image)


# СТАЛО (сердечки появляются чаще):
def hearts_plus(self, heart):
    if heart.x <= -heart.width:
        radius = p.display_width + random.randrange(300, 3000)  # ИЗМЕНЕНО
        heart.return_self(radius, heart.y, heart.width, heart.image)

    if p.usr_x <= heart.x <= p.usr_x + p.usr_height:
        if p.usr_y <= heart.y <= p.usr_y + p.usr_height:
            pygame.mixer.Sound.play(heart_plus_sound)
            if self.health < 2:
                self.health += 1

            radius = p.display_width + random.randrange(300, 3000)  # ИЗМЕНЕНО
            heart.return_self(radius, heart.y, heart.width, heart.image)


"""
================================================================================
ВАРИАНТЫ ЧАСТОТЫ
================================================================================

Очень часто (почти всегда видно сердечко):
    random.randrange(200, 1000)

Часто:
    random.randrange(300, 3000)

Средне (по умолчанию в решении):
    random.randrange(500, 5000)

Редко (исходная настройка):
    random.randrange(500, 10000)

Очень редко (почти никогда):
    random.randrange(1000, 20000)


================================================================================
ДОПОЛНИТЕЛЬНО: Изменить максимальное здоровье
================================================================================

По умолчанию сердечко восстанавливает здоровье только если health < 2.
Если вы сделали задание 2.1 (увеличили жизни до 5), измените условие:
"""

# Если здоровье может быть до 5:
if self.health < 5:  # ВМЕСТО: if self.health < 2:
    self.health += 1


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ Сердечки появляются чаще
✅ Легче восстанавливать здоровье
✅ Игра становится немного легче

КАК ПРОВЕРИТЬ:
1. Откройте game.py
2. Найдите метод hearts_plus()
3. Найдите ДВЕ строки с random.randrange(500, 10000)
4. Измените обе на random.randrange(300, 3000)
5. Запустите игру
6. Сердечки должны появляться чаще

ПРИМЕЧАНИЕ:
Обязательно измените ОБЕОБА места в методе hearts_plus()!
"""
