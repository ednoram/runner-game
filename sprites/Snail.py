import pygame

from sprites.Obstacle import Obstacle


class Snail(Obstacle):
    def __init__(self):
        image1 = pygame.image.load("assets/graphics/Snail/snail1.png").convert_alpha()
        image2 = pygame.image.load("assets/graphics/Snail/snail2.png").convert_alpha()

        super().__init__(image1, image2, 300)
