import os
import pygame


class Background:
    def __init__(self):
        self.bg_img = pygame.image.load(os.path.join("src", "assets", "imgs", "bg.png")).convert_alpha()

    def draw(self, win):
        win.blit(self.bg_img, (0, 0))
