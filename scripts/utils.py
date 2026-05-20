import os
import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_image_alpha(path):
    return pygame.image.load(BASE_IMG_PATH + path).convert_alpha()

def load_images(path):
    return [
        load_image(path + '/' + img_name)
        for img_name in sorted(os.listdir(BASE_IMG_PATH + path))
    ]

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
        self._max_frame = img_dur * len(images) - 1  # cached, avoids recomputing every update

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self._max_frame + 1)
        else:
            self.frame = min(self.frame + 1, self._max_frame)
            if self.frame >= self._max_frame:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]