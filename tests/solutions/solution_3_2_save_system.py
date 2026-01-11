"""
Решение для Задания 3.2: Система полноценных сохранений

Этот файл показывает, как реализовать полноценную систему сохранений
для кнопки Continue.
"""

# ============================================
# ФАЙЛ: save.py (обновленный)
# ============================================

"""
import shelve
import parameters as p


class Save:
    def __init__(self):
        self.file = shelve.open('data')

    def save(self):
        # Сохраняем базовые параметры
        self.file['usr_y'] = p.usr_y

    def save_game_state(self, health, scores, level=1):
        '''Сохраняет полное состояние игры'''
        self.file['health'] = health
        self.file['scores'] = scores
        self.file['level'] = level
        self.file['game_exists'] = True  # Флаг что есть сохраненная игра
        
    def load_game_state(self):
        '''Загружает сохраненное состояние игры'''
        try:
            return {
                'health': self.file.get('health', 2),
                'scores': self.file.get('scores', 0),
                'level': self.file.get('level', 1),
                'exists': self.file.get('game_exists', False)
            }
        except KeyError:
            return None

    def clear_game_state(self):
        '''Очищает сохраненное состояние игры'''
        if 'game_exists' in self.file:
            del self.file['game_exists']
        if 'health' in self.file:
            del self.file['health']
        if 'scores' in self.file:
            del self.file['scores']
        if 'level' in self.file:
            del self.file['level']

    def add(self, name, value):
        self.file[name] = value

    def get(self, name):
        try:
            return self.file[name]
        except KeyError:
            return 0

    def __del__(self):
        self.file.close()
"""

# ============================================
# ФАЙЛ: game.py (изменения)
# ============================================

"""
В классе Game добавить следующие изменения:

1. В функции start() изменить обработку состояния CONTINUE:

    elif self.game_state.check(State.CONTINUE):
        # Загружаем сохраненное состояние
        saved_state = self.save_data.load_game_state()
        
        if saved_state and saved_state['exists']:
            # Восстанавливаем состояние
            self.health = saved_state['health']
            self.scores = saved_state['scores']
            self.level = saved_state.get('level', 1)
            self.max_scores = self.save_data.get('max')
            
            self.choose_theme()
            self.start_game()
        else:
            # Если сохранений нет, начинаем новую игру
            print_text('No saved game found!', 200, 250)
            pygame.time.delay(2000)
            self.game_state.change(State.MENU)

2. При выходе из игры (когда игрок жив) сохранять состояние:

    def pause_menu(self):
        paused = True
        pygame.mixer.music.pause()
        
        continue_button = Button(222, 70)
        save_quit_button = Button(250, 70)
        
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            
            print_text('Pause', 350, 200, font_size=60)
            
            if continue_button.draw(280, 280, 'Continue', font_size=50):
                paused = False
            if save_quit_button.draw(250, 360, 'Save & Quit', font_size=50):
                # Сохраняем текущее состояние игры
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

3. При Game Over очищать сохранение:

    def game_over(self):
        # Очищаем сохраненную игру, так как игрок проиграл
        self.save_data.clear_game_state()
        
        if self.scores > self.max_scores:
            self.max_scores = self.scores

        stopped = True
        while stopped:
            # ... остальной код ...
"""

# ============================================
# ТЕСТИРОВАНИЕ
# ============================================

"""
Чтобы проверить, что система сохранений работает:

1. Запусти игру
2. Наиграй немного очков
3. Нажми ESC
4. Выбери "Save & Quit"
5. Вернись в главное меню
6. Нажми "Continue"
7. Проверь, что игра продолжилась с сохраненными очками и здоровьем

Если игрок умирает, сохранение должно автоматически удалиться.
"""

print("Решение для Задания 3.2 загружено!")
print("Смотри комментарии в этом файле для реализации.")
