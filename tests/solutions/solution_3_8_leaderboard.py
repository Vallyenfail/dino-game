"""
Решение для Задания 3.8: Таблица лидеров (Топ-5 результатов)

Этот файл показывает, как реализовать систему хранения и отображения
лучших результатов игры.
"""

# ============================================
# ФАЙЛ: save.py (добавить методы)
# ============================================

"""
import shelve
import parameters as p


class Save:
    def __init__(self):
        self.file = shelve.open('data')

    def save(self):
        self.file['usr_y'] = p.usr_y

    def add(self, name, value):
        self.file[name] = value

    def get(self, name):
        try:
            return self.file[name]
        except KeyError:
            return 0
    
    # НОВЫЕ МЕТОДЫ ДЛЯ ТАБЛИЦЫ ЛИДЕРОВ:
    
    def save_score(self, score, player_name="Player"):
        '''Сохраняет новый результат в таблицу лидеров'''
        # Получаем текущую таблицу лидеров
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
        
        # Сохраняем обратно
        self.file['leaderboard'] = leaderboard
        
        return leaderboard
    
    def get_leaderboard(self):
        '''Возвращает таблицу лидеров'''
        try:
            return self.file['leaderboard']
        except KeyError:
            # Если таблицы еще нет, возвращаем пустую
            return []
    
    def is_top_score(self, score):
        '''Проверяет, попал ли результат в топ-5'''
        leaderboard = self.get_leaderboard()
        
        # Если в таблице меньше 5 записей, автоматически топ
        if len(leaderboard) < 5:
            return True
        
        # Проверяем, больше ли результат самого слабого в топ-5
        return score > leaderboard[-1]['score']
    
    def clear_leaderboard(self):
        '''Очищает таблицу лидеров'''
        if 'leaderboard' in self.file:
            del self.file['leaderboard']

    def __del__(self):
        self.file.close()
"""

# ============================================
# ФАЙЛ: game.py (добавить экран таблицы лидеров)
# ============================================

"""
В классе Game добавить следующие методы:

1. Метод показа таблицы лидеров:

def show_leaderboard(self):
    '''Отображает таблицу лидеров'''
    leaderboard = self.save_data.get_leaderboard()
    
    back_button = Button(180, 70)
    clear_button = Button(280, 70)
    
    show = True
    while show:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        display.fill([0, 0, 0])  # Черный фон
        
        # Заголовок
        print_text('LEADERBOARD', 250, 50, font_size=60, font_color=(255, 215, 0))
        
        # Отображаем топ-5
        if leaderboard:
            y_position = 150
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
                
                print_text(position_text, 200, y_position, font_color=color, font_size=40)
                print_text(score_text, 500, y_position, font_color=color, font_size=40)
                
                y_position += 60
        else:
            print_text('No scores yet!', 280, 250, font_size=40)
        
        # Кнопки
        if back_button.draw(320, 500, 'Back', font_size=50):
            show = False
        
        if clear_button.draw(250, 570, 'Clear All', font_size=40):
            self.save_data.clear_leaderboard()
            leaderboard = []
        
        pygame.display.update()
        clock.tick(60)

2. Изменить метод game_over() для сохранения результата:

def game_over(self):
    if self.scores > self.max_scores:
        self.max_scores = self.scores
    
    # НОВЫЙ КОД: Проверяем, попал ли в топ-5
    is_top = self.save_data.is_top_score(self.scores)
    
    if is_top:
        # Показываем поздравление
        self.enter_name_screen()
    
    stopped = True
    while stopped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        print_text('Game over, press Enter to play again, Esc to exit', 40, 250)
        print_text('Max score: ' + str(self.max_scores), 300, 300)
        
        # НОВЫЙ КОД: Добавляем кнопку просмотра таблицы
        print_text('Press L to view Leaderboard', 230, 350, font_size=30)

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

3. Метод ввода имени для таблицы лидеров:

def enter_name_screen(self):
    '''Экран ввода имени для таблицы лидеров'''
    player_name = ""
    entering = True
    
    while entering:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(player_name) > 0:
                    # Сохраняем результат
                    self.save_data.save_score(self.scores, player_name)
                    entering = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_ESCAPE:
                    # Сохраняем с именем по умолчанию
                    self.save_data.save_score(self.scores, "Player")
                    entering = False
                elif len(player_name) < 15:  # Ограничение длины имени
                    # Добавляем только буквы и цифры
                    if event.unicode.isalnum() or event.unicode == " ":
                        player_name += event.unicode
        
        display.fill([0, 0, 0])
        
        # Поздравление
        print_text('NEW TOP SCORE!', 250, 150, font_size=50, font_color=(255, 215, 0))
        print_text(f'Score: {self.scores}', 330, 220, font_size=40)
        
        # Поле ввода имени
        print_text('Enter your name:', 270, 300, font_size=35)
        
        # Отображаем введенное имя
        name_display = player_name if player_name else "_"
        print_text(name_display, 320, 360, font_size=45, font_color=(0, 255, 0))
        
        # Подсказка
        print_text('Press Enter to save', 260, 450, font_size=25)
        print_text('Press Esc to skip', 280, 480, font_size=25)
        
        pygame.display.update()
        clock.tick(60)

4. Добавить кнопку в главное меню:

def show_menu(self):
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
        # НОВАЯ КНОПКА
        if leaderboard_button.draw(250, 340, 'Leaderboard', font_size=50):
            self.show_leaderboard()
        if quit_button.draw(358, 420, 'Quit', font_size=50):
            self.game_state.change(State.QUIT)
            return

        pygame.display.update()
        clock.tick(60)
"""

# ============================================
# ТЕСТИРОВАНИЕ
# ============================================

"""
Порядок тестирования:

1. Запусти игру
2. Наиграй любое количество очков
3. Умри (столкнись с кактусом)
4. Если результат в топ-5, появится экран ввода имени
5. Введи свое имя и нажми Enter
6. Вернись в главное меню
7. Нажми кнопку "Leaderboard"
8. Проверь, что твой результат сохранился

Проверь также:
- Попробуй набрать разные результаты (больше и меньше)
- Убедись, что таблица показывает только топ-5
- Попробуй очистить таблицу кнопкой "Clear All"
- Проверь, что после перезапуска игры результаты сохранились
"""

print("Решение для Задания 3.8 загружено!")
print("Смотри комментарии в этом файле для реализации.")
