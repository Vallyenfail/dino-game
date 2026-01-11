"""
Тесты для заданий уровня 1 (Легко) - Персонализация
"""
import os
import sys
from test_helpers import check_file_exists, check_value_in_file, print_test_result, get_file_content

# Путь к корневой папке проекта
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_1_1_dino_images():
    """Задание 1.1: Проверка наличия картинок динозавра"""
    print("\n--- Задание 1.1: Замена картинок динозавра ---")
    
    dino_files = ['Dino1.jpg', 'Dino2.jpg', 'Dino3.jpg', 'Dino_jump.jpg', 'Dino_jump2.jpg']
    all_exist = True
    
    for dino_file in dino_files:
        filepath = os.path.join(PROJECT_ROOT, 'Dino', dino_file)
        exists = check_file_exists(filepath)
        if not exists:
            all_exist = False
        print_test_result(f"Файл {dino_file} существует", exists)
    
    return all_exist


def test_1_2_music_file():
    """Задание 1.2: Проверка музыкального файла"""
    print("\n--- Задание 1.2: Замена фоновой музыки ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        # Проверяем наличие строки загрузки музыки
        has_music_load = "pygame.mixer.music.load" in content
        print_test_result("В game.py есть загрузка музыки", has_music_load)
        
        # Проверяем, что музыкальный файл существует
        music_files = ['Opening.mp3']  # По умолчанию
        music_exists = False
        for music_file in music_files:
            filepath = os.path.join(PROJECT_ROOT, 'Music', music_file)
            if check_file_exists(filepath):
                music_exists = True
                print_test_result(f"Файл музыки {music_file} существует", True)
                break
        
        return has_music_load and music_exists
    
    return False


def test_1_3_button_colors():
    """Задание 1.3: Проверка изменения цветов кнопок"""
    print("\n--- Задание 1.3: Изменение цвета кнопок ---")
    
    button_file = os.path.join(PROJECT_ROOT, 'Button.py')
    content = get_file_content(button_file)
    
    if content:
        has_inactive = "inactive_color" in content
        has_active = "active_color" in content
        
        print_test_result("Параметр inactive_color определен", has_inactive)
        print_test_result("Параметр active_color определен", has_active)
        
        return has_inactive and has_active
    
    return False


def test_1_4_window_size():
    """Задание 1.4: Проверка размера окна"""
    print("\n--- Задание 1.4: Изменение размера окна ---")
    
    params_file = os.path.join(PROJECT_ROOT, 'parameters.py')
    content = get_file_content(params_file)
    
    if content:
        has_width = "display_width" in content
        has_height = "display_height" in content
        
        print_test_result("Параметр display_width определен", has_width)
        print_test_result("Параметр display_height определен", has_height)
        
        return has_width and has_height
    
    return False


def test_1_5_cactus_speed():
    """Задание 1.5: Проверка скорости кактусов"""
    print("\n--- Задание 1.5: Изменение скорости кактусов ---")
    
    game_file = os.path.join(PROJECT_ROOT, 'game.py')
    content = get_file_content(game_file)
    
    if content:
        has_function = "create_cactus_arr" in content
        has_object = "Object(" in content
        
        print_test_result("Функция create_cactus_arr существует", has_function)
        print_test_result("Создаются объекты Object", has_object)
        
        return has_function and has_object
    
    return False


def test_1_6_jump_sound():
    """Задание 1.6: Проверка звука прыжка"""
    print("\n--- Задание 1.6: Замена звука прыжка ---")
    
    sounds_file = os.path.join(PROJECT_ROOT, 'sounds.py')
    content = get_file_content(sounds_file)
    
    if content:
        has_jump_sound = "jump_sound" in content
        print_test_result("Переменная jump_sound определена", has_jump_sound)
        
        # Проверяем наличие звукового файла
        jump_file = os.path.join(PROJECT_ROOT, 'Music', 'Jump.mp3')
        file_exists = check_file_exists(jump_file)
        print_test_result("Файл Jump.mp3 существует", file_exists)
        
        return has_jump_sound and file_exists
    
    return False


def run_all_level1_tests():
    """Запускает все тесты уровня 1"""
    print("=" * 60)
    print("ТЕСТЫ УРОВНЯ 1 - ПЕРСОНАЛИЗАЦИЯ (ЛЕГКО)")
    print("=" * 60)
    
    results = [
        test_1_1_dino_images(),
        test_1_2_music_file(),
        test_1_3_button_colors(),
        test_1_4_window_size(),
        test_1_5_cactus_speed(),
        test_1_6_jump_sound()
    ]
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"РЕЗУЛЬТАТЫ: {passed}/{total} тестов пройдено")
    print("=" * 60)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_level1_tests()
    sys.exit(0 if success else 1)
