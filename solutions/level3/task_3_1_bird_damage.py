"""
Задание 3.1: Реализация урона от пуль птиц

ПРОБЛЕМА:
В текущей версии игры птицы стреляют в игрока, но их пули пролетают сквозь динозавра
и не наносят урон. Это делает птиц бесполезными как противники.

ЧТО НУЖНО ИЗМЕНИТЬ:
Файл: game.py
Метод: run_game()
Место: после строки 225 (после self.check_birds_dmg)

БЫЛО:
```python
self.draw_birds(all_birds)
self.check_birds_dmg(all_mouse_bullets, all_birds)

pygame.display.update()
clock.tick(80)
```

СТАЛО:
```python
self.draw_birds(all_birds)
self.check_birds_dmg(all_mouse_bullets, all_birds)

# НОВЫЙ КОД: Проверка урона от пуль птиц
for bird in all_birds:
    bullets_to_remove = []
    for bullet in bird.all_bullets:
        # Проверяем столкновение пули птицы с динозавром
        if p.usr_x <= bullet.x <= p.usr_x + p.usr_width:
            if p.usr_y <= bullet.y <= p.usr_y + p.usr_height:
                bullets_to_remove.append(bullet)
                # Отнимаем здоровье
                if not self.check_health():
                    game = False
                    break
    
    # Удаляем пули, которые попали
    for bullet in bullets_to_remove:
        if bullet in bird.all_bullets:
            bird.all_bullets.remove(bullet)

pygame.display.update()
clock.tick(80)
```

ОЖИДАЕМЫЙ РЕЗУЛЬТАТ:
✅ Пули птиц теперь наносят урон игроку
✅ При попадании пули игрок теряет одно сердечко
✅ Игра становится сложнее - нужно уворачиваться от пуль!
✅ Птицы становятся реальной угрозой

КАК ПРОВЕРИТЬ:
1. Запустите игру
2. Дождитесь появления птицы
3. Дайте птице выстрелить в вас
4. Убедитесь что при попадании пропадает сердечко
5. После 2 попаданий должен быть Game Over
"""

# ПОЛНЫЙ КОД ФУНКЦИИ run_game() С ИЗМЕНЕНИЯМИ:

def run_game(self):
    """Основной игровой цикл"""
    
    pygame.mixer.music.play(-1)

    game = True
    cactus_arr = []
    self.create_cactus_arr(cactus_arr)

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
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE]:
            self.make_jump = True
            if 0 < self.jump_counter < 15:
                if not self.jump_num:
                    self.jump_num += 1
                    self.jump_counter = 30

        if self.make_jump:
            self.jump()

        display.blit(imgs.land, (0, 0))
        print_text('Score: ' + str(self.scores), 600, 10)

        self.draw_array(cactus_arr)
        self.move_objects(stone, cloud)

        self.draw_dino()

        if keys[pygame.K_ESCAPE]:
            self.pause()

        if not self.cooldown:
            if keys[pygame.K_x]:
                pygame.mixer.Sound.play(shot_sound)
                pygame.mixer.Sound.set_volume(shot_sound, 0.3)
                all_btn_bullets.append(Bullet(p.usr_x + p.usr_width, p.usr_y + 22))
                self.cooldown = 50
            elif click[0]:
                pygame.mixer.Sound.play(shot_sound)
                pygame.mixer.Sound.set_volume(shot_sound, 0.3)
                add_bullet = Bullet(p.usr_x + p.usr_width, p.usr_y + 22)
                add_bullet.find_path(mouse[0], mouse[1])
                all_mouse_bullets.append(add_bullet)
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
            game = False

        self.show_health()

        self.draw_birds(all_birds)
        self.check_birds_dmg(all_mouse_bullets, all_birds)

        # ========================================
        # НОВЫЙ КОД: Проверка урона от пуль птиц
        # ========================================
        for bird in all_birds:
            bullets_to_remove = []
            for bullet in bird.all_bullets:
                # Проверяем столкновение пули птицы с динозавром
                if p.usr_x <= bullet.x <= p.usr_x + p.usr_width:
                    if p.usr_y <= bullet.y <= p.usr_y + p.usr_height:
                        bullets_to_remove.append(bullet)
                        # Отнимаем здоровье
                        if not self.check_health():
                            game = False
                            break
            
            # Удаляем пули, которые попали
            for bullet in bullets_to_remove:
                if bullet in bird.all_bullets:
                    bird.all_bullets.remove(bullet)
        # ========================================

        pygame.display.update()
        clock.tick(80)

    return self.game_over()


# ИНСТРУКЦИЯ ПО ПРИМЕНЕНИЮ:
"""
1. Откройте файл game.py
2. Найдите метод run_game() (начинается примерно со строки 132)
3. Найдите строку: self.check_birds_dmg(all_mouse_bullets, all_birds)
4. СРАЗУ ПОСЛЕ НЕЁ добавьте код проверки урона от пуль птиц (строки 48-64 выше)
5. Сохраните файл
6. Запустите игру и проверьте!

ВАЖНО: Не удаляйте существующий код, только добавьте новый блок!
"""
