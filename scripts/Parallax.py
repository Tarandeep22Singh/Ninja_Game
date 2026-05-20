import random
import pygame

class Cloud:
    def __init__(self, pos, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )
        surf_w = surf.get_width()
        surf_h = surf.get_height()
        img_w  = self.img.get_width()
        img_h  = self.img.get_height()
        surf.blit(
            self.img,
            (
                render_pos[0] % (surf_w + img_w) - img_w,
                render_pos[1] % (surf_h + img_h) - img_h,
            ),
        )


class Clouds:
    def __init__(self, cloud_images, count=16):
        self.clouds = sorted(
            [
                Cloud(
                    (random.random() * 99999, random.random() * 99999),
                    random.choice(cloud_images),
                    random.random() * 0.05 + 0.05,
                    random.random() * 0.6 + 0.2,
                )
                for _ in range(count)
            ],
            key=lambda c: c.depth,
        )

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)


class ParallaxBackground:
    def __init__(self, layers,target_size):
        
        self._surf_w = None  # lazily cached on first render
        self._surf_h = None
        self._layers = []    # (img, depth, img_w, img_h) — avoids repeated .get_width()

        for img, depth in layers:
            img_w, img_h = img.get_size()
            scale_factor = target_size[0] / img_w
            new_h = int(img_h * scale_factor)
            scaled = pygame.transform.scale(img, (target_size[0], new_h))
            self._layers.append((scaled, depth, target_size[0], new_h))

    def render(self, surf, offset=(0, 0)):
        surf_w = surf.get_width()
        surf_h = surf.get_height()

        for img, depth, img_w, img_h in self._layers:  # ← _layers, and unpack all 4 values
            parallax_x = int(offset[0] * depth)
            parallax_y = int(offset[1] * depth * 0.3)

            y = surf_h - img_h + parallax_y

            x = -(parallax_x % img_w)
            while x < surf_w:
                surf.blit(img, (x, y))
                x += img_w