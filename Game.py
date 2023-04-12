import pygame
from random import randint

from sprites.Fly import Fly
from sprites.Snail import Snail
from sprites.Player import Player
from constants import FRAMES_PER_SECOND, SCREEN_HEIGHT, SCREEN_WIDTH, SKY_HEIGHT


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Runner")

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.score = 0
        self.start_time = 0
        self.game_over = False

        self.main_font = pygame.font.Font("assets/font/Pixeltype.ttf", 50)

        self.sky_surface = pygame.image.load("assets/graphics/sky.png").convert()
        self.ground_surface = pygame.image.load("assets/graphics/ground.png").convert()

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())

        self.obstacle_group = pygame.sprite.Group()

        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 900)

    def restart(self):
        if self.game_over:
            self.obstacle_group.empty()
            self.game_over = False
            self.score = 0
            self.start_time = pygame.time.get_ticks()

    def end(self):
        pygame.quit()
        exit()

    def draw_background(self):
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, SKY_HEIGHT))

    def draw_score(self):
        score_text = self.main_font.render(f"Score: {self.score}", False, "#333333")
        score_rect = score_text.get_rect(topright=(SCREEN_WIDTH - 20, 20))
        self.screen.blit(score_text, score_rect)

    def draw_game_over(self):
        game_over_text = self.main_font.render("Game Over", False, "Red")
        game_over_rect = game_over_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        )
        self.screen.blit(game_over_text, game_over_rect)

    def add_obstacle(self):
        if not self.game_over:
            if randint(0, 10) > 3:
                self.obstacle_group.add(Snail())
            else:
                self.obstacle_group.add(Fly())

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.end()
            elif event.type == self.obstacle_timer:
                self.add_obstacle()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.restart()

    def handle_collision(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.obstacle_group, False):
            self.game_over = True

    def update_score(self):
        self.score = int((pygame.time.get_ticks() - self.start_time) / 80)

    def update(self):
        self.draw_background()
        self.handle_events()
        self.player.draw(self.screen)
        self.obstacle_group.draw(self.screen)
        self.draw_score()
        self.handle_collision()

        if self.game_over:
            self.draw_game_over()
        else:
            self.player.update()
            self.obstacle_group.update()
            self.update_score()

        pygame.display.update()
        self.clock.tick(FRAMES_PER_SECOND)
