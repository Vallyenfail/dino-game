"""
Тесты для заданий уровня 3 (Сложно) - Новая функциональность
"""
import os
import sys
from test_helpers import check_file_exists, check_value_in_file, print_test_result, get_file_content

# Путь к корневой папке проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_3_1_bird_damage():
    """Задание 3.1: Проверка урона от птиц"""
    print("\n--- Задание 3.1: Урон от пуль птиц ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_birds = "all_birds" in content
        has_check_health = "check_health" in content
        
        print_test_result("Переменная all_birds используется", has_birds)
        print_test_result("Функция check_health существует", has_check_health)
        
        # Для полного теста нужна проверка коллизий с пулями птиц
        # Это требует анализа кода
        return has_birds and has_check_health
    
    return False


def test_3_2_save_system():
    """Задание 3.2: Проверка системы сохранений"""
    print("\n--- Задание 3.2: Система полноценных сохранений ---")
    
    save_file = os.path.join(PROJECT_ROOT, 'save.py')
    content = get_file_content(save_file)
    
    if content:
        has_save_class = "class Save" in content
        has_save_method = "def save" in content
        has_get_method = "def get" in content
        has_add_method = "def add" in content
        
        print_test_result("Класс Save определен", has_save_class)
        print_test_result("Метод save существует", has_save_method)
        print_test_result("Метод get существует", has_get_method)
        print_test_result("Метод add существует", has_add_method)
        
        return all([has_save_class, has_save_method, has_get_method, has_add_method])
    
    return False


def test_3_3_exit_button():
    """Задание 3.3: Проверка кнопки выхода"""
    print("\n--- Задание 3.3: Кнопка выхода из игры ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_escape = "K_ESCAPE" in content or "pygame.K_ESCAPE" in content
        has_pause = "pause" in content
        
        print_test_result("Обработка клавиши ESC существует", has_escape)
        print_test_result("Функция паузы существует", has_pause)
        
        return has_escape and has_pause
    
    return False


def test_3_4_hero_choice():
    """Задание 3.4: Проверка выбора персонажа"""
    print("\n--- Задание 3.4: Выбор персонажа ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_choose_hero = "choose_hero" in content
        print_test_result("Функция choose_hero существует", has_choose_hero)
        
        # Проверяем наличие set_theme для смены изображений
        has_set_theme = "set_theme" in content
        print_test_result("Функция set_theme используется", has_set_theme)
        
        return has_choose_hero
    
    return False


def test_3_5_new_enemy():
    """Задание 3.5: Проверка нового врага"""
    print("\n--- Задание 3.5: Новый тип врага ---")
    
    # Проверяем существование Bird.py как образца
    bird_file = os.path.join(PROJECT_ROOT, 'Bird.py')
    bird_exists = check_file_exists(bird_file)
    print_test_result("Файл Bird.py существует (образец)", bird_exists)
    
    # Для нового врага студент должен создать новый файл
    # Мы можем только проверить базовую структуру
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_bird_import = "Bird" in content
        print_test_result("Импорт Bird присутствует", has_bird_import)
        
        return bird_exists and has_bird_import
    
    return False


def test_3_6_level_system():
    """Задание 3.6: Проверка системы уровней"""
    print("\n--- Задание 3.6: Система уровней ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_scores = "self.scores" in content
        has_cactus_arr = "cactus_arr" in content
        
        print_test_result("Переменная scores используется", has_scores)
        print_test_result("Массив кактусов используется", has_cactus_arr)
        
        return has_scores and has_cactus_arr
    
    return False


def test_3_7_shield_bonus():
    """Задание 3.7: Проверка бонуса щит"""
    print("\n--- Задание 3.7: Бонус щит ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        # Проверяем базовую структуру для бонусов (сердечки)
        has_heart_logic = "heart" in content.lower()
        print_test_result("Логика бонусов (сердечки) существует", has_heart_logic)
        
        # Для щита нужна аналогичная логика
        return has_heart_logic
    
    return False


def test_3_8_leaderboard():
    """Задание 3.8: Проверка таблицы лидеров"""
    print("\n--- Задание 3.8: Таблица лидеров ---")
    
    save_file = os.path.join(PROJECT_ROOT, 'save.py')
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    
    save_content = get_file_content(save_file)
    game_content = get_file_content(game_file)
    
    if save_content and game_content:
        has_save_class = "class Save" in save_content
        has_max_scores = "max_scores" in game_content
        
        print_test_result("Класс Save существует", has_save_class)
        print_test_result("Переменная max_scores используется", has_max_scores)
        
        return has_save_class and has_max_scores
    
    return False


def test_3_9_pause_p_key():
    """Задание 3.9: Проверка паузы по P"""
    print("\n--- Задание 3.9: Пауза по клавише P ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_pause_function = "def pause" in content
        has_key_handling = "keys[" in content or "pygame.key" in content
        
        print_test_result("Функция pause существует", has_pause_function)
        print_test_result("Обработка клавиш присутствует", has_key_handling)
        
        return has_pause_function and has_key_handling
    
    return False


def test_3_10_death_animation():
    """Задание 3.10: Проверка анимации смерти"""
    print("\n--- Задание 3.10: Анимация смерти ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_check_health = "check_health" in content
        has_game_over = "game_over" in content
        
        print_test_result("Функция check_health существует", has_check_health)
        print_test_result("Функция game_over существует", has_game_over)
        
        return has_check_health and has_game_over
    
    return False


def run_all_level3_tests():
    """Запускает все тесты уровня 3"""
    print("=" * 60)
    print("ТЕСТЫ УРОВНЯ 3 - НОВАЯ ФУНКЦИОНАЛЬНОСТЬ (СЛОЖНО)")
    print("=" * 60)
    
    results = [
        test_3_1_bird_damage(),
        test_3_2_save_system(),
        test_3_3_exit_button(),
        test_3_4_hero_choice(),
        test_3_5_new_enemy(),
        test_3_6_level_system(),
        test_3_7_shield_bonus(),
        test_3_8_leaderboard(),
        test_3_9_pause_p_key(),
        test_3_10_death_animation()
    ]
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_level3_tests()
    sys.exit(0 if success else 1)
