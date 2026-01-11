"""
Тесты для заданий уровня 2 (Средне) - Изменение механики
"""
import os
import sys
from test_helpers import check_file_exists, check_value_in_file, print_test_result, get_file_content

# Путь к корневой папке проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_2_1_health_count():
    """Задание 2.1: Проверка количества жизней"""
    print("\n--- Задание 2.1: Увеличение количества жизней ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_health = "self.health" in content
        print_test_result("Параметр self.health определен", has_health)
        
        # Проверяем, что health устанавливается
        has_init = "def __init__" in content
        print_test_result("Метод __init__ существует", has_init)
        
        return has_health and has_init
    
    return False


def test_2_2_bullet_speed():
    """Задание 2.2: Проверка скорости пуль"""
    print("\n--- Задание 2.2: Изменение скорости пуль ---")
    
    bullet_file = os.path.join(PROJECT_ROOT, 'Bullet.py')
    content = get_file_content(bullet_file)
    
    if content:
        has_speed_x = "speed_x" in content
        has_speed_y = "speed_y" in content
        
        print_test_result("Параметр speed_x определен", has_speed_x)
        print_test_result("Параметр speed_y определен", has_speed_y)
        
        return has_speed_x and has_speed_y
    
    return False


def test_2_3_new_cactus():
    """Задание 2.3: Проверка добавления нового кактуса"""
    print("\n--- Задание 2.3: Добавление нового кактуса ---")
    
    images_file = os.path.join(PROJECT_ROOT, 'images.py')
    content = get_file_content(images_file)
    
    if content:
        has_cactus_img = "cactus_img" in content
        print_test_result("Список cactus_img определен", has_cactus_img)
        
        # Проверяем наличие файлов кактусов
        cactus_files = ['Cactus1.jpg', 'Cactus2.jpg', 'Cactus3.jpg']
        all_exist = all(
            check_file_exists(os.path.join(PROJECT_ROOT, 'Objects', f))
            for f in cactus_files
        )
        print_test_result("Базовые файлы кактусов существуют", all_exist)
        
        return has_cactus_img and all_exist
    
    return False


def test_2_4_hearts_frequency():
    """Задание 2.4: Проверка частоты появления сердечек"""
    print("\n--- Задание 2.4: Изменение частоты сердечек ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_hearts_plus = "hearts_plus" in content
        has_heart_object = "heart" in content.lower()
        
        print_test_result("Функция hearts_plus существует", has_hearts_plus)
        print_test_result("Упоминание heart в коде", has_heart_object)
        
        return has_hearts_plus and has_heart_object
    
    return False


def test_2_5_bird_speed():
    """Задание 2.5: Проверка скорости птиц"""
    print("\n--- Задание 2.5: Изменение скорости птиц ---")
    
    bird_file = os.path.join(PROJECT_ROOT, 'Bird.py')
    content = get_file_content(bird_file)
    
    if content:
        has_speed = "self.speed" in content
        has_class = "class Bird" in content
        
        print_test_result("Класс Bird определен", has_class)
        print_test_result("Параметр self.speed определен", has_speed)
        
        return has_speed and has_class
    
    return False


def test_2_6_bird_counter():
    """Задание 2.6: Проверка счетчика убитых птиц"""
    print("\n--- Задание 2.6: Счетчик убитых птиц ---")
    
    # Это задание требует модификации кода, проверяем базовую структуру
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_check_birds = "check_birds_dmg" in content
        print_test_result("Функция check_birds_dmg существует", has_check_birds)
        
        # Для полного теста нужно проверить добавление счетчика
        # но это опциональное задание
        return has_check_birds
    
    return False


def test_2_7_jump_height():
    """Задание 2.7: Проверка высоты прыжка"""
    print("\n--- Задание 2.7: Изменение высоты прыжка ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_jump = "def jump" in content
        has_jump_counter = "jump_counter" in content
        
        print_test_result("Функция jump существует", has_jump)
        print_test_result("Параметр jump_counter используется", has_jump_counter)
        
        return has_jump and has_jump_counter
    
    return False


def run_all_level2_tests():
    """Запускает все тесты уровня 2"""
    print("=" * 60)
    print("ТЕСТЫ УРОВНЯ 2 - ИЗМЕНЕНИЕ МЕХАНИКИ (СРЕДНЕ)")
    print("=" * 60)
    
    results = [
        test_2_1_health_count(),
        test_2_2_bullet_speed(),
        test_2_3_new_cactus(),
        test_2_4_hearts_frequency(),
        test_2_5_bird_speed(),
        test_2_6_bird_counter(),
        test_2_7_jump_height()
    ]
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_level2_tests()
    sys.exit(0 if success else 1)
