from enum import Enum

class State(Enum):  # Это будет отдельный тип данных, а не класс. Enumerate - ну ты понял
    MENU = 0
    START = 1,
    CONTINUE = 2,
    CHOOSE_THEME = 3,
    CHOOSE_HERO = 4,
    CHOOSE_LVL = 5,
    QUIT = 6


class GameState:
    def __init__(self):
        self.state = State.MENU  # сюда изначально заложится состояние меню

    def change(self, state):
        self.state = state

    def check(self, state):
        if self.state == state:
            return True
        return False
