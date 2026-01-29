"""
Задание 3.2: Система полноценных сохранений

ПРОБЛЕМА:
Кнопка "Continue" в меню сохраняет только максимальный счёт, но не восстанавливает
состояние игры (здоровье, текущие очки, позиции объектов). При нажатии Continue
игра начинается заново.

РЕШЕНИЕ:
Нужно обновить два файла:
1. save.py - добавить методы для сохранения/загрузки состояния игры
2. game.py - изменить обработку Continue и добавить кнопку "Save & Quit"

================================================================================
ЧАСТЬ 1: ОБНОВЛЁННЫЙ save.py
================================================================================
"""

# ПОЛНЫЙ КОД save.py С НОВЫМИ МЕТОДАМИ:

import shelve
import parameters as p


class Save:
    def __init__(self):
        self.file = shelve.open('data')

    def save(self):
        """Сохраняет базовые параметры"""
        self.file['usr_y'] = p.usr_y

    def add(self, name, value):
        """Добавляет значение по ключу"""
        self.file[name] = value

    def get(self, name):
        """Получает значение по ключу"""
        try:
            return self.file[name]
        except KeyError:
            return 0
    
    # ====================================================================
    # НОВЫЕ МЕТОДЫ ДЛЯ СИСТЕМЫ ПОЛНОЦЕННЫХ СОХРАНЕНИЙ
    # ====================================================================
    
    def save_game_state(self, health, scores, level=1):
        """
        Сохраняет полное состояние игры
        
        Args:
            health: Текущее количество жизней
            scores: Текущие очки
            level: Текущий уровень (по умолчанию 1)
        """
        self.file['health'] = health
        self.file['scores'] = scores
        self.file['level'] = level
        self.file['game_exists'] = True  # Флаг что есть сохранённая игра
    
    def load_game_state(self):
        """
        Загружает сохранённое состояние игры
        
        Returns:
            dict: Словарь с ключами 'health', 'scores', 'level', 'exists'
                  Если сохранения нет, возвращает значения по умолчанию
        """
        try:
            return {
                'health': self.file.get('health', 2),
                'scores': self.file.get('scores', 0),
                'level': self.file.get('level', 1),
                'exists': self.file.get('game_exists', False)
            }
        except KeyError:
            return {
                'health': 2,
                'scores': 0,
                'level': 1,
                'exists': False
            }
    
    def clear_game_state(self):
        """
        Очищает сохранённое состояние игры
        Используется при Game Over
        """
        keys_to_delete = ['game_exists', 'health', 'scores', 'level']
        for key in keys_to_delete:
            if key in self.file:
                del self.file[key]
    
    def has_saved_game(self):
        """
        Проверяет наличие сохранённой игры
        
        Returns:
            bool: True если есть сохранение, False иначе
        """
        try:
            return self.file.get('game_exists', False)
        except KeyError:
            return False

    def __del__(self):
        """Деструктор - закрывает файл"""
        self.file.close()


