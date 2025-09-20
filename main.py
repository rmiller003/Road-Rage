import pygame
import sys
import time
import random
import math

# Constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
CAR_WIDTH = 56
HORIZON_Y = 150

# Colors
GRAY = (119, 118, 110)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
BRIGHT_RED = (255, 0, 0)
BRIGHT_GREEN = (0, 255, 0)
BRIGHT_BLUE = (0, 0, 255)

class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
            self.sound_enabled = True
            self.engine_channel = pygame.mixer.Channel(0)
        except pygame.error:
            self.sound_enabled = False
            self.engine_channel = None
            print("Warning: Could not initialize sound mixer.")

        self.display_width = DISPLAY_WIDTH
        self.display_height = DISPLAY_HEIGHT
        self.gamedisplays = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Road Rage")
        self.clock = pygame.time.Clock()
        self.game_state = 'INTRO'
        self.pause = False

        # Load assets
        self.assets = self.load_assets()

        self.new_game()

    def new_game(self):
        self.background_y = 0
        self.lives = 3
        self.level = 1
        self.crash_time = 0
        self.score = 0
        self.passed = 0
        self.next_life_milestone = 500
        self.player = Player(self)
        self.obstacles = [Obstacle(self)]
        self.bullets = []
        self.explosions = []
        self.speed_offset = 0
        self.game_state = 'INTRO'

    def load_assets(self):
        assets = {
            'carimg': pygame.image.load('car1.jpg'),
            'backgroundpic': pygame.image.load("download12.jpg"),
            'yellow_strip': pygame.image.load("yellow strip.jpg"),
            'strip': pygame.image.load("strip.jpg"),
            'intro_background': pygame.image.load("background.jpg"),
            'instruction_background': pygame.image.load("background2.jpg"),
            'obstacle_cars': [
                pygame.image.load("car.jpg"),
                pygame.image.load("car1.jpg"),
                pygame.image.load("car2.jpg"),
                pygame.image.load("car4.jpg"),
                pygame.image.load("car5.jpg"),
                pygame.image.load("car6.jpg"),
                pygame.image.load("car7.jpg")
            ],
            'sounds': {}
        }
        try:
            boom_image = pygame.image.load('boom.jpg')
            width = boom_image.get_width()
            height = boom_image.get_height()
            assets['boom'] = pygame.transform.scale(boom_image, (width // 2, height // 2))
            assets['boom'].set_alpha(128)
        except (pygame.error, FileNotFoundError):
            assets['boom'] = None

        if self.sound_enabled:
            try:
                assets['sounds']['engine'] = pygame.mixer.Sound('engine.mp3')
                assets['sounds']['crash'] = pygame.mixer.Sound('crash.mp3')
                assets['sounds']['horn'] = pygame.mixer.Sound('horn.mp3')
                assets['sounds']['brake'] = pygame.mixer.Sound('breaks.mp3')
                assets['sounds']['beep'] = pygame.mixer.Sound('beep.mp3')
                assets['sounds']['go'] = pygame.mixer.Sound('go.mp3')
                assets['sounds']['engine2'] = pygame.mixer.Sound('engine2.mp3')
                assets['sounds']['gun'] = pygame.mixer.Sound('gun.mp3')
                assets['sounds']['explosion'] = pygame.mixer.Sound('explosion.mp3')
                pygame.mixer.music.load('Car Chase.mp3')
            except pygame.error as e:
                print(f"Warning: Could not load sound files. {e}")
                assets['sounds'] = None
        else:
            assets['sounds'] = None

        return assets

    def run(self):
        while True:
            if self.game_state == 'INTRO':
                self.intro_loop()
            elif self.game_state == 'COUNTDOWN':
                self.countdown_loop()
            elif self.game_state == 'PLAYING':
                self.game_loop()
            elif self.game_state == 'INSTRUCTIONS':
                self.introduction()
            elif self.game_state == 'PAUSED':
                self.paused_loop()
            elif self.game_state == 'LEVEL_UP':
                self.level_up_loop()
            elif self.game_state == 'GAME_OVER':
                self.game_over_loop()

    def level_up_loop(self):
        self.gamedisplays.blit(self.assets['instruction_background'], (0, 0))
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = self.text_objects("LEVEL " + str(self.level), large_text)
        text_rect.center = (self.display_width / 2, self.display_height / 2)
        self.gamedisplays.blit(text_surf, text_rect)

        pygame.display.update()
        time.sleep(2)

        self.game_state = 'PLAYING'

    def toggle_pause(self):
        if self.game_state == 'PLAYING':
            self.game_state = 'PAUSED'
        elif self.game_state == 'PAUSED':
            self.game_state = 'PLAYING'
            if self.assets['sounds']:
                pygame.mixer.music.unpause()
                if hasattr(self, 'engine_channel'):
                    self.engine_channel.unpause()

    def paused_loop(self):
        if self.assets['sounds']:
            pygame.mixer.music.pause()
            if hasattr(self, 'engine_channel'):
                self.engine_channel.pause()

        while self.game_state == 'PAUSED':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

            self.gamedisplays.blit(self.assets['instruction_background'], (0, 0))
            large_text = pygame.font.Font('freesansbold.ttf', 115)
            text_surf, text_rect = self.text_objects("PAUSED", large_text)
            text_rect.center = (self.display_width / 2, self.display_height / 2)
            self.gamedisplays.blit(text_surf, text_rect)

            self.button("CONTINUE", 150, 450, 150, 50, GREEN, BRIGHT_GREEN, self.toggle_pause)
            self.button("MAIN MENU", 550, 450, 200, 50, RED, BRIGHT_RED, self.back_to_menu)

            pygame.display.update()
            self.clock.tick(30)

    def intro_loop(self):
        if self.assets['sounds']:
            pygame.mixer.music.stop()
            if hasattr(self, 'engine_channel'):
                self.engine_channel.stop()

        while self.game_state == 'INTRO':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()

            self.gamedisplays.blit(self.assets['intro_background'], (0, 0))
            large_text = pygame.font.Font('freesansbold.ttf', 115)
            text_surf, text_rect = self.text_objects("ROAD RAGE", large_text)
            text_rect.center = (400, 100)
            self.gamedisplays.blit(text_surf, text_rect)

            self.button("START", 150, 520, 100, 50, GREEN, BRIGHT_GREEN, self.start_game)
            self.button("QUIT", 550, 520, 100, 50, RED, BRIGHT_RED, self.quit_game)
            self.button("INSTRUCTION", 300, 520, 200, 50, BLUE, BRIGHT_BLUE, self.show_instructions)

            pygame.display.update()
            self.clock.tick(50)

    def introduction(self):
        while self.game_state == 'INSTRUCTIONS':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

            self.gamedisplays.blit(self.assets['instruction_background'], (0, 0))
            large_text = pygame.font.Font('freesansbold.ttf', 80)
            small_text = pygame.font.Font('freesansbold.ttf', 20)
            medium_text = pygame.font.Font('freesansbold.ttf', 40)

            text_surf, text_rect = self.text_objects("This is a car game in which you need to dodge the coming cars", small_text)
            text_rect.center = ((350), (200))
            self.gamedisplays.blit(text_surf, text_rect)

            text_surf, text_rect = self.text_objects("INSTRUCTION", large_text)
            text_rect.center = ((400), (100))
            self.gamedisplays.blit(text_surf, text_rect)

            stext_surf, stext_rect = self.text_objects("ARROW LEFT : LEFT TURN", small_text)
            stext_rect.center = ((150), (400))
            self.gamedisplays.blit(stext_surf, stext_rect)

            htext_surf, htext_rect = self.text_objects("ARROW RIGHT : RIGHT TURN", small_text)
            htext_rect.center = ((150), (450))
            self.gamedisplays.blit(htext_surf, htext_rect)

            atext_surf, atext_rect = self.text_objects("ARROW UP : ACCELERATOR", small_text)
            atext_rect.center = ((150), (500))
            self.gamedisplays.blit(atext_surf, atext_rect)

            rtext_surf, rtext_rect = self.text_objects("ARROW DOWN : BRAKE ", small_text)
            rtext_rect.center = ((150), (550))
            self.gamedisplays.blit(rtext_surf, rtext_rect)

            ptext_surf, ptext_rect = self.text_objects("P : PAUSE", small_text)
            ptext_rect.center = ((150), (350))
            self.gamedisplays.blit(ptext_surf, ptext_rect)

            stext_surf, stext_rect = self.text_objects("CONTROLS", medium_text)
            stext_rect.center = ((350), (300))
            self.gamedisplays.blit(stext_surf, stext_rect)

            self.button("BACK", 600, 450, 100, 50, BLUE, BRIGHT_BLUE, self.back_to_menu)

            pygame.display.update()
            self.clock.tick(30)

    def get_max_obstacles(self):
        if self.level >= 8:
            return 4
        elif self.level >= 3:
            return 3
        else:
            return 1

    def game_loop(self):
        if self.sound_enabled and self.assets['sounds']:
            self.engine_channel.play(self.assets['sounds']['engine'], -1)

        while self.game_state == 'PLAYING':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                self.player.handle_event(event)

            max_obstacles = self.get_max_obstacles()
            if len(self.obstacles) < max_obstacles:
                self.obstacles.append(Obstacle(self))

            self.player.update()
            for obstacle in self.obstacles:
                obstacle.update()
            for bullet in self.bullets:
                bullet.update()
            for explosion in self.explosions:
                explosion.update()

            # Remove bullets that are off-screen
            self.bullets = [bullet for bullet in self.bullets if bullet.y > 0]

            # Handle bullet-obstacle collisions
            for bullet in self.bullets[:]:
                for obstacle in self.obstacles[:]:
                    if bullet.y < obstacle.y + obstacle.height and bullet.y + bullet.height > obstacle.y and \
                       bullet.x < obstacle.x + obstacle.width and bullet.x + bullet.width > obstacle.x:
                        if self.assets['sounds'] and 'explosion' in self.assets['sounds']:
                            self.assets['sounds']['explosion'].play()
                        self.explosions.append(Explosion(self, obstacle.x, obstacle.y))
                        self.obstacles.remove(obstacle)
                        self.bullets.remove(bullet)
                        self.score += 25
                        break

            self.background_y += (9 + self.speed_offset)

            self.draw_background()
            self.player.draw()
            for obstacle in self.obstacles:
                obstacle.draw()
            for bullet in self.bullets:
                bullet.draw()
            for explosion in self.explosions:
                explosion.draw()

            # The speed displayed in the HUD will be the speed of the first car in the list
            display_speed = (self.obstacles[0].base_speed + self.speed_offset) if self.obstacles else (9 + self.speed_offset)
            self.display_hud(display_speed)
            self.button("PAUSE", 650, 0, 150, 50, BLUE, BRIGHT_BLUE, self.toggle_pause)

            if self.check_crash():
                if self.assets['sounds']:
                    if hasattr(self, 'engine_channel'):
                        self.engine_channel.stop()
                    self.assets['sounds']['crash'].play()

                self.lives -= 1
                if self.lives > 0:
                    # Draw the crash message on top of the final frame
                    large_text = pygame.font.Font('freesansbold.ttf', 80)
                    text_surf, text_rect = self.text_objects("YOU CRASHED", large_text)
                    text_rect.center = (self.display_width / 2, self.display_height / 2)
                    self.gamedisplays.blit(text_surf, text_rect)
                    pygame.display.update()
                    time.sleep(2)

                    self.player = Player(self)
                    self.obstacles = [Obstacle(self)]
                    self.game_state = 'PLAYING'
                    if self.assets['sounds']:
                        self.engine_channel.play(self.assets['sounds']['engine'], -1)
                else:
                    self.game_state = 'GAME_OVER'

            pygame.display.update()
            self.clock.tick(60)

    def game_over_loop(self):
        if self.assets['sounds']:
            pygame.mixer.music.stop()
            if hasattr(self, 'engine_channel'):
                self.engine_channel.stop()

        while self.game_state == 'GAME_OVER':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start_game()

            self.gamedisplays.blit(self.assets['intro_background'], (0, 0))
            large_text = pygame.font.Font('freesansbold.ttf', 115)
            text_surf, text_rect = self.text_objects("GAME OVER", large_text)
            text_rect.center = (self.display_width / 2, self.display_height / 2)
            self.gamedisplays.blit(text_surf, text_rect)

            self.button("RESTART", 150, 450, 150, 50, GREEN, BRIGHT_GREEN, self.start_game)
            self.button("MAIN MENU", 550, 450, 200, 50, RED, BRIGHT_RED, self.back_to_menu)

            pygame.display.update()
            self.clock.tick(30)

    def start_game(self):
        self.new_game()
        self.game_state = 'COUNTDOWN'
        if self.assets['sounds']:
            pygame.mixer.music.play(-1)

    def countdown_loop(self):
        self.gamedisplays.fill(GRAY)
        self.draw_background()

        countdown_font = pygame.font.Font('freesansbold.ttf', 115)
        for i in range(3, 0, -1):
            self.gamedisplays.fill(GRAY)
            self.draw_background()
            text_surf, text_rect = self.text_objects(str(i), countdown_font)
            text_rect.center = (self.display_width / 2, self.display_height / 2)
            self.gamedisplays.blit(text_surf, text_rect)
            if self.assets['sounds']:
                self.assets['sounds']['beep'].play()
            pygame.display.update()
            time.sleep(1)

        self.gamedisplays.fill(GRAY)
        self.draw_background()
        text_surf, text_rect = self.text_objects("GO!!!", countdown_font)
        text_rect.center = (self.display_width / 2, self.display_height / 2)
        self.gamedisplays.blit(text_surf, text_rect)
        if self.assets['sounds']:
            self.assets['sounds']['go'].play()
        pygame.display.update()
        time.sleep(1)

        self.game_state = 'PLAYING'

    def show_instructions(self):
        self.game_state = 'INSTRUCTIONS'

    def back_to_menu(self):
        self.game_state = 'INTRO'

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def button(self, msg, x, y, w, h, ic, ac, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.gamedisplays, ac, (x, y, w, h))
            if click[0] == 1 and action is not None:
                action()
        else:
            pygame.draw.rect(self.gamedisplays, ic, (x, y, w, h))

        small_text = pygame.font.Font("freesansbold.ttf", 20)
        text_surf, text_rect = self.text_objects(msg, small_text)
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.gamedisplays.blit(text_surf, text_rect)

    def text_objects(self, text, font):
        text_surface = font.render(text, True, BLACK)
        return text_surface, text_surface.get_rect()

    def display_hud(self, speed):
        font = pygame.font.SysFont(None, 25)

        passed_text = font.render("Passed: " + str(self.passed), True, BLACK)
        self.gamedisplays.blit(passed_text, (0, 50))

        score_text = font.render("Score: " + str(self.score), True, RED)
        self.gamedisplays.blit(score_text, (0, 30))

        lives_text = font.render("Lives: " + str(self.lives), True, BLACK)
        self.gamedisplays.blit(lives_text, (0, 70))

        self.draw_speedometer(speed)

    def draw_speedometer(self, speed):
        x = self.display_width - 100
        y = self.display_height - 100
        radius = 50

        # Draw the speedometer arc
        pygame.draw.arc(self.gamedisplays, BLACK, (x - radius, y - radius, radius * 2, radius * 2), math.pi, 2 * math.pi, 3)

        # Draw the needle
        angle = math.pi + (speed / 30) * math.pi
        if angle > 2 * math.pi:
            angle = 2 * math.pi
        if angle < math.pi:
            angle = math.pi

        end_x = x + radius * math.cos(angle)
        end_y = y + radius * math.sin(angle)
        pygame.draw.line(self.gamedisplays, RED, (x, y), (end_x, end_y), 3)

    def draw_background(self):
        self.gamedisplays.fill(GRAY)
        rel_y = self.background_y % self.assets['backgroundpic'].get_rect().height
        self.gamedisplays.blit(self.assets['backgroundpic'], (0, rel_y - self.assets['backgroundpic'].get_rect().height))
        self.gamedisplays.blit(self.assets['backgroundpic'], (700, rel_y - self.assets['backgroundpic'].get_rect().height))
        if rel_y < self.display_height:
            self.gamedisplays.blit(self.assets['backgroundpic'], (0, rel_y))
            self.gamedisplays.blit(self.assets['backgroundpic'], (700, rel_y))

        # Draw strips
        rel_y_strip = self.background_y % self.assets['yellow_strip'].get_rect().height
        for i in range(-2, self.display_height // self.assets['yellow_strip'].get_rect().height + 2):
            self.gamedisplays.blit(self.assets['yellow_strip'], (400, rel_y_strip + i * self.assets['yellow_strip'].get_rect().height))
            self.gamedisplays.blit(self.assets['strip'], (120, rel_y_strip + i * self.assets['strip'].get_rect().height))
            self.gamedisplays.blit(self.assets['strip'], (680, rel_y_strip + i * self.assets['strip'].get_rect().height))

    def check_crash(self):
        if self.player.x > 690 - CAR_WIDTH or self.player.x < 110:
            return True
        for obstacle in self.obstacles:
            if self.player.y < obstacle.y + obstacle.height:
                if self.player.x > obstacle.x and self.player.x < obstacle.x + obstacle.width or \
                   self.player.x + CAR_WIDTH > obstacle.x and self.player.x + CAR_WIDTH < obstacle.x + obstacle.width:
                    return True
        return False

class Bullet:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.speed = -10
        self.width = 4
        self.height = 10
        self.color = (255, 255, 0) # Yellow

    def update(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(self.game.gamedisplays, self.color, (self.x, self.y, self.width, self.height))

class Explosion:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.image = self.game.assets.get('boom')
        self.lifetime = 0.5 # seconds
        self.spawn_time = time.time()

    def update(self):
        if time.time() - self.spawn_time > self.lifetime:
            self.game.explosions.remove(self)

    def draw(self):
        if self.image:
            self.game.gamedisplays.blit(self.image, (self.x, self.y))

class Player:
    def __init__(self, game):
        self.game = game
        # Center of road is 400. Car width is 56. 400 - (56/2) = 372
        self.x = 372
        self.y = (game.display_height * 0.6)
        self.x_change = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x_change = -5
            elif event.key == pygame.K_RIGHT:
                self.x_change = 5
            elif event.key == pygame.K_p:
                self.game.toggle_pause()
            elif event.key == pygame.K_UP:
                # Decrease the speed offset to make obstacles move slower, creating the illusion of player acceleration.
                self.game.speed_offset = max(-5, self.game.speed_offset - 2)
                if self.game.assets['sounds'] and 'engine2' in self.game.assets['sounds']:
                    self.game.assets['sounds']['engine2'].play()
            elif event.key == pygame.K_DOWN:
                # Increase the speed offset to make obstacles move faster, creating the illusion of player braking.
                self.game.speed_offset = min(10, self.game.speed_offset + 2)
                if self.game.assets['sounds']:
                    self.game.assets['sounds']['brake'].play()
            elif event.key == pygame.K_LSHIFT:
                if self.game.assets['sounds']:
                    self.game.assets['sounds']['horn'].play()
            elif event.key == pygame.K_SPACE:
                if self.game.level >= 2:
                    self.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.x_change = 0

    def update(self):
        self.x += self.x_change

    def shoot(self):
        if self.game.assets['sounds'] and 'gun' in self.game.assets['sounds']:
            self.game.assets['sounds']['gun'].play()
        bullet1 = Bullet(self.game, self.x + 10, self.y)
        bullet2 = Bullet(self.game, self.x + CAR_WIDTH - 14, self.y)
        self.game.bullets.append(bullet1)
        self.game.bullets.append(bullet2)

    def draw(self):
        self.game.gamedisplays.blit(self.game.assets['carimg'], (self.x, self.y))

class Obstacle:
    def __init__(self, game):
        self.game = game
        self.x = random.randrange(200, (game.display_width - 200))
        self.y = -600
        self.base_speed = (5 + (game.level - 1) * 1) + random.choice([0, 1, 2])
        self.x_change = random.choice([-1, 1])
        self.image = random.choice(self.game.assets['obstacle_cars'])
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def update(self):
        self.y += self.base_speed + self.game.speed_offset
        self.x += self.x_change

        if self.x < 110 or self.x > 690 - self.width:
            self.x_change *= -1

        if self.y > self.game.display_height:
            self.y = -self.height
            self.x = random.randrange(170, (self.game.display_width - 170))
            self.image = random.choice(self.game.assets['obstacle_cars'])
            self.base_speed = (5 + (game.level - 1) * 1) + random.choice([0, 1, 2])
            self.game.passed += 1
            self.game.score = self.game.passed * 10

            if self.game.score >= self.game.next_life_milestone:
                self.game.lives += 1
                self.game.next_life_milestone += 500

            if self.game.passed > 0 and self.game.passed % 10 == 0:
                self.game.level += 1
                self.game.game_state = 'LEVEL_UP'

    def draw(self):
        self.game.gamedisplays.blit(self.image, (self.x, self.y))

if __name__ == '__main__':
    game = Game()
    game.run()
