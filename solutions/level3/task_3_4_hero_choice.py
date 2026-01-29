"""
Задание 3.4: Реализация выбора персонажа

ПРОБЛЕМА:
В коде есть готовая функция choose_hero() (строка 88 в game.py), но она нигде не вызывается.
Игрок не может выбрать персонажа перед началом игры.

РЕШЕНИЕ:
Просто добавить вызов choose_hero() в нужном месте.

================================================================================
ИЗМЕНЕНИЕ В game.py
================================================================================

Найдите метод start() (строка ~32), найдите блок:

    elif self.game_state.check(State.START):
        self.choose_theme()
        self.start_game()

ЗАМЕНИТЕ НА:

    elif self.game_state.check(State.START):
        self.choose_hero()      # ДОБАВИЛИ: выбор персонажа
        self.choose_theme()
        self.start_game()


ОБЪЯСНЕНИЕ:
- choose_hero() уже реализована в коде (строка 88-108)
- Она показывает меню выбора между "Pink Dino" и "Purple Dino"
- Использует функцию set_theme() для смены спрайтов
- Мы просто добавляем её вызов перед choose_theme()

================================================================================
КАК РАБОТАЕТ choose_hero()
================================================================================
"""

# СУЩЕСТВУЮЩИЙ КОД в game.py (строка 88-108):
def choose_hero_existing(self):
    """Функция уже есть в коде, ничего менять не нужно"""
    hero1 = Button(300, 70)
    hero2 = Button(300, 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill([0, 0, 0])

        if hero1.draw(270, 200, 'Pink Dino', font_size=50):
            set_theme(1)  # Устанавливаем тему 1
            return
        if hero2.draw(270, 300, 'Purple Dino', font_size=50):
            set_theme(2)  # Устанавливаем тему 2
            return

        pygame.display.update()
        clock.tick(60)


"""
================================================================================
ДОПОЛНИТЕЛЬНО: Создание собственных персонажей
================================================================================

Если хотите добавить своих персонажей:

1. Подготовьте спрайты:
   - Создайте папку с новыми спрайтами динозавра
   - Назовите их так же: Dino1.jpg, Dino2.jpg, Dino3.jpg, Dino_jump.jpg, Dino_jump2.jpg

2. Обновите images.py:
"""

# ПРИМЕР ДОБАВЛЕНИЯ ТРЕТЬЕГО ПЕРСОНАЖА в images.py:
"""
# В конце файла images.py добавьте:

def set_theme(num):
    global land, dino_img
    land = pygame.image.load(f'Effects and background/Land{num}.jpg')
    
    # ДОБАВЛЕНО: поддержка третьего персонажа
    if num == 3:
        dino_img = [
            pygame.image.load('Dino3/Dino1.jpg'),  # Папка с третьим персонажем
            pygame.image.load('Dino3/Dino3.jpg'),
            pygame.image.load('Dino3/Dino2.jpg'),
            pygame.image.load('Dino3/Dino_jump.jpg'),
            pygame.image.load('Dino3/Dino_jump2.jpg')
        ]
"""

# ОБНОВЛЕННАЯ choose_hero() с тремя персонажами:
def choose_hero_extended(self):
    """Расширенная версия с тремя персонажами"""
    hero1 = Button(300, 70)
    hero2 = Button(300, 70)
    hero3 = Button(300, 70)  # НОВАЯ КНОПКА

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill([0, 0, 0])
        print_text('Choose Your Character', 210, 100, font_size=50)

        if hero1.draw(250, 200, 'Pink Dino', font_size=45):
            set_theme(1)
            return
        if hero2.draw(250, 290, 'Purple Dino', font_size=45):
            set_theme(2)
            return
        if hero3.draw(250, 380, 'Blue Dino', font_size=45):  # НОВАЯ КНОПКА
            set_theme(3)
            return

        pygame.display.update()
        clock.tick(60)


"""
================================================================================
АЛЬТЕРНАТИВА: Объединить выбор героя и темы
================================================================================

Можно сделать так, чтобы выбор персонажа сразу определял и фон:
"""

def choose_hero_and_theme(self):
    """Выбор персонажа определяет и фон"""
    hero1 = Button(300, 70)
    hero2 = Button(300, 70)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.fill([0, 0, 0])
        print_text('Choose Your Character', 210, 80, font_size=50)
        
        # Превью персонажей (если есть картинки)
        # display.blit(hero1_preview, (200, 150))
        # display.blit(hero2_preview, (500, 150))

        if hero1.draw(150, 400, 'Day Runner', font_size=45):
            set_theme(1)  # Дневная тема + розовый динозавр
            return
        if hero2.draw(450, 400, 'Night Runner', font_size=45):
            set_theme(2)  # Ночная тема + фиолетовый динозавр
            return

        pygame.display.update()
        clock.tick(60)


"""
И в методе start() оставить только:

    elif self.game_state.check(State.START):
        self.choose_hero()  # Один вызов вместо двух
        self.start_game()
"""


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ При нажатии "Start game" появляется экран выбора персонажа
✅ Можно выбрать между Pink Dino и Purple Dino
✅ После выбора персонажа открывается выбор темы
✅ Игра начинается с выбранным персонажем

КАК ПРОВЕРИТЬ:
1. Запустите игру
2. Нажмите "Start game"
3. Должен появиться экран выбора персонажа
4. Выберите любого персонажа
5. Выберите тему
6. Проверьте что играете выбранным персонажем

ПРИМЕЧАНИЕ:
Если у вас нет разных спрайтов для персонажей, set_theme() может менять
только фон, а персонаж останется тем же. Это нормально для базовой версии игры.
"""