"""
================================================================================
ЧАСТЬ 2: ИЗМЕНЕНИЯ В game.py
================================================================================

ИЗМЕНЕНИЕ 1: Обработка кнопки Continue в методе start()
--------------------------------------------------------------------------------
Найдите в game.py метод start() (строка ~32), найдите блок:

    elif self.game_state.check(State.CONTINUE):
        self.max_scores = self.save_data.get('max')
        self.start_game()

ЗАМЕНИТЕ НА:

    elif self.game_state.check(State.CONTINUE):
        # Загружаем сохранённое состояние
        saved_state = self.save_data.load_game_state()
        
        if saved_state and saved_state['exists']:
            # Восстанавливаем состояние игры
            self.health = saved_state['health']
            self.scores = saved_state['scores']
            self.level = saved_state.get('level', 1)
            self.max_scores = self.save_data.get('max')
            
            self.choose_theme()
            self.start_game()
        else:
            # Если сохранений нет, показываем сообщение
            display.fill([0, 0, 0])
            print_text('No saved game found!', 250, 280, font_size=40)
            print_text('Press Enter to return to menu', 200, 350)
            pygame.display.update()
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RETURN]:
                    waiting = False
            
            self.game_state.change(State.MENU)


ИЗМЕНЕНИЕ 2: Новая функция pause_menu() вместо pause()
--------------------------------------------------------------------------------
Найдите в game.py метод pause() (строка ~337), ЗАМЕНИТЕ ЕГО ПОЛНОСТЬЮ на:

    def pause_menu(self):
        '''Меню паузы с возможностью сохранения и выхода'''
        paused = True
        pygame.mixer.music.pause()
        
        continue_button = Button(222, 70)
        save_quit_button = Button(250, 70)
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            display.fill([0, 0, 0])
            print_text('PAUSE', 350, 180, font_size=60)
            
            # Кнопка продолжить
            if continue_button.draw(290, 270, 'Continue', font_size=50):
                paused = False
            
            # Кнопка сохранить и выйти
            if save_quit_button.draw(250, 360, 'Save & Quit', font_size=50):
                # Сохраняем текущее состояние игры
                self.save_data.save_game_state(
                    health=self.health,
                    scores=self.scores,
                    level=getattr(self, 'level', 1)
                )
                self.game_state.change(State.MENU)
                return False  # Выход из игры
            
            pygame.display.update()
            clock.tick(15)
        
        pygame.mixer.music.unpause()
        return True  # Продолжаем игру


ИЗМЕНЕНИЕ 3: Обновление вызова паузы в run_game()
--------------------------------------------------------------------------------
Найдите в run_game() (строка ~180):

    if keys[pygame.K_ESCAPE]:
        self.pause()

ЗАМЕНИТЕ НА:

    if keys[pygame.K_ESCAPE]:
        if not self.pause_menu():
            return False  # Выходим из игры если нажали Save & Quit


ИЗМЕНЕНИЕ 4: Очистка сохранения при Game Over
--------------------------------------------------------------------------------
Найдите в game.py метод game_over() (строка ~438), В НАЧАЛЕ метода добавьте:

    def game_over(self):
        # Очищаем сохранённую игру так как игрок проиграл
        self.save_data.clear_game_state()
        
        if self.scores > self.max_scores:
            self.max_scores = self.scores
        
        # ... остальной код game_over() ...


================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ Кнопка "Continue" восстанавливает игру с сохранёнными очками и здоровьем
✅ В паузе есть кнопка "Save & Quit" для сохранения и выхода
✅ При Game Over сохранение удаляется автоматически
✅ Если нажать Continue без сохранения, показывается сообщение

КАК ПРОВЕРИТЬ:
1. Запустите игру
2. Наиграйте несколько очков
3. Нажмите ESC
4. Нажмите "Save & Quit"
5. В главном меню нажмите "Continue"
6. Убедитесь что игра продолжилась с сохранёнными очками и здоровьем!
"""

# Для удобства копирования - полный метод pause_menu():
def pause_menu_full_code(self):
    """ПОЛНЫЙ КОД метода pause_menu() - готов для копирования"""
    paused = True
    pygame.mixer.music.pause()
    
    continue_button = Button(222, 70)
    save_quit_button = Button(250, 70)
    
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        display.fill([0, 0, 0])
        print_text('PAUSE', 350, 180, font_size=60)
        
        if continue_button.draw(290, 270, 'Continue', font_size=50):
            paused = False
        
        if save_quit_button.draw(250, 360, 'Save & Quit', font_size=50):
            self.save_data.save_game_state(
                health=self.health,
                scores=self.scores,
                level=getattr(self, 'level', 1)
            )
            self.game_state.change(State.MENU)
            return False
        
        pygame.display.update()
        clock.tick(15)
    
    pygame.mixer.music.unpause()
    return True
