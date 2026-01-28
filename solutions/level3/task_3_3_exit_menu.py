"""
Задание 3.3: Кнопка выхода из игры (улучшенное меню паузы)

ПРОБЛЕМА:
При нажатии ESC игра просто ставится на паузу с текстом "Paused, press enter to continue".
Нет возможности выйти в главное меню не проигрывая.

РЕШЕНИЕ:
Заменить простую функцию pause() на полноценное меню с кнопками:
- Continue (продолжить игру)
- Quit to Menu (выйти в главное меню)

ВАЖНО: Это задание частично реализовано в задании 3.2 (система сохранений).
Если вы уже сделали задание 3.2, у вас уже есть метод pause_menu() с кнопкой "Save & Quit".
Здесь мы даём упрощённую версию без сохранения.

================================================================================
ЗАМЕНА МЕТОДА pause() В game.py
================================================================================

Найдите в game.py метод pause() (строка ~337) и ЗАМЕНИТЕ его на:
"""

def pause_menu(self):
    """
    Улучшенное меню паузы с кнопками
    
    БЫЛО: Текстовая пауза с ожиданием Enter
    СТАЛО: Графическое меню с кнопками
    """
    paused = True
    pygame.mixer.music.pause()
    
    # Создаём кнопки
    continue_button = Button(222, 70)
    quit_button = Button(260, 70)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # Заливаем экран чёрным
        display.fill([0, 0, 0])
        
        # Заголовок
        print_text('PAUSE', 350, 150, font_size=65)
        
        # Кнопка продолжить
        if continue_button.draw(290, 270, 'Continue', font_size=50):
            paused = False  # Выходим из паузы
        
        # Кнопка выхода в меню
        if quit_button.draw(250, 360, 'Quit to Menu', font_size=50):
            # Меняем состояние игры на MENU
            self.game_state.change(State.MENU)
            return False  # Говорим run_game() что нужно выйти
        
        pygame.display.update()
        clock.tick(15)
    
    # Возобновляем музыку при продолжении
    pygame.mixer.music.unpause()
    return True  # Продолжаем игру


"""
================================================================================
ИЗМЕНЕНИЕ ВЫЗОВА ПАУЗЫ В run_game()
================================================================================

Найдите в run_game() (строка ~180) код:

    if keys[pygame.K_ESCAPE]:
        self.pause()

ЗАМЕНИТЕ НА:

    if keys[pygame.K_ESCAPE]:
        if not self.pause_menu():
            return False  # Выходим из run_game() если нажали Quit to Menu


ОБЪЯСНЕНИЕ:
- pause_menu() возвращает True если игра продолжается
- pause_menu() возвращает False если игрок выбрал "Quit to Menu"
- Если False, то run_game() завершается с return False
- start_game() получает False и тоже завершается
- Игрок возвращается в главное меню

================================================================================
ПОЛНЫЙ КОД С ИЗМЕНЕНИЯМИ
================================================================================
"""

# ПОЛНЫЙ МЕТОД pause_menu():
def pause_menu_full(self):
    """ГОТОВО ДЛЯ КОПИРОВАНИЯ"""
    paused = True
    pygame.mixer.music.pause()
    
    continue_button = Button(222, 70)
    quit_button = Button(260, 70)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        display.fill([0, 0, 0])
        print_text('PAUSE', 350, 150, font_size=65)
        
        if continue_button.draw(290, 270, 'Continue', font_size=50):
            paused = False
        
        if quit_button.draw(250, 360, 'Quit to Menu', font_size=50):
            self.game_state.change(State.MENU)
            return False
        
        pygame.display.update()
        clock.tick(15)
    
    pygame.mixer.music.unpause()
    return True


# ИЗМЕНЕННЫЙ ФРАГМЕНТ run_game():
"""
# В методе run_game(), примерно строка 180:

        if keys[pygame.K_ESCAPE]:
            if not self.pause_menu():
                return False  # Выход в меню
"""


"""
================================================================================
ВАРИАНТ С СОХРАНЕНИЕМ (из задания 3.2)
================================================================================

Если хотите добавить ещё и кнопку сохранения:
"""

def pause_menu_with_save(self):
    """Меню паузы с сохранением (комбинация заданий 3.2 и 3.3)"""
    paused = True
    pygame.mixer.music.pause()
    
    continue_button = Button(222, 70)
    save_quit_button = Button(250, 70)
    quit_button = Button(260, 70)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        display.fill([0, 0, 0])
        print_text('PAUSE', 350, 120, font_size=65)
        
        # Продолжить
        if continue_button.draw(290, 220, 'Continue', font_size=50):
            paused = False
        
        # Сохранить и выйти
        if save_quit_button.draw(250, 310, 'Save & Quit', font_size=50):
            self.save_data.save_game_state(
                health=self.health,
                scores=self.scores,
                level=getattr(self, 'level', 1)
            )
            self.game_state.change(State.MENU)
            return False
        
        # Выйти без сохранения
        if quit_button.draw(230, 400, 'Quit (No Save)', font_size=45):
            self.game_state.change(State.MENU)
            return False
        
        pygame.display.update()
        clock.tick(15)
    
    pygame.mixer.music.unpause()
    return True


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ При нажатии ESC открывается графическое меню
✅ Есть кнопка "Continue" для продолжения игры
✅ Есть кнопка "Quit to Menu" для выхода в главное меню
✅ Музыка ставится на паузу и возобновляется корректно
✅ Можно выйти из игры не проигрывая

КАК ПРОВЕРИТЬ:
1. Запустите игру
2. Начните играть
3. Нажмите ESC
4. Попробуйте нажать "Continue" - игра должна продолжиться
5. Снова нажмите ESC
6. Нажмите "Quit to Menu" - должны вернуться в главное меню
7. Проверьте что игра не сохранилась (если не сделали задание 3.2)
"""
