import os

import pygame


class Floor:
    def __init__(self, height):
        self.__floor_img = pygame.image.load(os.path.join("src", "assets", "imgs", "base.png")).convert_alpha()
        self.__x = 0
        self.__x2 = self.__floor_img.get_width()
        self.__speed = 5
        self.__height = height
        self.__width = self.__floor_img.get_width()

    def get_height(self):
        return self.__height

    def draw(self, win):
        self.move()
        win.blit(self.__floor_img, (self.__x, self.__height - self.__floor_img.get_height()))
        win.blit(self.__floor_img, (self.__x2, self.__height - self.__floor_img.get_height()))

    def move(self):
        self.__x -= self.__speed
        self.__x2 -= self.__speed

        if self.__x + self.__width < 0:
            self.__x = self.__x2 + self.__width

        if self.__x2 + self.__width < 0:
            self.__x2 = self.__x + self.__width
