import shelve
import parameters as p


class Save:
    def __init__(self):
        self.file = shelve.open('data')

        # self.info = {
        #     'name': 'Kanye',
        #     'age' : 24,
        #     'state': State.MENU
        # }

    def save(self):
        # self.file['Info'] = self.info  под ключом инфо записали инфо
        self.file['usr_y'] = p.usr_y

    def add(self, name, value):
        self.file[name] = value

    def get(self, name):
        try:  # попробует, если нет, то не выдаст ошибку, а выдаст ветвь except
            return self.file[name]
        except KeyError:
            return 0

        # num = self.file['Number']
        # print(num)
        # print(self.file['Info'])

    # ========================================================================
    # МЕТОДЫ ДЛЯ СИСТЕМЫ ПОЛНОЦЕННЫХ СОХРАНЕНИЙ (ЗАДАНИЕ 3.2)
    # ========================================================================
    
    def save_game_state(self, health, scores, level=1):
        """Сохраняет полное состояние игры для продолжения"""
        self.file['health'] = health
        self.file['scores'] = scores
        self.file['level'] = level
        self.file['game_exists'] = True
    
    def load_game_state(self):
        """Загружает сохранённое состояние игры"""
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
        """Очищает сохранённое состояние игры (используется при Game Over)"""
        keys_to_delete = ['game_exists', 'health', 'scores', 'level']
        for key in keys_to_delete:
            if key in self.file:
                del self.file[key]
    
    def has_saved_game(self):
        """Проверяет наличие сохранённой игры"""
        try:
            return self.file.get('game_exists', False)
        except KeyError:
            return False
    
    # ========================================================================
    # МЕТОДЫ ДЛЯ ТАБЛИЦЫ ЛИДЕРОВ (ЗАДАНИЕ 3.8)
    # ========================================================================
    
    def save_score(self, score, player_name="Player"):
        """Сохраняет результат в таблицу лидеров"""
        leaderboard = self.get_leaderboard()
        
        leaderboard.append({
            'name': player_name,
            'score': score
        })
        
        leaderboard.sort(key=lambda x: x['score'], reverse=True)
        leaderboard = leaderboard[:5]
        
        self.file['leaderboard'] = leaderboard
        return leaderboard
    
    def get_leaderboard(self):
        """Получает текущую таблицу лидеров"""
        try:
            return self.file['leaderboard']
        except KeyError:
            return []
    
    def is_top_score(self, score):
        """Проверяет попадает ли результат в топ-5"""
        leaderboard = self.get_leaderboard()
        
        if len(leaderboard) < 5:
            return True
        
        return score > leaderboard[-1]['score']
    
    def clear_leaderboard(self):
        """Полностью очищает таблицу лидеров"""
        if 'leaderboard' in self.file:
            del self.file['leaderboard']

    def __del__(self):  # деструктор
        self.file.close()
