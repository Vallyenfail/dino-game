"""
Задание 3.8: Таблица лидеров (Топ-5 результатов)

ПРОБЛЕМА:
Игра сохраняет только один максимальный счёт. Невозможно увидеть историю результатов
или соревноваться с друзьями.

РЕШЕНИЕ:
Добавить систему сохранения топ-5 результатов с именами игроков, экран ввода имени
при попадании в топ, и отображение таблицы лидеров.

Нужно изменить:
1. save.py - добавить методы для работы с таблицей лидеров
2. game.py - добавить экраны ввода имени и отображения таблицы

================================================================================
ЧАСТЬ 1: МЕТОДЫ ДЛЯ save.py
================================================================================
Добавьте эти методы в класс Save в файле save.py:
"""

# МЕТОДЫ ДЛЯ ДОБАВЛЕНИЯ В save.py:

def save_score(self, score, player_name="Player"):
    """
    Сохраняет результат в таблицу лидеров
    
    Args:
        score (int): Количество очков
        player_name (str): Имя игрока (по умолчанию "Player")
    
    Returns:
        list: Обновлённая таблица лидеров (топ-5)
    """
    # Получаем текущую таблицу
    leaderboard = self.get_leaderboard()
    
    # Добавляем новый результат
    leaderboard.append({
        'name': player_name,
        'score': score
    })
    
    # Сортируем по убыванию очков
    leaderboard.sort(key=lambda x: x['score'], reverse=True)
    
    # Оставляем только топ-5
    leaderboard = leaderboard[:5]
    
    # Сохраняем
    self.file['leaderboard'] = leaderboard
    
    return leaderboard

def get_leaderboard(self):
    """
    Получает текущую таблицу лидеров
    
    Returns:
        list: Список словарей с ключами 'name' и 'score'
              Пустой список если таблицы нет
    """
    try:
        return self.file['leaderboard']
    except KeyError:
        return []

def is_top_score(self, score):
    """
    Проверяет попадает ли результат в топ-5
    
    Args:
        score (int): Количество очков
    
    Returns:
        bool: True если результат попадает в топ-5
    """
    leaderboard = self.get_leaderboard()
    
    # Если в таблице меньше 5 записей, автоматически попадаем
    if len(leaderboard) < 5:
        return True
    
    # Проверяем больше ли результат самого слабого в топ-5
    return score > leaderboard[-1]['score']

def clear_leaderboard(self):
    """Полностью очищает таблицу лидеров"""
    if 'leaderboard' in self.file:
        del self.file['leaderboard']


"""
================================================================================
ЧАСТЬ 2: МЕТОД ВВОДА ИМЕНИ ДЛЯ game.py
================================================================================
Добавьте этот метод в класс Game:
"""

def enter_name_screen(self):
    """
    Экран ввода имени для таблицы лидеров
    Показывается когда игрок попадает в топ-5
    """
    player_name = ""
    entering = True
    
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    # Сохраняем результат с именем
                    self.save_data.save_score(self.scores, player_name)
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    # Удаляем последний символ
                    player_name = player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # Сохраняем с именем по умолчанию
                    self.save_data.save_score(self.scores, "Player")
                    entering = False
                elif len(player_name) < 15:  # Ограничение длины имени
                    # Добавляем только буквы, цифры и пробелы
                    if event.unicode.isalnum() or event.unicode == " ":
                        player_name += event.unicode
        
        display.fill([0, 0, 0])
        
        # Заголовок
        print_text('NEW TOP SCORE!', 230, 120, font_size=55, font_color=(255, 215, 0))
        print_text(f'Score: {self.scores}', 320, 190, font_size=45)
        
        # Поле ввода
        print_text('Enter your name:', 260, 270, font_size=35)
        
        # Отображаем введённое имя
        name_display = player_name if player_name else "_"
        print_text(name_display, 300, 330, font_size=45, font_color=(0, 255, 0))
        
        # Подсказки
        print_text('Press Enter to save', 250, 430, font_size=28)
        print_text('Press Esc to skip', 270, 465, font_size=28)
        
        pygame.display.update()
        clock.tick(60)


"""
================================================================================
ЧАСТЬ 3: МЕТОД ОТОБРАЖЕНИЯ ТАБЛИЦЫ ДЛЯ game.py
================================================================================
Добавьте этот метод в класс Game:
"""

