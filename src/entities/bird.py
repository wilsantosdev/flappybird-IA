import os

import pygame


class Bird:
    __max_rotation = 25
    __imgs = [pygame.image.load(os.path.join("src", "assets", "imgs", "bird" + str(x) + ".png")) for x in range(1, 4)]
    __rotation_speed = 20
    __animation_time = 5

    def __init__(self, x, y):
        self.__x = x
        self.__y = y
        self.__tilt = 0
        self.__tick_count = 0
        self.__velocity = 0
        self.__height = self.__y
        self.__img_count = 0
        self.__img = self.__imgs[0]

    def jump(self):
        self.__velocity = -7.5
        self.__tick_count = 0
        self.__height = self.__y

    def move(self):
        self.__tick_count += 1

        displacement = self.__velocity * self.__tick_count + 0.5 * 3 * self.__tick_count ** 2

        if displacement >= 16:
            displacement = (displacement / abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.__y = self.__y + displacement

        if displacement < 0 or self.__y < self.__height + 50:  # tilt up
            if self.__tilt < self.__max_rotation:
                self.__tilt = self.__max_rotation
        else:
            if self.__tilt > -90:
                self.__tilt -= self.__rotation_speed

    def draw(self, win):
        self.__img_count += 1

        if self.__img_count <= self.__animation_time:
            self.__img = self.__imgs[0]
        elif self.__img_count <= self.__animation_time * 2:
            self.__img = self.__imgs[1]
        elif self.__img_count <= self.__animation_time * 3:
            self.__img = self.__imgs[2]
        elif self.__img_count <= self.__animation_time * 4:
            self.__img = self.__imgs[1]
        elif self.__img_count == self.__animation_time * 4 + 1:
            self.__img = self.__imgs[0]
            self.__img_count = 0

        if self.__tilt <= -80:
            self.__img = self.__imgs[1]
            self.__img_count = self.__animation_time * 2

        self.blitRotateCenter(win, self.__img, (self.__x, self.__y), self.__tilt)

    @staticmethod
    def blitRotateCenter(win, image, top_left, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)

        win.blit(rotated_image, new_rect.topleft)

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_img(self):
        return self.__img

    def get_mask(self):
        return pygame.mask.from_surface(self.__img)

