"""Вспомогательные функции для тестов"""
import os
import sys

# Добавляем родительскую папку в путь для импорта модулей игры
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def check_file_exists(filepath):
    """Проверяет существование файла"""
    return os.path.exists(filepath)


def check_value_in_file(filepath, search_value):
    """Проверяет наличие значения в файле"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            return str(search_value) in content
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return False


def get_file_content(filepath):
    """Возвращает содержимое файла"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return None


def print_test_result(test_name, passed, details=""):
    """Выводит результат теста"""
    status = "✅ PASSED" if passed else "❌ FAILED"
    print(f"{status}: {test_name}")
    if details:
        print(f"   {details}")
