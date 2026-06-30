"""
draw_utils.py
Funções puras para desenhar sprites via primitivas do pygame.
Nenhuma classe de jogo aqui — só formas.
"""

import pygame
import math
from config import RED, ORANGE, YELLOW, GREEN, WHITE, CYAN, PURPLE

# cache de superfícies de sprite já carregadas (evita reabrir arquivo a cada frame)
_heart_cache: dict[str, pygame.Surface | None] = {}


def draw_ship(surf: pygame.Surface, x, y, w, h, color, highlight):
    """Nave do jogador (aponta para a direita)."""
    pts = [
        (x + w,       y + h // 2),
        (x + w * 0.3, y),
        (x,           y + h // 4),
        (x,           y + h * 3 // 4),
        (x + w * 0.3, y + h),
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, highlight, pts, 2)
    pygame.draw.ellipse(surf, highlight,
                        (x + w * 0.45, y + h * 0.35, w * 0.3, h * 0.3))


def draw_enemy_fighter(surf: pygame.Surface, x, y, w, h, color):
    """Nave inimiga angular (aponta para a esquerda)."""
    pts = [
        (x,           y + h // 2),
        (x + w * 0.3, y),
        (x + w,       y + h // 4),
        (x + w,       y + h * 3 // 4),
        (x + w * 0.3, y + h),
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, RED, pts, 2)
    pygame.draw.circle(surf, ORANGE, (int(x + w * 2 / 3), int(y + h // 2)), h // 5)


def draw_enemy_ufo(surf: pygame.Surface, x, y, r, color):
    """OVNI inimigo."""
    pygame.draw.ellipse(surf, color, (x - r, y - r // 2, r * 2, r))
    pygame.draw.ellipse(surf,
                        (color[0] // 2, color[1] // 2, color[2] // 2),
                        (x - r // 2, y - r * 3 // 4, r, r // 2))
    pygame.draw.ellipse(surf, RED, (x - r, y - r // 2, r * 2, r), 2)


def draw_boss(surf: pygame.Surface, x, y, w, h, color, hp_ratio: float):
    """Boss com barra de HP embutida."""
    pts = [
        (x,           y + h // 2),
        (x + w * 0.2, y),
        (x + w * 0.6, y + h * 0.1),
        (x + w,       y + h // 2),
        (x + w * 0.6, y + h * 0.9),
        (x + w * 0.2, y + h),
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, ORANGE, pts, 3)
    # barra de HP
    bar_w = int(w * hp_ratio)
    pygame.draw.rect(surf, RED,   (x, y - 14, w, 8))
    pygame.draw.rect(surf, GREEN, (x, y - 14, bar_w, 8))
    # olho
    pygame.draw.circle(surf, YELLOW, (int(x + w * 2 / 3), int(y + h // 2)), h // 5)
    pygame.draw.circle(surf, RED,    (int(x + w * 2 / 3), int(y + h // 2)), h // 8)


def draw_heart(surf: pygame.Surface, cx: int, cy: int, size: int, filled: bool):
    """
    Desenha um coração centrado em (cx, cy).
    - Se HEART_SPRITE_FULL / HEART_SPRITE_EMPTY estiverem definidos em config,
      usa os sprites (escalados para size x size pixels).
    - Caso contrário, desenha via polígono matemático.
    filled = True → vida disponível;  False → vida perdida.
    """
    from config import HEART_SPRITE_FULL, HEART_SPRITE_EMPTY

    sprite_path = HEART_SPRITE_FULL if filled else HEART_SPRITE_EMPTY

    if sprite_path:
        # cache de sprites já carregados para não reabrir o arquivo a cada frame
        if sprite_path not in _heart_cache:
            try:
                img = pygame.image.load(sprite_path).convert_alpha()
                _heart_cache[sprite_path] = img
            except Exception as e:
                print(f"[draw_utils] Não foi possível carregar sprite de coração: {e}")
                _heart_cache[sprite_path] = None

        img = _heart_cache[sprite_path]
        if img is not None:
            scaled = pygame.transform.scale(img, (size * 2, size * 2))
            surf.blit(scaled, (cx - size, cy - size))
            return
        # se falhou no load, cai no procedural abaixo

    # ── Modo procedural ──────────────────────────────────────────────────────
    color  = (220, 40, 60) if filled else (60, 40, 50)
    border = (255, 80, 100) if filled else (100, 70, 80)

    pts = []
    for i in range(32):
        t  = math.pi * 2 * i / 32 - math.pi / 2
        hx = size * 16 * (math.sin(t) ** 3)
        hy = -size * (13 * math.cos(t) - 5 * math.cos(2*t)
                      - 2 * math.cos(3*t) - math.cos(4*t))
        scale = size / 16
        pts.append((cx + hx * scale, cy + hy * scale))

    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, border, pts, 2)
