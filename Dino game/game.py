from Bird import *
from Button import *
from Object import *
from images import *
import images as imgs
from effects import *
from states import *
from save import *


class Game:
    def __init__(self):
        pygame.display.set_caption('Run Dino! Run')  # Смена имени игры
        pygame.display.set_icon(icon)   # Смена иконки

        pygame.mixer.music.load('Music/Opening.mp3')
        pygame.mixer.music.set_volume(0.3)

        self.cactus_options = [20, 430, 30, 450, 25, 420]  # Параметры кактусов относительно экрана (ноль вверху экрана)
        self.img_counter = 0
        self.health = 2
        self.make_jump = False
        self.jump_counter = 30
        self.scores = 0
        self.jump_num = 0
        self.max_scores = 0
        self.max_above = 0
        self.cooldown = 0
        self.game_state = GameState()
        self.save_data = Save()

    def start(self):
        # состояния игры
        while True:
            if self.game_state.check(State.MENU):
                # self.max_scores = self.save_data.get('max')
                self.show_menu()
            elif self.game_state.check(State.START):
                self.choose_theme()
                self.start_game()
            elif self.game_state.check(State.CONTINUE):
                self.max_scores = self.save_data.get('max')
                self.start_game()
            elif self.game_state.check(State.QUIT):
                self.save_data.save()
                self.save_data.add('max', self.max_scores)  # сохраняет по индексу max
                break

    def show_menu(self):
        menu_background = pygame.image.load('Effects and background/Cat.jpg')

        start_button = Button(288, 70)
        continue_button = Button(222, 70)
        quit_button = Button(120, 70)

        show = True

        while show:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.blit(menu_background, (0, 0))
            if start_button.draw(270, 200, 'Start game', font_size=50):
                self.game_state.change(State.START)
                return
            if continue_button.draw(300, 280, 'Continue', font_size=50):
                self.game_state.change(State.CONTINUE)
                return
            if quit_button.draw(358, 370, 'Quit', font_size=50):
                self.game_state.change(State.QUIT)
                return

            pygame.display.update()
            clock.tick(60)

    def start_game(self):

        while self.run_game():
            self.scores = 0
            self.make_jump = False
            self.jump_counter = 30
            p.usr_y = p.display_height - p.usr_height - 100
            self.health = 2
            self.cooldown = 0

    def choose_hero(self):
        hero1 = Button(300, 70)
        hero2 = Button(300, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill([0, 0, 0])

            if hero1.draw(270, 200, 'Pink Dino', font_size=50):
                set_theme(1)
                return
            if hero2.draw(270, 300, 'Purple Dino', font_size=50):
                set_theme(2)
                return

            pygame.display.update()
            clock.tick(60)

    def choose_theme(self):
        theme1 = Button(250, 70)
        theme2 = Button(300, 70)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            display.fill([0, 0, 0])

            if theme1.draw(270, 200, 'Day theme', font_size=50):
                set_theme(1)
                return
            if theme2.draw(270, 300, 'Night theme', font_size=50):
                set_theme(2)
                return

            pygame.display.update()
            clock.tick(60)

    def run_game(self):
        # TODO Для чего нужно это делать? разве он сам не считывает?

        pygame.mixer.music.play(-1)

        game = True
        cactus_arr = []
        self.create_cactus_arr(cactus_arr)  # Вызываем функцию кактусов

        stone, cloud = self.open_random_object()
        heart = Object(display_width, 280, 30, health_img, 4)

        all_btn_bullets = []
        all_mouse_bullets = []

        bird1 = Bird(-80)
        bird2 = Bird(-40)

        all_birds = [bird1, bird2]

        while game:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pos()  # Позиция мышки
            click = pygame.mouse.get_pressed()

            if keys[pygame.K_SPACE]:  # Присвоение кнопке пробела прыжок
                self.make_jump = True
                if 0 < self.jump_counter < 15:
                    if not self.jump_num:  # если не нулевое
                        self.jump_num += 1
                        self.jump_counter = 30

            if self.make_jump:
                self.jump()

            display.blit(imgs.land, (0, 0))  # Заполнили землю
            print_text('Score: ' + str(self.scores), 600, 10)

            self.draw_array(cactus_arr)  # Рисуем кактусы
            self.move_objects(stone, cloud)

            # Создание персонажа
            self.draw_dino()

            if keys[pygame.K_ESCAPE]:
                self.pause()

            if not self.cooldown:
                if keys[pygame.K_x]:
                    pygame.mixer.Sound.play(shot_sound)
                    pygame.mixer.Sound.set_volume(shot_sound, 0.3)
                    all_btn_bullets.append(Bullet(p.usr_x + p.usr_width, p.usr_y + 22))  # Bullet
                    self.cooldown = 50
                elif click[0]:  # Левая кнопка мыши
                    pygame.mixer.Sound.play(shot_sound)
                    pygame.mixer.Sound.set_volume(shot_sound, 0.3)
                    add_bullet = Bullet(p.usr_x + p.usr_width, p.usr_y + 22)
                    add_bullet.find_path(mouse[0], mouse[1])  # x and y

                    all_mouse_bullets.append(add_bullet)  # Bullet
                    self.cooldown = 50
            else:
                print_text('Cooldown time: ' + str(self.cooldown // 10), 482, 40)
                self.cooldown -= 1

            for bullet in all_btn_bullets:
                if not bullet.move():
                    all_btn_bullets.remove(bullet)

            for bullet in all_mouse_bullets:
                if not bullet.move_to():
                    all_mouse_bullets.remove(bullet)

            heart.move()
            self.hearts_plus(heart)

            self.count_score(cactus_arr)

            if self.check_collision(cactus_arr):
                # pygame.mixer.music.stop()
                # pygame.mixer.Sound.play(fall_sound)
                # if not check_health():
                game = False

            self.show_health()

            # bird1.draw()

            self.draw_birds(all_birds)
            self.check_birds_dmg(all_mouse_bullets, all_birds)

            pygame.display.update()  # Чтобы обновлялся дисплей
            clock.tick(80)  # 60 кадров в секунду

        return self.game_over()

    def jump(self):  # Функция прыжка
        if self.jump_counter >= -30:
            if self.jump_counter == 30:
                pygame.mixer.Sound.play(jump_sound)  # Включит звук

            p.usr_y -= self.jump_counter / 2.5
            self.jump_counter -= 1
        else:
            if p.usr_y < 400:
                p.usr_y = min(400, p.usr_y - self.jump_counter / 2.5)
                self.jump_counter -= 1
            else:
                self.jump_num = 0
                self.jump_counter = 30
                self.make_jump = False

    def create_cactus_arr(self, array):  # Массив с кактусами
        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]
        array.append(Object(display_width + 20, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]
        array.append(Object(display_width + 300, height, width, img, 4))

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]
        array.append(Object(display_width + 600, height, width, img, 4))

    @staticmethod
    def find_radius(array):
        maximum = max(array[0].x, array[1].x, array[2].x)

        if maximum < display_width:  # Не находится ли левее границы дисплея
            radius = display_width
            if radius - maximum < 50:
                radius += 280
        else:
            radius = maximum

        choice = random.randrange(0, 5)  # Чтобы кактусы не спавнились близко и далеко
        if choice == 0:
            radius += random.randrange(10, 15)
        else:
            radius += random.randrange(250, 400)

        return radius

    def draw_array(self, array):
        for cactus in array:
            check = cactus.move()
            if not check:
                self.object_return(array, cactus)

    def object_return(self, objects, obj):
        radius = self.find_radius(objects)

        choice = random.randrange(0, 3)
        img = cactus_img[choice]
        width = self.cactus_options[choice * 2]
        height = self.cactus_options[choice * 2 + 1]

        obj.return_self(radius, height, width, img)

    @staticmethod
    def open_random_object():
        choice = random.randrange(0, 2)
        img_of_stone = stone_img[choice]

        choice = random.randrange(0, 2)
        img_of_cloud = cloud_img[choice]

        stone = Object(display_width, display_height - 80, 10, img_of_stone, 4)
        cloud = Object(display_width, 80, 100, img_of_cloud, 2)

        return stone, cloud

    @staticmethod
    def move_objects(stone, cloud):
        check = stone.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_stone = stone_img[choice]
            stone.return_self(p.display_width, 500 + random.randrange(10, 80), stone.width, img_of_stone)

        check = cloud.move()
        if not check:
            choice = random.randrange(0, 2)
            img_of_cloud = cloud_img[choice]
            cloud.return_self(p.display_width, random.randrange(10, 200), stone.width, img_of_cloud)

    def draw_dino(self):
        if self.img_counter == 25:  # плавная анимация персонажа
            self.img_counter = 0

        display.blit(dino_img[self.img_counter // 5], (p.usr_x, p.usr_y))
        self.img_counter += 1

    @staticmethod
    def pause():
        paused = True

        pygame.mixer.music.pause()

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Paused, press enter to continue', 160, 300)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:  # Присвоение кнопке паузы
                paused = False

            pygame.display.update()
            clock.tick(15)

        pygame.mixer.music.unpause()

    def check_collision(self, barriers):  # Логика блять, разбираться
        for barrier in barriers:
            if barrier.y == 450:  # Little cactus
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr_width - 8 <= barrier.x + barrier.width:
                        if self.check_health():  # Столкновения логика, рисуем новый кактус
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter >= 0:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 20 <= barrier.x + barrier.width:
                            if self.check_health():  # Столкновения логика, рисуем новый кактус
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                else:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                            if self.check_health():  # Столкновения логика, рисуем новый кактус
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
            else:  # Other cactuses
                if not self.make_jump:
                    if barrier.x <= p.usr_x + p.usr_width - 8 <= barrier.x + barrier.width:
                        if self.check_health():  # Столкновения логика, рисуем новый кактус
                            self.object_return(barriers, barrier)
                            return False
                        else:
                            return True
                elif self.jump_counter == 10:  # Прыжок только начался
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + usr_width - 5 <= barrier.x + barrier.width:
                            if self.check_health():  # Столкновения логика, рисуем новый кактус
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                elif self.jump_counter >= -1:
                    if p.usr_y + p.usr_height - 5 >= barrier.y:
                        if barrier.x <= p.usr_x + p.usr_width - 20 <= barrier.x + barrier.width:
                            if self.check_health():  # Столкновения логика, рисуем новый кактус
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
                else:  # Обратный прыжок
                    if p.usr_y + p.usr_height - 10 >= barrier.y:
                        if barrier.x <= p.usr_x + 5 <= barrier.x + barrier.width:
                            if self.check_health():  # Столкновения логика, рисуем новый кактус
                                self.object_return(barriers, barrier)
                                return False
                            else:
                                return True
        return False

    # TODO: Сделать логику "насаживания" на кактус

    def count_score(self, barriers):
        above_cactus = 0

        if -20 <= self.jump_counter < 25:
            for barrier in barriers:
                if p.usr_y + p.usr_height - 5 <= barrier.y:
                    if barrier.x <= p.usr_x <= barrier.x + barrier.width:
                        above_cactus += 1
                    elif barrier.x <= p.usr_x + p.usr_width <= barrier.x + barrier.width:
                        above_cactus += 1

            self.max_above = max(self.max_above, above_cactus)
        else:
            if self.jump_counter == -30:
                self.scores += self.max_above
                self.max_above = 0

    def game_over(self):
        if self.scores > self.max_scores:
            self.max_scores = self.scores

        stopped = True
        while stopped:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            print_text('Game over, press Enter to play again, Esc to exit', 40, 250)
            print_text('Max score: ' + str(self.max_scores), 300, 300)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                return True
            if keys[pygame.K_ESCAPE]:
                self.game_state.change(State.QUIT)
                return False

            pygame.display.update()
            clock.tick(15)

    def show_health(self):
        show = 0
        x = 20
        while show != self.health:
            display.blit(health_img, (x, 20))
            x += 40
            show += 1

    def check_health(self):
        self.health -= 1
        if self.health == 0:
            pygame.mixer.Sound.play(fall_sound)
            return False
        else:
            pygame.mixer.Sound.play(crash_sound)
            return True

    def hearts_plus(self, heart):

        if heart.x <= -heart.width:
            radius = p.display_width + random.randrange(500, 10000)
            heart.return_self(radius, heart.y, heart.width, heart.image)

        if p.usr_x <= heart.x <= p.usr_x + p.usr_height:
            if p.usr_y <= heart.y <= p.usr_y + p.usr_height:
                pygame.mixer.Sound.play(heart_plus_sound)
                if self.health < 2:
                    self.health += 1

                radius = p.display_width + random.randrange(500, 10000)
                heart.return_self(radius, heart.y, heart.width, heart.image)

                # TODO: реализовать варьирование координаты
    @staticmethod
    def draw_birds(birds):
        for bird in birds:
            action = bird.draw()
            if action == 1:
                bird.show()
            elif action == 2:
                bird.hide()
            else:
                bird.shoot()

    @staticmethod
    def check_birds_dmg(bullets, birds):
        for bird in birds:
            for bullet in bullets:
                bird.kill_bird(bullet)
