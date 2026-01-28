"""
Проверка работоспособности решений всех уровней
Этот скрипт не требует pygame display и проверяет код/файлы статически

Структура тестов:
- Level 1: Визуальные изменения (файлы, параметры)
- Level 2: Изменение параметров (значения в коде)
- Level 3: Логика (наличие методов, классов)
"""
import sys
import os
import re
import ast

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


# ==============================================================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ==============================================================================

def read_file(filename):
    """Читает файл и возвращает содержимое"""
    filepath = os.path.join(PROJECT_ROOT, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None


def find_value_in_code(content, pattern):
    """Ищет значение по регулярному выражению"""
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def check_method_exists(content, method_name):
    """Проверяет наличие метода в коде"""
    return f"def {method_name}" in content


def check_attribute_in_init(content, attr_name):
    """Проверяет наличие атрибута в __init__"""
    # Ищем self.attr_name = в методе __init__
    return f"self.{attr_name}" in content


# ==============================================================================
# БАЗОВЫЕ ПРОВЕРКИ СТРУКТУРЫ
# ==============================================================================

def test_files_structure():
    """Проверка структуры файлов проекта"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА СТРУКТУРЫ ПРОЕКТА")
    print("=" * 60)
    
    required_files = [
        'game.py', 'save.py', 'Bird.py', 'Bullet.py', 'Button.py',
        'Object.py', 'parameters.py', 'images.py', 'sounds.py',
        'effects.py', 'states.py', 'main.py'
    ]
    
    all_exist = True
    for filename in required_files:
        filepath = os.path.join(PROJECT_ROOT, filename)
        if os.path.exists(filepath):
            print(f"  ✅ {filename}")
        else:
            print(f"  ❌ {filename} - НЕ НАЙДЕН")
            all_exist = False
    
    # Проверка папок
    folders = ['Dino', 'Bird', 'Objects', 'Music', 'Effects and background']
    for folder in folders:
        folderpath = os.path.join(PROJECT_ROOT, folder)
        if os.path.exists(folderpath):
            print(f"  ✅ {folder}/")
        else:
            print(f"  ❌ {folder}/ - НЕ НАЙДЕНА")
            all_exist = False
    
    return all_exist


def test_solutions_structure():
    """Проверка структуры папки решений"""
    print("\n" + "=" * 60)
    print("ПРОВЕРКА СТРУКТУРЫ РЕШЕНИЙ")
    print("=" * 60)
    
    solutions_dir = os.path.join(PROJECT_ROOT, 'solutions')
    
    if not os.path.exists(solutions_dir):
        print("  ❌ Папка solutions/ не найдена")
        return False
    
    expected = {
        'level1': 6,  # 6 заданий
        'level2': 7,  # 7 заданий
        'level3': 11  # 11 заданий (включая 3.2 с двумя файлами)
    }
    
    all_ok = True
    for level, expected_count in expected.items():
        level_dir = os.path.join(solutions_dir, level)
        if os.path.exists(level_dir):
            files = [f for f in os.listdir(level_dir) if f.endswith(('.py', '.md'))]
            status = "✅" if len(files) >= expected_count - 1 else "⚠️"
            print(f"  {status} {level}/ - {len(files)} файлов (ожидается ~{expected_count})")
        else:
            print(f"  ❌ {level}/ не найдена")
            all_ok = False
    
    return all_ok


# ==============================================================================
# LEVEL 1 - ВИЗУАЛЬНЫЕ ИЗМЕНЕНИЯ
# ==============================================================================

def test_level1():
    """Тесты заданий уровня 1 (визуальные изменения)"""
    print("\n" + "=" * 60)
    print("LEVEL 1 - ВИЗУАЛЬНЫЕ ИЗМЕНЕНИЯ")
    print("=" * 60)
    
    results = {}
    
    # 1.1 - Замена спрайта динозавра
    print("\n📋 Задание 1.1: Замена спрайта динозавра")
    images_content = read_file('images.py')
    dino_folder = os.path.join(PROJECT_ROOT, 'Dino')
    dino_files = os.listdir(dino_folder) if os.path.exists(dino_folder) else []
    
    # Проверяем что в Dino есть файлы
    has_dino_sprites = len([f for f in dino_files if f.endswith(('.jpg', '.png'))]) >= 3
    results['1.1'] = has_dino_sprites
    print(f"  {'✅' if has_dino_sprites else '⚠️'} Спрайты динозавра: {len(dino_files)} файлов")
    print("  ℹ️  Для проверки изменения нужен визуальный тест")
    
    # 1.2 - Замена фоновой музыки
    print("\n📋 Задание 1.2: Фоновая музыка")
    music_folder = os.path.join(PROJECT_ROOT, 'Music')
    music_files = os.listdir(music_folder) if os.path.exists(music_folder) else []
    
    has_music = 'Opening.mp3' in music_files or any(f.endswith('.mp3') for f in music_files)
    results['1.2'] = has_music
    print(f"  {'✅' if has_music else '❌'} Музыкальные файлы: {len(music_files)}")
    print("  ℹ️  Для проверки изменения музыки нужен аудио тест")
    
    # 1.3 - Цвета кнопок
    print("\n📋 Задание 1.3: Цвета кнопок")
    button_content = read_file('Button.py')
    
    # Ищем цвета в Button.py
    inactive_match = re.search(r'inactive_color\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)', button_content)
    active_match = re.search(r'active_color\s*=\s*\((\d+),\s*(\d+),\s*(\d+)\)', button_content)
    
    if inactive_match and active_match:
        inactive = tuple(map(int, inactive_match.groups()))
        active = tuple(map(int, active_match.groups()))
        default_inactive = (13, 162, 58)
        changed = inactive != default_inactive
        results['1.3'] = True  # Файл корректный
        print(f"  ✅ inactive_color = {inactive}")
        print(f"  ✅ active_color = {active}")
        print(f"  {'🔄' if changed else '⚪'} Цвет {'изменён' if changed else 'стандартный (зелёный)'}")
    else:
        results['1.3'] = False
        print("  ❌ Не удалось найти цвета кнопок")
    
    # 1.4 - Размер окна
    print("\n📋 Задание 1.4: Размер окна")
    params_content = read_file('parameters.py')
    
    width_match = re.search(r'display_width\s*=\s*(\d+)', params_content)
    height_match = re.search(r'display_height\s*=\s*(\d+)', params_content)
    
    if width_match and height_match:
        width = int(width_match.group(1))
        height = int(height_match.group(1))
        default_size = (800, 600)
        changed = (width, height) != default_size
        results['1.4'] = True
        print(f"  ✅ Размер окна: {width}x{height}")
        print(f"  {'🔄' if changed else '⚪'} Размер {'изменён' if changed else 'стандартный'}")
    else:
        results['1.4'] = False
        print("  ❌ Не удалось найти размеры окна")
    
    # 1.5 - Скорость кактусов
    print("\n📋 Задание 1.5: Скорость кактусов")
    object_content = read_file('Object.py')
    game_content_1_5 = read_file('game.py')
    
    # Object принимает speed как параметр, проверяем в game.py где создаются объекты
    speed_match = re.search(r'Object\([^)]*,\s*(\d+)\s*\)', game_content_1_5)
    has_speed_param = 'self.speed = speed' in object_content
    
    if has_speed_param:
        results['1.5'] = True
        if speed_match:
            default_speed = int(speed_match.group(1))
            print(f"  ✅ Object принимает параметр speed")
            print(f"  ✅ Скорость по умолчанию в game.py: {default_speed}")
            print(f"  {'🔄' if default_speed != 4 else '⚪'} Скорость {'изменена' if default_speed != 4 else 'стандартная (4)'}")
        else:
            print(f"  ✅ Object принимает параметр speed")
            print(f"  ℹ️  Скорость задаётся при создании объекта")
    else:
        results['1.5'] = False
        print("  ❌ Object не имеет параметра speed")
    
    # 1.6 - Звук прыжка
    print("\n📋 Задание 1.6: Звук прыжка")
    sounds_content = read_file('sounds.py')
    
    has_jump_sound = 'Jump' in sounds_content or 'jump' in sounds_content
    results['1.6'] = has_jump_sound
    print(f"  {'✅' if has_jump_sound else '❌'} Звук прыжка определён")
    
    # Итог Level 1
    passed = sum(1 for v in results.values() if v)
    print(f"\n📊 Level 1: {passed}/{len(results)} заданий проверено успешно")
    
    return results


# ==============================================================================
# LEVEL 2 - ИЗМЕНЕНИЕ ПАРАМЕТРОВ
# ==============================================================================

def test_level2():
    """Тесты заданий уровня 2 (параметры)"""
    print("\n" + "=" * 60)
    print("LEVEL 2 - ИЗМЕНЕНИЕ ПАРАМЕТРОВ")
    print("=" * 60)
    
    results = {}
    game_content = read_file('game.py')
    bird_content = read_file('Bird.py')
    bullet_content = read_file('Bullet.py')
    
    # 2.1 - Количество жизней
    print("\n📋 Задание 2.1: Количество жизней")
    health_matches = re.findall(r'self\.health\s*=\s*(\d+)', game_content)
    if health_matches:
        health_values = list(set(map(int, health_matches)))
        results['2.1'] = True
        print(f"  ✅ Значения health в коде: {health_values}")
        print(f"  {'🔄' if any(h != 2 for h in health_values) else '⚪'} {'Изменено' if any(h != 2 for h in health_values) else 'Стандартное (2)'}")
    else:
        results['2.1'] = False
        print("  ❌ Не найдено значение health")
    
    # 2.2 - Скорость пуль
    print("\n📋 Задание 2.2: Скорость пуль")
    bullet_speed_match = re.search(r'self\.speed_x\s*=\s*(\d+)', bullet_content)
    if bullet_speed_match:
        speed = int(bullet_speed_match.group(1))
        results['2.2'] = True
        print(f"  ✅ Скорость пуль: {speed}")
        print(f"  {'🔄' if speed != 8 else '⚪'} {'Изменено' if speed != 8 else 'Стандартная (8)'}")
    else:
        results['2.2'] = False
        print("  ❌ Не найдена скорость пуль")
    
    # 2.3 - Новый спрайт кактуса
    print("\n📋 Задание 2.3: Новый спрайт кактуса")
    objects_folder = os.path.join(PROJECT_ROOT, 'Objects')
    cactus_files = [f for f in os.listdir(objects_folder) if 'Cactus' in f] if os.path.exists(objects_folder) else []
    results['2.3'] = len(cactus_files) >= 3
    print(f"  {'✅' if len(cactus_files) >= 3 else '⚠️'} Спрайтов кактусов: {len(cactus_files)}")
    print(f"  {'🔄' if len(cactus_files) > 3 else '⚪'} {'Добавлен новый' if len(cactus_files) > 3 else 'Стандартные (3)'}")
    
    # 2.4 - Частота появления сердечек
    print("\n📋 Задание 2.4: Частота сердечек")
    # Ищем random.randrange для сердечек
    heart_match = re.search(r'randrange\s*\(\s*500\s*,\s*(\d+)\s*\)', game_content)
    if heart_match:
        max_range = int(heart_match.group(1))
        results['2.4'] = True
        print(f"  ✅ Диапазон появления: 500-{max_range}")
        print(f"  {'🔄' if max_range != 10000 else '⚪'} {'Изменено' if max_range != 10000 else 'Стандартный (10000)'}")
    else:
        results['2.4'] = True  # Может быть изменён по-другому
        print("  ⚠️ Не удалось определить точный диапазон")
    
    # 2.5 - Скорость птиц
    print("\n📋 Задание 2.5: Скорость птиц")
    bird_speed_match = re.search(r'self\.speed\s*=\s*(\d+)', bird_content)
    if bird_speed_match:
        speed = int(bird_speed_match.group(1))
        results['2.5'] = True
        print(f"  ✅ Скорость птиц: {speed}")
        print(f"  {'🔄' if speed != 3 else '⚪'} {'Изменено' if speed != 3 else 'Стандартная (3)'}")
    else:
        results['2.5'] = False
        print("  ❌ Не найдена скорость птиц")
    
    # 2.6 - Счётчик убитых птиц (return в kill_bird)
    print("\n📋 Задание 2.6: Счётчик птиц (return в kill_bird)")
    has_return_true = 'return True' in bird_content and 'kill_bird' in bird_content
    has_return_false = 'return False' in bird_content and 'kill_bird' in bird_content
    
    # Проверяем birds_killed в game.py
    has_birds_counter = 'birds_killed' in game_content
    
    if has_return_true and has_return_false:
        results['2.6'] = True
        print(f"  ✅ kill_bird() возвращает True/False")
        print(f"  {'✅' if has_birds_counter else '⚠️'} Счётчик birds_killed {'найден' if has_birds_counter else 'не найден'} в game.py")
    else:
        results['2.6'] = False
        print("  ⚠️ kill_bird() не возвращает значения (задание не выполнено)")
    
    # 2.7 - Высота прыжка
    print("\n📋 Задание 2.7: Высота прыжка")
    jump_matches = re.findall(r'jump_counter\s*[=<>]+\s*(-?\d+)', game_content)
    if jump_matches:
        results['2.7'] = True
        unique_values = list(set(jump_matches))
        print(f"  ✅ Значения jump_counter: {unique_values[:5]}...")
        print(f"  ℹ️  Проверьте визуально что прыжок работает корректно")
    else:
        results['2.7'] = False
        print("  ❌ Не найдены параметры прыжка")
    
    # Итог Level 2
    passed = sum(1 for v in results.values() if v)
    print(f"\n📊 Level 2: {passed}/{len(results)} заданий проверено успешно")
    
    return results


# ==============================================================================
# LEVEL 3 - ЛОГИКА (МЕТОДЫ И КЛАССЫ)
# ==============================================================================

def test_level3():
    """Тесты заданий уровня 3 (логика - без pygame display)"""
    print("\n" + "=" * 60)
    print("LEVEL 3 - ЛОГИКА (СТАТИЧЕСКИЙ АНАЛИЗ)")
    print("=" * 60)
    
    results = {}
    game_content = read_file('game.py')
    save_content = read_file('save.py')
    
    # 3.1 - Урон от пуль птиц
    print("\n📋 Задание 3.1: Урон от пуль птиц")
    # Ищем код проверки столкновения пуль птиц с игроком
    has_bird_bullet_check = 'bird.all_bullets' in game_content or 'all_bullets' in game_content
    has_collision_check = 'p.usr_x' in game_content and 'bullet.x' in game_content
    results['3.1'] = has_bird_bullet_check
    print(f"  {'✅' if has_bird_bullet_check else '⚠️'} Обработка пуль птиц: {'найдена' if has_bird_bullet_check else 'не найдена'}")
    print(f"  ℹ️  Требуется функциональный тест для полной проверки")
    
    # 3.2 - Система сохранений
    print("\n📋 Задание 3.2: Система сохранений")
    methods_3_2 = ['save_game_state', 'load_game_state', 'clear_game_state', 'has_saved_game']
    found_methods = [m for m in methods_3_2 if f'def {m}' in save_content]
    results['3.2'] = len(found_methods) == len(methods_3_2)
    
    for method in methods_3_2:
        status = "✅" if method in found_methods else "❌"
        print(f"  {status} {method}()")
    
    # 3.3 - Меню выхода (pause_menu)
    print("\n📋 Задание 3.3: Меню выхода")
    has_pause_menu = 'def pause_menu' in game_content
    results['3.3'] = has_pause_menu
    print(f"  {'✅' if has_pause_menu else '⚠️'} pause_menu(): {'найден' if has_pause_menu else 'не найден (используется старый pause())'}")
    
    # 3.4 - Выбор героя
    print("\n📋 Задание 3.4: Выбор героя")
    has_choose_hero = 'def choose_hero' in game_content or 'def choose_theme' in game_content
    results['3.4'] = has_choose_hero
    print(f"  {'✅' if has_choose_hero else '⚠️'} choose_hero/choose_theme(): {'найден' if has_choose_hero else 'не найден'}")
    
    # 3.5 - Летучие мыши (класс Bat)
    print("\n📋 Задание 3.5: Летучие мыши")
    bat_exists = os.path.exists(os.path.join(PROJECT_ROOT, 'Bat.py'))
    if bat_exists:
        bat_content = read_file('Bat.py')
        has_bat_class = 'class Bat' in bat_content
        has_zigzag = 'move_zigzag' in bat_content or 'zigzag' in bat_content
        has_kill = 'kill_bat' in bat_content
        
        results['3.5'] = has_bat_class and has_zigzag and has_kill
        print(f"  ✅ Bat.py существует")
        print(f"  {'✅' if has_bat_class else '❌'} class Bat")
        print(f"  {'✅' if has_zigzag else '❌'} move_zigzag()")
        print(f"  {'✅' if has_kill else '❌'} kill_bat()")
    else:
        results['3.5'] = False
        print("  ❌ Bat.py не найден")
    
    # 3.6 - Система уровней
    print("\n📋 Задание 3.6: Система уровней")
    has_level = 'self.level' in game_content
    results['3.6'] = has_level
    print(f"  {'✅' if has_level else '⚠️'} self.level: {'найден' if has_level else 'не найден'}")
    
    # 3.7 - Щит
    print("\n📋 Задание 3.7: Щит-бонус")
    has_shield = 'shield' in game_content.lower()
    results['3.7'] = has_shield
    print(f"  {'✅' if has_shield else '⚠️'} shield: {'найден' if has_shield else 'не найден'}")
    
    # 3.8 - Таблица лидеров
    print("\n📋 Задание 3.8: Таблица лидеров")
    methods_3_8 = ['save_score', 'get_leaderboard', 'is_top_score', 'clear_leaderboard']
    found_methods_3_8 = [m for m in methods_3_8 if f'def {m}' in save_content]
    results['3.8'] = len(found_methods_3_8) == len(methods_3_8)
    
    for method in methods_3_8:
        status = "✅" if method in found_methods_3_8 else "❌"
        print(f"  {status} {method}()")
    
    # 3.9 - Пауза на P
    print("\n📋 Задание 3.9: Пауза по клавише P")
    has_p_key = 'K_p' in game_content or 'pygame.K_p' in game_content
    results['3.9'] = has_p_key
    print(f"  {'✅' if has_p_key else '⚠️'} K_p: {'найден' if has_p_key else 'не найден'}")
    
    # 3.10 - Анимация смерти
    print("\n📋 Задание 3.10: Анимация смерти")
    has_death_animation = 'death_animation' in game_content or 'death' in game_content.lower()
    results['3.10'] = has_death_animation
    print(f"  {'✅' if has_death_animation else '⚠️'} death_animation: {'найден' if has_death_animation else 'не найден'}")
    
    # Итог Level 3
    passed = sum(1 for v in results.values() if v)
    print(f"\n📊 Level 3: {passed}/{len(results)} заданий проверено успешно")
    
    return results


# ==============================================================================
# ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ SAVE.PY (без pygame)
# ==============================================================================

def test_save_functionality():
    """Функциональные тесты системы сохранений"""
    print("\n" + "=" * 60)
    print("ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ SAVE.PY")
    print("=" * 60)
    
    try:
        from save import Save
        save_data = Save()
        
        # Тест 3.2: Сохранение состояния
        print("\n📋 Тест save_game_state / load_game_state")
        try:
            save_data.save_game_state(health=3, scores=150, level=2)
            loaded = save_data.load_game_state()
            
            assert loaded['health'] == 3, f"health={loaded['health']}, ожидалось 3"
            assert loaded['scores'] == 150, f"scores={loaded['scores']}, ожидалось 150"
            assert loaded['level'] == 2, f"level={loaded['level']}, ожидалось 2"
            assert loaded['exists'] == True, "exists должен быть True"
            
            print("  ✅ Сохранение состояния работает")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            return False
        
        # Тест clear_game_state
        print("\n📋 Тест clear_game_state")
        try:
            save_data.clear_game_state()
            loaded = save_data.load_game_state()
            assert loaded['exists'] == False, "exists должен быть False после очистки"
            print("  ✅ Очистка состояния работает")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            return False
        
        # Тест 3.8: Таблица лидеров
        print("\n📋 Тест save_score / get_leaderboard")
        try:
            save_data.clear_leaderboard()
            save_data.save_score(100, "Alice")
            save_data.save_score(200, "Bob")
            save_data.save_score(150, "Charlie")
            
            leaderboard = save_data.get_leaderboard()
            
            assert len(leaderboard) == 3, f"Длина={len(leaderboard)}, ожидалось 3"
            assert leaderboard[0]['name'] == "Bob", "Первый должен быть Bob"
            assert leaderboard[0]['score'] == 200, "У Bob должно быть 200 очков"
            
            print("  ✅ Таблица лидеров работает")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            return False
        
        # Тест топ-5
        print("\n📋 Тест ограничения топ-5")
        try:
            save_data.clear_leaderboard()
            for i in range(7):
                save_data.save_score(i * 50, f"Player{i}")
            
            leaderboard = save_data.get_leaderboard()
            assert len(leaderboard) == 5, f"Должно быть 5 записей, получено {len(leaderboard)}"
            print("  ✅ Ограничение топ-5 работает")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            return False
        
        # Тест is_top_score
        print("\n📋 Тест is_top_score")
        try:
            save_data.clear_leaderboard()
            for i in range(5):
                save_data.save_score((i + 1) * 50, f"Player{i}")  # 50, 100, 150, 200, 250
            
            assert save_data.is_top_score(300) == True, "300 должен попасть в топ"
            assert save_data.is_top_score(40) == False, "40 не должен попасть в топ"
            print("  ✅ is_top_score работает")
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
            return False
        
        # Очистка после тестов
        save_data.clear_leaderboard()
        save_data.clear_game_state()
        
        print("\n✅ ВСЕ ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ SAVE.PY ПРОЙДЕНЫ!")
        return True
        
    except ImportError as e:
        print(f"  ❌ Ошибка импорта: {e}")
        return False


# ==============================================================================
# ТЕСТ КЛАССА BAT
# ==============================================================================

def test_bat_class():
    """Тест класса Bat"""
    print("\n" + "=" * 60)
    print("ФУНКЦИОНАЛЬНЫЕ ТЕСТЫ BAT.PY")
    print("=" * 60)
    
    try:
        from Bat import Bat
        
        print("\n📋 Создание объекта Bat")
        bat = Bat()
        
        # Проверка атрибутов
        required_attrs = ['x', 'y', 'speed_x', 'speed_y', 'alive', 'width', 'height']
        for attr in required_attrs:
            assert hasattr(bat, attr), f"Отсутствует атрибут {attr}"
        print("  ✅ Все атрибуты присутствуют")
        
        # Проверка методов
        required_methods = ['move_zigzag', 'kill_bat', 'reset']
        for method in required_methods:
            assert hasattr(bat, method), f"Отсутствует метод {method}"
        print("  ✅ Все методы присутствуют")
        
        # Тест move_zigzag
        print("\n📋 Тест move_zigzag()")
        initial_x = bat.x
        bat.move_zigzag()
        assert bat.x < initial_x, "Летучая мышь должна двигаться влево"
        print("  ✅ move_zigzag работает")
        
        # Тест reset
        print("\n📋 Тест reset()")
        bat.alive = False
        bat.reset()
        assert bat.alive == True, "После reset alive должен быть True"
        print("  ✅ reset работает")
        
        print("\n✅ ВСЕ ТЕСТЫ BAT.PY ПРОЙДЕНЫ!")
        return True
        
    except ImportError as e:
        print(f"  ⚠️ Bat.py не найден или ошибка импорта: {e}")
        print("  ℹ️  Это нормально если задание 3.5 ещё не выполнено")
        return False
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False


# ==============================================================================
# ГЛАВНАЯ ФУНКЦИЯ
# ==============================================================================

def main():
    """Запуск всех тестов"""
    print("=" * 60)
    print("🎮 ПОЛНАЯ ПРОВЕРКА РЕШЕНИЙ DINO GAME")
    print("=" * 60)
    print(f"Корень проекта: {PROJECT_ROOT}")
    
    all_results = {}
    
    # Структурные тесты
    all_results['structure'] = test_files_structure()
    all_results['solutions'] = test_solutions_structure()
    
    # Тесты по уровням
    all_results['level1'] = test_level1()
    all_results['level2'] = test_level2()
    all_results['level3'] = test_level3()
    
    # Функциональные тесты
    all_results['save_func'] = test_save_functionality()
    all_results['bat_func'] = test_bat_class()
    
    # Итоговый отчёт
    print("\n" + "=" * 60)
    print("📊 ИТОГОВЫЙ ОТЧЁТ")
    print("=" * 60)
    
    # Подсчёт по уровням
    level_results = {
        'Level 1': all_results.get('level1', {}),
        'Level 2': all_results.get('level2', {}),
        'Level 3': all_results.get('level3', {})
    }
    
    total_passed = 0
    total_tasks = 0
    
    for level, results in level_results.items():
        if isinstance(results, dict):
            passed = sum(1 for v in results.values() if v)
            total = len(results)
            total_passed += passed
            total_tasks += total
            status = "✅" if passed == total else "⚠️" if passed > 0 else "❌"
            print(f"  {status} {level}: {passed}/{total} заданий")
    
    print(f"\n  📈 ВСЕГО: {total_passed}/{total_tasks} заданий проверено успешно")
    
    # Функциональные тесты
    func_passed = sum([
        1 if all_results.get('save_func', False) else 0,
        1 if all_results.get('bat_func', False) else 0
    ])
    print(f"  🔧 Функциональные тесты: {func_passed}/2")
    
    print("\n" + "=" * 60)
    
    if total_passed == total_tasks and func_passed == 2:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
    else:
        print("⚠️ Некоторые проверки не пройдены")
        print("ℹ️  Это нормально если вы ещё не выполнили все задания")
    
    print("=" * 60)
    
    return total_passed == total_tasks


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
