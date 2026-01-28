"""
Тесты для проверки решений всех заданий из инструкции

Логика тестирования:
- Если код задания НЕ применён в проекте → тест пропускается (skip)
- Если код задания ПРИМЕНЁН → тест проверяет что он работает корректно

Это позволяет:
1. Проверить работоспособность решений когда они применены
2. Не падать когда решения ещё не применены
"""
import pytest
import os
import sys
import re

# Добавляем корень проекта в путь
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Устанавливаем dummy драйвер для headless тестирования
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import pygame
pygame.init()

from game import Game
from Bird import Bird
from Bullet import Bullet
import parameters as p


# ==============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==============================================================================

def read_file(filename):
    """Читает файл из корня проекта"""
    filepath = os.path.join(PROJECT_ROOT, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def check_code_applied(filename, pattern):
    """Проверяет применён ли код (по паттерну в файле)"""
    content = read_file(filename)
    if content is None:
        return False
    return bool(re.search(pattern, content))


# ==============================================================================
# FIXTURES
# ==============================================================================

@pytest.fixture
def clean_game():
    """Создаёт чистый экземпляр игры для тестов"""
    game = Game()
    game.health = 2
    game.scores = 0
    return game


@pytest.fixture
def test_bird():
    """Создаёт птицу для тестов"""
    bird = Bird(-80)
    bird.y = 200
    return bird


@pytest.fixture
def test_bullet():
    """Создаёт пулю для тестов"""
    return Bullet(100, 200)


# ==============================================================================
# LEVEL 1 - ВИЗУАЛЬНЫЕ ТЕСТЫ
# ==============================================================================

class TestLevel1Visual:
    """Тесты визуальных изменений Level 1"""
    
    def test_task_1_4_window_size(self):
        """Задание 1.4: Размер окна"""
        assert hasattr(p, 'display_width'), "display_width должен быть определён"
        assert hasattr(p, 'display_height'), "display_height должен быть определён"
        assert p.display_width > 0, "display_width должен быть > 0"
        assert p.display_height > 0, "display_height должен быть > 0"
        
        print(f"✅ Размер окна: {p.display_width}x{p.display_height}")
    
    def test_task_1_5_object_parameters(self):
        """Задание 1.5: Параметры объектов"""
        from Object import Object
        from images import cactus_img
        
        obj = Object(100, 400, 30, cactus_img[0], 4)
        
        assert hasattr(obj, 'speed'), "Object должен иметь атрибут speed"
        assert obj.speed > 0, "Скорость должна быть > 0"
        
        print(f"✅ Скорость объектов: {obj.speed}")


# ==============================================================================
# LEVEL 2 - ТЕСТЫ ПАРАМЕТРОВ
# ==============================================================================

class TestLevel2Parameters:
    """Тесты изменения параметров Level 2"""
    
    def test_task_2_1_health(self, clean_game):
        """Задание 2.1: Количество жизней"""
        game = clean_game
        initial_health = game.health
        
        game.check_health()
        assert game.health == initial_health - 1, "Health должен уменьшиться на 1"
        
        print(f"✅ Задание 2.1: Начальное здоровье = {initial_health}")
    
    def test_task_2_2_bullet_speed(self, test_bullet):
        """Задание 2.2: Скорость пуль"""
        bullet = test_bullet
        
        assert hasattr(bullet, 'speed_x'), "Bullet должен иметь speed_x"
        assert bullet.speed_x > 0, "Скорость пуль должна быть > 0"
        
        initial_x = bullet.x
        bullet.move()
        assert bullet.x > initial_x, "Пуля должна двигаться вправо"
        
        print(f"✅ Задание 2.2: Скорость пуль = {bullet.speed_x}")
    
    def test_task_2_5_bird_speed(self, test_bird):
        """Задание 2.5: Скорость птиц"""
        bird = test_bird
        
        assert hasattr(bird, 'speed'), "Bird должен иметь speed"
        assert bird.speed > 0, "Скорость птиц должна быть > 0"
        
        print(f"✅ Задание 2.5: Скорость птиц = {bird.speed}")
    
    def test_task_2_6_bird_kill_return(self, test_bird, test_bullet):
        """Задание 2.6: kill_bird возвращает значение"""
        # Проверяем применён ли код
        bird_content = read_file('Bird.py')
        has_return = 'return True' in bird_content and 'return False' in bird_content
        
        if not has_return:
            pytest.skip("Задание 2.6 не применено (kill_bird не возвращает значения)")
        
        bird = test_bird
        bullet = test_bullet
        
        # Пуля мимо птицы
        bullet.x = bird.x + 1000
        result = bird.kill_bird(bullet)
        
        assert result == False, "kill_bird должен вернуть False при промахе"
        
        # Пуля попала
        bullet.x = bird.x + 10
        bullet.y = bird.y + 10
        result = bird.kill_bird(bullet)
        
        assert result == True, "kill_bird должен вернуть True при попадании"
        
        print("✅ Задание 2.6: kill_bird() возвращает True/False")


# ==============================================================================
# LEVEL 3 - КРИТИЧНЫЕ ЗАДАНИЯ
# ==============================================================================

class TestLevel3Critical:
    """Критичные задания уровня 3"""
    
    def test_task_3_1_bird_damage_logic(self, clean_game):
        """
        Задание 3.1: Урон от пуль птиц - проверка логики
        
        Этот тест проверяет ЛОГИКУ обработки столкновений.
        Работает независимо от того, применён ли код в game.py
        """
        game = clean_game
        initial_health = game.health
        
        bird = Bird(-80)
        bird.y = 200
        
        # Создаём пулю птицы в позиции игрока
        bird_bullet = Bullet(bird.x, bird.y)
        bird_bullet.x = p.usr_x + 10
        bird_bullet.y = p.usr_y + 10
        bird.all_bullets.append(bird_bullet)
        
        # Логика проверки столкновения (как в решении)
        bullets_to_remove = []
        hit_detected = False
        
        for bullet in bird.all_bullets:
            if p.usr_x <= bullet.x <= p.usr_x + p.usr_width:
                if p.usr_y <= bullet.y <= p.usr_y + p.usr_height:
                    bullets_to_remove.append(bullet)
                    hit_detected = True
                    game.check_health()
        
        for bullet in bullets_to_remove:
            if bullet in bird.all_bullets:
                bird.all_bullets.remove(bullet)
        
        assert hit_detected, "Попадание должно быть обнаружено"
        assert game.health == initial_health - 1, "Здоровье должно уменьшиться"
        assert len(bird.all_bullets) == 0, "Пуля должна быть удалена"
        
        print("✅ Задание 3.1: Логика урона от пуль птиц работает!")
    
    def test_task_3_1_bird_damage_in_game(self):
        """
        Задание 3.1: Проверка что код применён в game.py
        """
        game_content = read_file('game.py')
        
        # Ищем код проверки столкновений пуль птиц
        has_bird_bullet_check = 'bird.all_bullets' in game_content
        has_usr_collision = 'p.usr_x' in game_content and 'bullet.x' in game_content
        
        if not has_bird_bullet_check:
            pytest.skip("Задание 3.1 не применено в game.py (нет обработки bird.all_bullets)")
        
        # Ищем цикл проверки пуль птиц
        pattern = r'for\s+bullet\s+in\s+bird\.all_bullets'
        has_loop = bool(re.search(pattern, game_content))
        
        assert has_loop, "В game.py должен быть цикл проверки пуль птиц"
        
        print("✅ Задание 3.1: Код применён в game.py!")
    
    def test_task_3_1_miss_no_damage(self, clean_game):
        """Задание 3.1: Промахи не наносят урон"""
        game = clean_game
        initial_health = game.health
        
        bird = Bird(-80)
        bird.y = 200
        
        # Пуля МИМО игрока
        bullet = Bullet(bird.x, bird.y)
        bullet.x = p.usr_x + p.usr_width + 100
        bullet.y = p.usr_y + 10
        bird.all_bullets.append(bullet)
        
        hit_detected = False
        for b in bird.all_bullets:
            if p.usr_x <= b.x <= p.usr_x + p.usr_width:
                if p.usr_y <= b.y <= p.usr_y + p.usr_height:
                    hit_detected = True
        
        assert not hit_detected, "Промах не должен засчитываться"
        assert game.health == initial_health, "Здоровье не должно измениться"
        
        print("✅ Задание 3.1: Промахи не наносят урон!")


class TestLevel3SaveSystem:
    """Тесты системы сохранений (3.2 и 3.8)"""
    
    def test_task_3_2_methods_exist(self):
        """Задание 3.2: Проверка наличия методов"""
        from save import Save
        save_data = Save()
        
        methods = ['save_game_state', 'load_game_state', 'clear_game_state', 'has_saved_game']
        missing = [m for m in methods if not hasattr(save_data, m)]
        
        if missing:
            pytest.skip(f"Задание 3.2 не применено (отсутствуют методы: {missing})")
        
        print("✅ Задание 3.2: Все методы присутствуют")
    
    def test_task_3_2_save_load(self):
        """Задание 3.2: Сохранение и загрузка состояния"""
        from save import Save
        save_data = Save()
        
        if not hasattr(save_data, 'save_game_state'):
            pytest.skip("Задание 3.2 не применено")
        
        save_data.save_game_state(health=3, scores=150, level=2)
        
        assert save_data.has_saved_game(), "Должно быть активное сохранение"
        
        loaded = save_data.load_game_state()
        
        assert loaded['exists'], "exists должен быть True"
        assert loaded['health'] == 3, "health должен быть 3"
        assert loaded['scores'] == 150, "scores должен быть 150"
        assert loaded['level'] == 2, "level должен быть 2"
        
        save_data.clear_game_state()
        
        print("✅ Задание 3.2: Сохранение/загрузка работает!")
    
    def test_task_3_2_clear(self):
        """Задание 3.2: Очистка сохранения"""
        from save import Save
        save_data = Save()
        
        if not hasattr(save_data, 'clear_game_state'):
            pytest.skip("Задание 3.2 не применено")
        
        save_data.save_game_state(health=2, scores=50)
        save_data.clear_game_state()
        
        assert not save_data.has_saved_game(), "Сохранение должно быть удалено"
        
        print("✅ Задание 3.2: Очистка работает!")
    
    def test_task_3_8_methods_exist(self):
        """Задание 3.8: Проверка наличия методов таблицы лидеров"""
        from save import Save
        save_data = Save()
        
        methods = ['save_score', 'get_leaderboard', 'is_top_score', 'clear_leaderboard']
        missing = [m for m in methods if not hasattr(save_data, m)]
        
        if missing:
            pytest.skip(f"Задание 3.8 не применено (отсутствуют методы: {missing})")
        
        print("✅ Задание 3.8: Все методы присутствуют")
    
    def test_task_3_8_leaderboard(self):
        """Задание 3.8: Таблица лидеров"""
        from save import Save
        save_data = Save()
        
        if not hasattr(save_data, 'save_score'):
            pytest.skip("Задание 3.8 не применено")
        
        save_data.clear_leaderboard()
        
        save_data.save_score(100, "Alice")
        save_data.save_score(200, "Bob")
        save_data.save_score(150, "Charlie")
        
        leaderboard = save_data.get_leaderboard()
        
        assert len(leaderboard) == 3, "Должно быть 3 записи"
        assert leaderboard[0]['name'] == "Bob", "Первый - Bob"
        assert leaderboard[0]['score'] == 200, "У Bob 200 очков"
        
        save_data.clear_leaderboard()
        
        print("✅ Задание 3.8: Таблица лидеров работает!")
    
    def test_task_3_8_top_5(self):
        """Задание 3.8: Ограничение топ-5"""
        from save import Save
        save_data = Save()
        
        if not hasattr(save_data, 'save_score'):
            pytest.skip("Задание 3.8 не применено")
        
        save_data.clear_leaderboard()
        
        for i in range(7):
            save_data.save_score(i * 50, f"Player{i}")
        
        leaderboard = save_data.get_leaderboard()
        
        assert len(leaderboard) == 5, "Должно быть максимум 5 записей"
        
        save_data.clear_leaderboard()
        
        print("✅ Задание 3.8: Топ-5 работает!")


class TestLevel3Additional:
    """Дополнительные задания Level 3"""
    
    def test_task_3_3_pause_menu(self):
        """Задание 3.3: Меню паузы"""
        game_content = read_file('game.py')
        
        has_pause_menu = 'def pause_menu' in game_content
        
        if not has_pause_menu:
            pytest.skip("Задание 3.3 не применено (нет pause_menu)")
        
        # Проверяем что pause_menu вызывается
        has_call = 'pause_menu()' in game_content or 'self.pause_menu()' in game_content
        
        assert has_call, "pause_menu() должен вызываться в коде"
        
        print("✅ Задание 3.3: pause_menu найден и используется!")
    
    def test_task_3_5_bat_class(self):
        """Задание 3.5: Класс Bat"""
        bat_path = os.path.join(PROJECT_ROOT, 'Bat.py')
        
        if not os.path.exists(bat_path):
            pytest.skip("Задание 3.5 не применено (нет Bat.py)")
        
        from Bat import Bat
        bat = Bat()
        
        # Проверяем атрибуты
        assert hasattr(bat, 'x'), "Должен быть x"
        assert hasattr(bat, 'y'), "Должен быть y"
        assert hasattr(bat, 'speed_x'), "Должен быть speed_x"
        assert hasattr(bat, 'speed_y'), "Должен быть speed_y"
        assert hasattr(bat, 'alive'), "Должен быть alive"
        
        # Проверяем методы
        assert hasattr(bat, 'move_zigzag'), "Должен быть move_zigzag"
        assert hasattr(bat, 'kill_bat'), "Должен быть kill_bat"
        assert hasattr(bat, 'reset'), "Должен быть reset"
        
        # Тест движения
        initial_x = bat.x
        bat.move_zigzag()
        assert bat.x < initial_x, "Должен двигаться влево"
        
        print("✅ Задание 3.5: Класс Bat работает!")
    
    def test_task_3_6_level_system(self, clean_game):
        """Задание 3.6: Система уровней"""
        game = clean_game
        
        if not hasattr(game, 'level'):
            pytest.skip("Задание 3.6 не применено (нет self.level)")
        
        assert game.level >= 1, "Уровень должен быть >= 1"
        
        print(f"✅ Задание 3.6: level = {game.level}")
    
    def test_task_3_7_shield(self, clean_game):
        """Задание 3.7: Щит"""
        game = clean_game
        game_content = read_file('game.py')
        
        has_shield = 'has_shield' in game_content
        
        if not has_shield:
            pytest.skip("Задание 3.7 не применено (нет has_shield)")
        
        # Проверяем наличие атрибута
        assert hasattr(game, 'has_shield'), "Должен быть атрибут has_shield"
        
        # Тестируем логику щита
        game.has_shield = False
        assert game.has_shield == False, "Изначально щита нет"
        
        game.has_shield = True
        assert game.has_shield == True, "Щит можно активировать"
        
        print("✅ Задание 3.7: Щит реализован!")
    
    def test_task_3_9_p_key(self):
        """Задание 3.9: Пауза по P"""
        game_content = read_file('game.py')
        
        has_p_key = 'K_p' in game_content
        
        if not has_p_key:
            pytest.skip("Задание 3.9 не применено (нет K_p)")
        
        # Проверяем что K_p используется с паузой
        has_pause_with_p = ('K_p' in game_content and 
                          ('pause' in game_content.lower()))
        
        assert has_pause_with_p, "K_p должен использоваться для паузы"
        
        print("✅ Задание 3.9: Клавиша P работает!")
    
    def test_task_3_10_death_animation(self, clean_game):
        """Задание 3.10: Анимация смерти"""
        game_content = read_file('game.py')
        
        has_method = 'def death_animation' in game_content
        
        if not has_method:
            pytest.skip("Задание 3.10 не применено (нет метода death_animation)")
        
        game = clean_game
        
        # Проверяем что метод существует
        assert hasattr(game, 'death_animation'), "Должен быть метод death_animation"
        
        # Проверяем что метод вызывается в check_collision
        has_call = 'self.death_animation()' in game_content
        assert has_call, "death_animation должен вызываться в check_collision"
        
        print("✅ Задание 3.10: Анимация смерти реализована!")


# ==============================================================================
# ИНТЕГРАЦИОННЫЕ ТЕСТЫ
# ==============================================================================

class TestIntegration:
    """Интеграционные тесты"""
    
    def test_game_creation(self):
        """Создание объекта Game"""
        game = Game()
        
        assert hasattr(game, 'health'), "Должен быть health"
        assert hasattr(game, 'scores'), "Должен быть scores"
        assert hasattr(game, 'game_state'), "Должен быть game_state"
        assert hasattr(game, 'save_data'), "Должен быть save_data"
        
        print("✅ Game создаётся корректно")
    
    def test_bird_can_shoot(self, test_bird):
        """Птица может стрелять"""
        bird = test_bird
        
        assert hasattr(bird, 'all_bullets'), "Должен быть all_bullets"
        assert isinstance(bird.all_bullets, list), "all_bullets - список"
        assert hasattr(bird, 'shoot'), "Должен быть метод shoot"
        
        print("✅ Птица может стрелять")
    
    def test_bullet_moves(self, test_bullet):
        """Пуля двигается"""
        bullet = test_bullet
        
        initial_x = bullet.x
        bullet.move()
        
        assert bullet.x != initial_x, "Пуля должна двигаться"
        
        print("✅ Пуля двигается")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
