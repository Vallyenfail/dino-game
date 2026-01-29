import random
from sounds import *
from parameters import *


class Bat:

        self.width = 40
        self.height = 40
        self.speed_x = 4  # Скорость по горизонтали
        self.img_cnt = 0

    def draw(self, bat_images):
        if self.img_cnt == len(bat_images) * 5:
            self.img_cnt = 0

        display.blit(bat_images[self.img_cnt // 5], (self.x, self.y))
        self.img_cnt += 1

    def move_zigzag(self):
        self.x -= self.speed_x

        # Зигзаг по вертикали
        self.y += self.speed_y * self.direction_y
        self.zigzag_counter += 1

        # Меняем направление каждые 30 кадров
        if self.zigzag_counter >= 30:
            self.zigzag_counter = 0

            self.direction_y = 1
        elif self.y > 400:
            self.y = 400
            self.direction_y = -1

        if self.x < -self.width:
            return False
        return True

    def kill_bat(self, bullet):
        if self.x <= bullet.x <= self.x + self.width:
            if self.y <= bullet.y <= self.y + self.height:
                return True
        return False

    def reset(self):
        self.zigzag_counter = 0
        self.direction_y = random.choice([-1, 1])
