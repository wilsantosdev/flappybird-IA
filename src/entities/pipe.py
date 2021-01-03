import os
import random

import pygame


class Pipe:
    __gap = 100
    __speed = 5

    def __init__(self, x):
        self.__x = x
        self.__height = 0

        self.__pipe_top_y = 0
        self.__pipe_bottom_y = 0

        self.__pipe_bottom = pygame.image.load(os.path.join("src", "assets", "imgs", "pipe.png")).convert_alpha()
        self.__pipe_top = pygame.transform.flip(self.__pipe_bottom, False, True)

        self.__passed = False

        self.set_height()

    def get_pipe_top(self):
        return self.__pipe_top

    def get_pipe_bottom(self):
        return self.__pipe_bottom

    def set_passed(self, passed):
        self.__passed = passed

    def has_passed(self):
        return self.__passed

    def get_height(self):
        return self.__height

    def get_x(self):
        return self.__x

    def get_pipe_top_y(self):
        return self.__pipe_top_y

    def get_pipe_bottom_y(self):
        return self.__pipe_bottom_y

    def set_height(self):
        self.__height = random.randrange(0, 300)
        self.__pipe_top_y = self.__height - self.__pipe_top.get_height()
        self.__pipe_bottom_y = self.__height + self.__gap

    def __move(self):
        self.__x -= self.__speed

    def draw(self, win):
        self.__move()
        win.blit(self.__pipe_top, (self.__x, self.__pipe_top_y))
        win.blit(self.__pipe_bottom, (self.__x, self.__pipe_bottom_y))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.__pipe_top)
        bottom_mask = pygame.mask.from_surface(self.__pipe_bottom)
        top_offset = (self.__x - bird.get_x(), self.__pipe_top_y - round(bird.get_y()))
        bottom_offset = (self.__x - bird.get_x(), self.__pipe_bottom_y - round(bird.get_y()))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if b_point or t_point:
            return True

        return False

