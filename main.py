import pygame
import sys
import time
import random

# Constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
CAR_WIDTH = 56

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
        self.display_width = DISPLAY_WIDTH
        self.display_height = DISPLAY_HEIGHT
        self.gamedisplays = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Road Rage")
        self.clock = pygame.time.Clock()
        self.game_state = 'INTRO'
        self.pause = False
        self.background_y = 0
        self.lives = 3
        self.level = 1

        # Load assets
        self.assets = self.load_assets()

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
            ]
        }
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
            elif self.game_state == 'CRASHED':
                self.crashed_loop()
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

    def crashed_loop(self):
        self.gamedisplays.blit(self.assets['instruction_background'], (0, 0))
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = self.text_objects("YOU CRASHED", large_text)
        text_rect.center = (self.display_width / 2, self.display_height / 2)
        self.gamedisplays.blit(text_surf, text_rect)

        pygame.display.update()
        time.sleep(2)

        self.player = Player(self)
        self.obstacle = Obstacle(self)

        self.game_state = 'COUNTDOWN'

    def toggle_pause(self):
        if self.game_state == 'PLAYING':
            self.game_state = 'PAUSED'
        elif self.game_state == 'PAUSED':
            self.game_state = 'PLAYING'

    def paused_loop(self):
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
        while self.game_state == 'INTRO':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

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

            atext_surf, atext_rect = self.text_objects("A : ACCELERATOR", small_text)
            atext_rect.center = ((150), (500))
            self.gamedisplays.blit(atext_surf, atext_rect)

            rtext_surf, rtext_rect = self.text_objects("B : BRAKE ", small_text)
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

    def game_loop(self):
        self.player = Player(self)
        self.obstacle = Obstacle(self)

        while self.game_state == 'PLAYING':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                self.player.handle_event(event)

            self.player.update()
            self.obstacle.update()
            self.background_y += self.obstacle.speed

            self.draw_background()
            self.player.draw()
            self.obstacle.draw()
            self.display_hud(self.obstacle.passed, self.obstacle.score)
            self.button("PAUSE", 650, 0, 150, 50, BLUE, BRIGHT_BLUE, self.toggle_pause)

            if self.check_crash():
                self.lives -= 1
                if self.lives > 0:
                    self.game_state = 'CRASHED'
                else:
                    self.game_state = 'GAME_OVER'

            pygame.display.update()
            self.clock.tick(60)

    def game_over_loop(self):
        while self.game_state == 'GAME_OVER':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()

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
        self.game_state = 'COUNTDOWN'

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
            pygame.display.update()
            time.sleep(1)

        self.gamedisplays.fill(GRAY)
        self.draw_background()
        text_surf, text_rect = self.text_objects("GO!!!", countdown_font)
        text_rect.center = (self.display_width / 2, self.display_height / 2)
        self.gamedisplays.blit(text_surf, text_rect)
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

    def display_hud(self, passed, score):
        font = pygame.font.SysFont(None, 25)

        passed_text = font.render("Passed: " + str(passed), True, BLACK)
        self.gamedisplays.blit(passed_text, (0, 50))

        score_text = font.render("Score: " + str(score), True, RED)
        self.gamedisplays.blit(score_text, (0, 30))

        lives_text = font.render("Lives: " + str(self.lives), True, BLACK)
        self.gamedisplays.blit(lives_text, (0, 70))

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
        if self.player.y < self.obstacle.y + self.obstacle.height:
            if self.player.x > self.obstacle.x and self.player.x < self.obstacle.x + self.obstacle.width or \
               self.player.x + CAR_WIDTH > self.obstacle.x and self.player.x + CAR_WIDTH < self.obstacle.x + self.obstacle.width:
                return True
        return False

class Player:
    def __init__(self, game):
        self.game = game
        self.x = (game.display_width * 0.45)
        self.y = (game.display_height * 0.8)
        self.x_change = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.x_change = -5
            elif event.key == pygame.K_RIGHT:
                self.x_change = 5
            elif event.key == pygame.K_p:
                self.game.toggle_pause()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.x_change = 0

    def update(self):
        self.x += self.x_change

    def draw(self):
        self.game.gamedisplays.blit(self.game.assets['carimg'], (self.x, self.y))

class Obstacle:
    def __init__(self, game):
        self.game = game
        self.x = random.randrange(200, (game.display_width - 200))
        self.y = -750
        self.speed = 9
        self.width = 56
        self.height = 125
        self.passed = 0
        self.score = 0
        self.image = random.choice(self.game.assets['obstacle_cars'])

    def update(self):
        self.y += self.speed
        if self.y > self.game.display_height:
            self.y = 0 - self.height
            self.x = random.randrange(170, (self.game.display_width - 170))
            self.image = random.choice(self.game.assets['obstacle_cars'])
            self.passed += 1
            self.score = self.passed * 10
            if self.passed % 10 == 0:
                self.game.level += 1
                self.speed += 2
                self.game.game_state = 'LEVEL_UP'

    def draw(self):
        self.game.gamedisplays.blit(self.image, (self.x, self.y))


if __name__ == '__main__':
    game = Game()
    game.run()
