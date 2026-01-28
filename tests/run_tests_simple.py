"""
Простой запуск тестов без pytest
Запускает все тесты и выводит результаты
"""
import sys
import os

# Добавляем корневую папку проекта в путь
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import pygame

# Инициализация pygame
pygame.init()
pygame.display.set_mode((800, 600))

# Импортируем тестовый класс
from test_solutions import TestLevel3Critical

# Создаём экземпляр класса
test_class = TestLevel3Critical()

# Список тестов для запуска
tests = [
    ("Задание 3.1: Урон от пуль птиц", test_class.test_task_3_1_bird_damage),
    ("Задание 3.1: Множественные попадания", test_class.test_task_3_1_multiple_hits),
    ("Задание 3.1: Промахи", test_class.test_task_3_1_miss),
    ("Задание 3.2: Сохранение состояния", test_class.test_task_3_2_save_game_state),
    ("Задание 3.2: Очистка сохранений", test_class.test_task_3_2_clear_save),
    ("Задание 3.2: Кнопка Continue", test_class.test_task_3_2_continue_button),
    ("Задание 3.8: Сохранение в таблицу", test_class.test_task_3_8_save_score),
    ("Задание 3.8: Ограничение топ-5", test_class.test_task_3_8_top_5_limit),
    ("Задание 3.8: Проверка попадания в топ", test_class.test_task_3_8_is_top_score),
    ("Задание 3.8: Очистка таблицы", test_class.test_task_3_8_clear_leaderboard),
]

# Запускаем тесты
print("=" * 80)
print("ЗАПУСК ТЕСТОВ ДЛЯ КРИТИЧНЫХ ЗАДАНИЙ УРОВНЯ 3")
print("=" * 80)
print()

passed = 0
failed = 0
errors = []

for test_name, test_func in tests:
    try:
        print(f"Запуск: {test_name}...")
        
        # Для тестов требующих clean_game fixture
        from game import Game
        clean_game = Game()
        
        # Запускаем тест
        if 'clean_game' in test_func.__code__.co_varnames:
            test_func(clean_game)
        else:
            test_func()
        
        print(f"  ✅ PASSED\n")
        passed += 1
        
    except AssertionError as e:
        print(f"  ❌ FAILED: {e}\n")
        failed += 1
        errors.append((test_name, str(e)))
        
    except Exception as e:
        print(f"  ❌ ERROR: {e}\n")
        failed += 1
        errors.append((test_name, f"ERROR: {e}"))

# Итоги
print("=" * 80)
print(f"РЕЗУЛЬТАТЫ: {passed} пройдено, {failed} не пройдено")
print("=" * 80)

if errors:
    print("\nОШИБКИ:")
    for test_name, error in errors:
        print(f"  - {test_name}: {error}")
else:
    print("\n✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")

pygame.quit()
sys.exit(0 if failed == 0 else 1)
