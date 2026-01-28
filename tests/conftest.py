"""
Конфигурация pytest для тестирования Dino Game

Настройки:
- Инициализация pygame с dummy драйвером для headless тестирования
- Fixtures для игровых объектов
"""
import os
import sys
import pytest

# Добавляем корень проекта в путь
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Устанавливаем dummy драйверы ДО импорта pygame
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')


def pytest_configure(config):
    """Вызывается при старте pytest"""
    # Инициализация pygame для тестов
    import pygame
    pygame.init()


def pytest_unconfigure(config):
    """Вызывается при завершении pytest"""
    import pygame
    pygame.quit()


@pytest.fixture
def clean_game():
    """Создаёт чистый экземпляр игры для тестов"""
    from game import Game
    game = Game()
    game.health = 2
    game.scores = 0
    return game


@pytest.fixture
def test_bird():
    """Создаёт птицу для тестов"""
    from Bird import Bird
    bird = Bird(-80)
    bird.y = 200
    return bird


@pytest.fixture
def test_bullet():
    """Создаёт пулю для тестов"""
    from Bullet import Bullet
    return Bullet(100, 200)


@pytest.fixture
def save_data():
    """Создаёт объект Save для тестов с очисткой после"""
    from save import Save
    save = Save()
    yield save
    # Очистка после теста
    try:
        save.clear_game_state()
        save.clear_leaderboard()
    except:
        pass