def show_leaderboard(self):
    """Отображает таблицу лидеров с топ-5 результатами"""
    leaderboard = self.save_data.get_leaderboard()
    
    back_button = Button(180, 70)
    clear_button = Button(280, 70)
    
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        display.fill([0, 0, 0])
        
        # Заголовок
        print_text('LEADERBOARD', 230, 40, font_size=65, font_color=(255, 215, 0))
        
        # Отображаем топ-5
        if leaderboard:
            y_position = 140
            for i, entry in enumerate(leaderboard, 1):
                # Место, имя и очки
                position_text = f"{i}. {entry['name']}"
                score_text = f"{entry['score']} pts"
                
                # Цвет в зависимости от места
                if i == 1:
                    color = (255, 215, 0)  # Золото
                elif i == 2:
                    color = (192, 192, 192)  # Серебро
                elif i == 3:
                    color = (205, 127, 50)  # Бронза
                else:
                    color = (255, 255, 255)  # Белый
                
                # Отображаем позицию и имя слева
                print_text(position_text, 150, y_position, font_color=color, font_size=42)
                # Отображаем очки справа
                print_text(score_text, 480, y_position, font_color=color, font_size=42)
                
                y_position += 65
        else:
            print_text('No scores yet!', 260, 250, font_size=45)
            print_text('Be the first to play!', 230, 310, font_size=35)
        
        # Кнопки
        if back_button.draw(315, 490, 'Back', font_size=50):
            show = False
        
        if clear_button.draw(240, 560, 'Clear All', font_size=42):
            # Очищаем таблицу
            self.save_data.clear_leaderboard()
            leaderboard = []
        
        pygame.display.update()
        clock.tick(60)


"""
================================================================================
ЧАСТЬ 4: ИЗМЕНЕНИЕ game_over() В game.py
================================================================================
Найдите метод game_over() и измените его начало:
"""

def game_over_updated(self):
    """Обновлённый метод game_over с проверкой топ-5"""
    # Обновляем максимальный счёт
    if self.scores > self.max_scores:
        self.max_scores = self.scores
    
    # НОВЫЙ КОД: Проверяем попадание в топ-5
    is_top = self.save_data.is_top_score(self.scores)
    
    if is_top and self.scores > 0:  # Только если набрали хоть какие-то очки
        # Показываем экран ввода имени
        self.enter_name_screen()
    
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over, press Enter to play again, Esc to exit', 40, 250)
        print_text('Max score: ' + str(self.max_scores), 300, 300)
        
        # НОВЫЙ КОД: Подсказка для просмотра таблицы
        print_text('Press L to view Leaderboard', 220, 360, font_size=32)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            return True
        if keys[pygame.K_ESCAPE]:
            self.game_state.change(State.QUIT)
            return False
        # НОВЫЙ КОД: Открываем таблицу по L
        if keys[pygame.K_l]:
            self.show_leaderboard()

        pygame.display.update()
        clock.tick(15)


"""
================================================================================
ЧАСТЬ 5: ДОБАВЛЕНИЕ КНОПКИ В ГЛАВНОЕ МЕНЮ
================================================================================
Найдите метод show_menu() и обновите его:
"""

def show_menu_updated(self):
    """Обновлённое главное меню с кнопкой Leaderboard"""
    menu_background = pygame.image.load('Effects and background/Cat.jpg')

    start_button = Button(288, 70)
    continue_button = Button(222, 70)
    leaderboard_button = Button(280, 70)  # НОВАЯ КНОПКА
    quit_button = Button(120, 70)

    show = True

    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        display.blit(menu_background, (0, 0))
        
        if start_button.draw(270, 180, 'Start game', font_size=50):
            self.game_state.change(State.START)
            return
        if continue_button.draw(300, 260, 'Continue', font_size=50):
            self.game_state.change(State.CONTINUE)
            return
        # НОВАЯ КНОПКА: Таблица лидеров
        if leaderboard_button.draw(240, 340, 'Leaderboard', font_size=50):
            self.show_leaderboard()  # Показываем таблицу, не выходя из меню
        if quit_button.draw(358, 420, 'Quit', font_size=50):
            self.game_state.change(State.QUIT)
            return

        pygame.display.update()
        clock.tick(60)


"""
================================================================================
ОЖИДАЕМЫЙ РЕЗУЛЬТАТ
================================================================================

✅ После игры с хорошим результатом появляется экран ввода имени
✅ В главном меню есть кнопка "Leaderboard"
✅ Таблица показывает топ-5 результатов с именами
✅ Места 1-3 окрашены золотом, серебром и бронзой
✅ В Game Over можно нажать L для просмотра таблицы
✅ Есть кнопка очистки всей таблицы

КАК ПРОВЕРИТЬ:
1. Запустите игру несколько раз, набирая разные результаты
2. При попадании в топ-5 введите своё имя
3. В главном меню нажмите "Leaderboard"
4. Проверьте что таблица сохраняется после перезапуска игры
5. Попробуйте очистить таблицу кнопкой "Clear All"
"""
