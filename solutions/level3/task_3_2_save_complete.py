"""
Задание 3.2: Полный файл save.py с системой сохранений

ИНСТРУКЦИЯ:
Этот файл можно использовать как ПОЛНУЮ ЗАМЕНУ вашего save.py

1. Сделайте резервную копию вашего save.py
2. Скопируйте содержимое этого файла
3. Замените им содержимое вашего save.py
4. Затем примените изменения в game.py (смотри task_3_2_save_system.py)
"""

import shelve
import parameters as p


class Save:
    """
    Класс для сохранения и загрузки данных игры
    
    Использует shelve для хранения данных в файле 'data'
    Поддерживает сохранение максимального счёта и полного состояния игры
    """
    
    def __init__(self):
        """Инициализация - открывает файл для сохранений"""
        self.file = shelve.open('data')

    def save(self):
        """
        Сохраняет базовые параметры игры
        (используется для сохранения позиции игрока)
        """
        self.file['usr_y'] = p.usr_y

    def add(self, name, value):
        """
        Добавляет произвольное значение в сохранение
        
        Args:
            name: Ключ для сохранения
            value: Значение для сохранения
        
        Пример:
            save.add('max', 100)  # Сохраняет максимальный счёт
        """
        self.file[name] = value

    def get(self, name):
        """
        Получает значение из сохранения по ключу
        
        Args:
            name: Ключ для получения
        
        Returns:
            Сохранённое значение или 0 если ключ не найден
        
        Пример:
            max_score = save.get('max')  # Получает максимальный счёт
        """
        try:
            return self.file[name]
        except KeyError:
            return 0
    
    # ========================================================================
    # МЕТОДЫ ДЛЯ СИСТЕМЫ ПОЛНОЦЕННЫХ СОХРАНЕНИЙ (ЗАДАНИЕ 3.2)
    # ========================================================================
    
    def save_game_state(self, health, scores, level=1):
        """
        Сохраняет полное состояние игры для продолжения
        
        Args:
            health (int): Текущее количество жизней игрока
            scores (int): Текущие очки игрока
            level (int): Текущий уровень сложности (по умолчанию 1)
        
        Пример использования:
            save_data.save_game_state(health=3, scores=150, level=2)
        """
        self.file['health'] = health
        self.file['scores'] = scores
        self.file['level'] = level
        self.file['game_exists'] = True  # Флаг наличия сохранённой игры
    
    def load_game_state(self):
        """
        Загружает сохранённое состояние игры
        
        Returns:
            dict: Словарь с ключами:
                - 'health': количество жизней (по умолчанию 2)
                - 'scores': текущие очки (по умолчанию 0)
                - 'level': текущий уровень (по умолчанию 1)
                - 'exists': есть ли сохранение (True/False)
        
        Пример использования:
            state = save_data.load_game_state()
            if state['exists']:
                self.health = state['health']
                self.scores = state['scores']
        """
        try:
            return {
                'health': self.file.get('health', 2),
                'scores': self.file.get('scores', 0),
                'level': self.file.get('level', 1),
                'exists': self.file.get('game_exists', False)
            }
        except KeyError:
            # Если что-то пошло не так, возвращаем значения по умолчанию
            return {
                'health': 2,
                'scores': 0,
                'level': 1,
                'exists': False
            }
    
    def clear_game_state(self):
        """
        Очищает сохранённое состояние игры
        
        Используется при Game Over - удаляет сохранение чтобы
        кнопка Continue не загружала проигранную игру
        
        Пример использования:
            # В методе game_over():
            self.save_data.clear_game_state()
        """
        keys_to_delete = ['game_exists', 'health', 'scores', 'level']
        for key in keys_to_delete:
            if key in self.file:
                del self.file[key]
    
    def has_saved_game(self):
        """
        Проверяет наличие сохранённой игры
        
        Returns:
            bool: True если есть активное сохранение, False иначе
        
        Пример использования:
            if save_data.has_saved_game():
                # Показать кнопку Continue
            else:
                # Скрыть кнопку Continue
        """
        try:
            return self.file.get('game_exists', False)
        except KeyError:
            return False

    def __del__(self):
        """
        Деструктор - автоматически закрывает файл при удалении объекта
        Вызывается Python когда объект больше не нужен
        """
        self.file.close()


# ============================================================================
# ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ
# ============================================================================

"""
# Создание объекта сохранения
save_data = Save()

# Сохранение состояния игры (например, в меню паузы)
save_data.save_game_state(health=3, scores=150, level=2)

# Загрузка состояния игры (например, при нажатии Continue)
state = save_data.load_game_state()
if state['exists']:
    self.health = state['health']
    self.scores = state['scores']
    print(f"Игра загружена: {state['health']} жизней, {state['scores']} очков")
else:
    print("Сохранений не найдено")

# Проверка наличия сохранения
if save_data.has_saved_game():
    print("Есть сохранённая игра!")

# Очистка сохранения (например, при Game Over)
save_data.clear_game_state()

# Сохранение максимального счёта (как раньше)
save_data.add('max', 200)
max_score = save_data.get('max')
"""
