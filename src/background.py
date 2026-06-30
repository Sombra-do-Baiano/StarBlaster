"""
background.py
Fundo de estrelas com parallax scrolling.
Usa STAR_COUNT, STAR_SPEED_MIN/MAX, STAR_SIZE_FACTOR de config.py.
Se BACKGROUND_IMAGE estiver definida, desenha a imagem antes das estrelas.
Se STAR_SPRITE estiver definida, usa o sprite no lugar do círculo.
"""

import pygame
import random
from src.config import (
    W, H,
    STAR_COUNT, STAR_SPEED_MIN, STAR_SPEED_MAX, STAR_SIZE_FACTOR,
    BACKGROUND_IMAGE, STAR_SPRITE,
)


class StarField:
    def __init__(self):
        self.stars = [
            (random.randint(0, W), random.randint(0, H),
             random.uniform(STAR_SPEED_MIN, STAR_SPEED_MAX))
            for _ in range(STAR_COUNT)
        ]

        # carrega imagem de fundo, se configurada
        self._bg: pygame.Surface | None = None
        if BACKGROUND_IMAGE:
            try:
                img = pygame.image.load(BACKGROUND_IMAGE).convert()
                self._bg = pygame.transform.scale(img, (W, H))
            except Exception as e:
                print(f"[background] Não foi possível carregar {BACKGROUND_IMAGE}: {e}")

        # carrega sprite de estrela, se configurado
        self._star_sprite: pygame.Surface | None = None
        if STAR_SPRITE:
            try:
                self._star_sprite = pygame.image.load(STAR_SPRITE).convert_alpha()
            except Exception as e:
                print(f"[background] Não foi possível carregar {STAR_SPRITE}: {e}")

    def update(self):
        self.stars = [
            ((x - spd * 1.5) % W, y, spd)
            for x, y, spd in self.stars
        ]

    def draw(self, surf: pygame.Surface):
        # imagem de fundo
        if self._bg:
            surf.blit(self._bg, (0, 0))

        # estrelas
        for x, y, spd in self.stars:
            if self._star_sprite:
                size = max(1, int(spd * STAR_SIZE_FACTOR * 4))
                scaled = pygame.transform.scale(self._star_sprite, (size, size))
                surf.blit(scaled, (int(x) - size // 2, int(y) - size // 2))
            else:
                brightness = int(spd / STAR_SPEED_MAX * 200 + 55)
                radius = max(1, int(spd * STAR_SIZE_FACTOR))
                pygame.draw.circle(
                    surf,
                    (brightness, brightness, brightness),
                    (int(x), int(y)),
                    radius,
                )
