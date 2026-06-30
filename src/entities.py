"""
entities.py
Entidades do jogador: Player, Bullet, PowerUp, Particle.
Todos os valores numéricos vêm de config.py.
"""

import pygame
import random
import math
from src.config import (
    W, H,
    CYAN, WHITE, ORANGE, PURPLE, BLACK,
    # player
    PLAYER_W, PLAYER_H, PLAYER_SPEED, PLAYER_START_X,
    PLAYER_INVINCIBLE_FRAMES, PLAYER_MAX_X_FRACTION,
    PLAYER_SHOOT_RATE_NORMAL, PLAYER_SHOOT_RATE_RAPID,
    PLAYER_SHOOT_RATE_SPREAD, PLAYER_SHOOT_RATE_BIGSHOT,
    PLAYER_POWER_DURATION,
    # tiros
    BULLET_PLAYER_W, BULLET_PLAYER_H, BULLET_PLAYER_VX,
    BULLET_PLAYER_DMG, BULLET_PLAYER_COLOR,
    BULLET_SPREAD_W, BULLET_SPREAD_H, BULLET_SPREAD_VX,
    BULLET_SPREAD_ANGLES, BULLET_SPREAD_DMG, BULLET_SPREAD_COLOR,
    BULLET_BIG_W, BULLET_BIG_H, BULLET_BIG_VX,
    BULLET_BIG_DMG, BULLET_BIG_COLOR,
    # powerups
    POWERUP_RADIUS, POWERUP_SPEED, POWERUP_BOB_AMP, POWERUP_BOB_FREQ,
    POWERUP_COLORS, POWERUP_LABELS,
    # partículas
    PARTICLE_LIFE_MIN, PARTICLE_LIFE_MAX,
    PARTICLE_VEL_MIN, PARTICLE_VEL_MAX,
    PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX, PARTICLE_GRAVITY,
    # geral
    MAX_LIVES, HEART_SIZE, HEART_SPACING, fonts,
)
from src.draw_utils import draw_ship, draw_heart


# ── Particle ──────────────────────────────────────────────────────────────────

class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=None, size=None):
        self.x, self.y = float(x), float(y)
        self.color = color
        self.vx = vx if vx is not None else random.uniform(PARTICLE_VEL_MIN, PARTICLE_VEL_MAX)
        self.vy = vy if vy is not None else random.uniform(PARTICLE_VEL_MIN, PARTICLE_VEL_MAX)
        self.life     = life or random.randint(PARTICLE_LIFE_MIN, PARTICLE_LIFE_MAX)
        self.max_life = self.life
        self.size     = size or random.uniform(PARTICLE_SIZE_MIN, PARTICLE_SIZE_MAX)

    def update(self):
        self.x  += self.vx
        self.y  += self.vy
        self.vy += PARTICLE_GRAVITY
        self.life -= 1

    def draw(self, surf: pygame.Surface):
        alpha = self.life / self.max_life
        r = int(self.color[0] * alpha)
        g = int(self.color[1] * alpha)
        b = int(self.color[2] * alpha)
        s = max(1, int(self.size * alpha))
        pygame.draw.circle(surf, (r, g, b), (int(self.x), int(self.y)), s)


def explode(particles: list, x, y, color, n: int = 25):
    for _ in range(n):
        particles.append(Particle(x, y, color))


# ── Bullet ────────────────────────────────────────────────────────────────────

class Bullet:
    def __init__(self, x, y, vx, vy, color, dmg: int = 1, w: int = 14, h: int = 5):
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = vx, vy
        self.color = color
        self.dmg   = dmg
        self.w, self.h = w, h
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x > W + 20 or self.x < -20 or self.y < -20 or self.y > H + 20:
            self.alive = False

    def draw(self, surf: pygame.Surface):
        glow = pygame.Surface((self.w + 8, self.h + 8), pygame.SRCALPHA)
        r, g, b = self.color
        pygame.draw.ellipse(glow, (r, g, b, 60), (0, 0, self.w + 8, self.h + 8))
        surf.blit(glow, (self.x - self.w // 2 - 4, self.y - self.h // 2 - 4))
        pygame.draw.ellipse(surf, self.color,
                            (self.x - self.w // 2, self.y - self.h // 2, self.w, self.h))

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.w // 2, self.y - self.h // 2, self.w, self.h)


# ── PowerUp ───────────────────────────────────────────────────────────────────

POWERUP_TYPES = ["rapid", "spread", "shield", "bigshot"]


class PowerUp:
    def __init__(self, x, y, kind: str):
        self.x, self.y = float(x), float(y)
        self.kind  = kind
        self.alive = True
        self.r     = POWERUP_RADIUS
        self.t     = 0.0

    def update(self):
        self.x -= POWERUP_SPEED
        self.t += POWERUP_BOB_FREQ
        if self.x < -30:
            self.alive = False

    def draw(self, surf: pygame.Surface):
        bob = math.sin(self.t) * POWERUP_BOB_AMP
        c   = POWERUP_COLORS[self.kind]
        cx, cy = int(self.x), int(self.y + bob)
        pygame.draw.circle(surf, c, (cx, cy), self.r)
        pygame.draw.circle(surf, WHITE, (cx, cy), self.r, 2)
        lbl = fonts["sm"].render(POWERUP_LABELS[self.kind], True, BLACK)
        surf.blit(lbl, (cx - lbl.get_width() // 2, cy - lbl.get_height() // 2))

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r * 2, self.r * 2)


# ── Player ────────────────────────────────────────────────────────────────────

class Player:
    def __init__(self):
        self.w, self.h = PLAYER_W, PLAYER_H
        self.x = float(PLAYER_START_X)
        self.y = float(H // 2 - self.h // 2)
        self.spd = PLAYER_SPEED

        self.lives = MAX_LIVES
        self.alive = True

        self.shoot_cd   = 0
        self.shoot_rate = PLAYER_SHOOT_RATE_NORMAL
        self.power      = "normal"
        self.power_timer = 0

        self.shield       = False
        self.shield_timer = 0
        self.invincible   = 0
        self.engine_t     = 0

    def update(self, keys: pygame.key.ScancodeWrapper):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= self.spd
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += self.spd
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= self.spd
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += self.spd

        max_x = W * PLAYER_MAX_X_FRACTION
        self.x = max(0.0, min(max_x, self.x + dx))
        self.y = max(0.0, min(float(H - self.h), self.y + dy))

        if self.shoot_cd > 0:
            self.shoot_cd -= 1

        if self.power_timer > 0:
            self.power_timer -= 1
            if self.power_timer == 0:
                self.power = "normal"
                self.shoot_rate = PLAYER_SHOOT_RATE_NORMAL

        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False

        if self.invincible > 0:
            self.invincible -= 1

        self.engine_t += 1

    def shoot(self, bullets: list):
        if self.shoot_cd > 0:
            return
        self.shoot_cd = self.shoot_rate
        cx = self.x + self.w
        cy = self.y + self.h // 2

        if self.power in ("normal", "rapid"):
            bullets.append(Bullet(cx, cy,
                                  BULLET_PLAYER_VX, 0,
                                  BULLET_PLAYER_COLOR,
                                  dmg=BULLET_PLAYER_DMG,
                                  w=BULLET_PLAYER_W, h=BULLET_PLAYER_H))

        elif self.power == "spread":
            for angle in BULLET_SPREAD_ANGLES:
                rad = math.radians(angle)
                bullets.append(Bullet(cx, cy,
                                      math.cos(rad) * BULLET_SPREAD_VX,
                                      math.sin(rad) * BULLET_SPREAD_VX,
                                      BULLET_SPREAD_COLOR,
                                      dmg=BULLET_SPREAD_DMG,
                                      w=BULLET_SPREAD_W, h=BULLET_SPREAD_H))

        elif self.power == "bigshot":
            bullets.append(Bullet(cx, cy,
                                  BULLET_BIG_VX, 0,
                                  BULLET_BIG_COLOR,
                                  dmg=BULLET_BIG_DMG,
                                  w=BULLET_BIG_W, h=BULLET_BIG_H))

    def apply_power(self, kind: str):
        dur = PLAYER_POWER_DURATION
        if kind == "rapid":
            self.power, self.shoot_rate, self.power_timer = "rapid",   PLAYER_SHOOT_RATE_RAPID,   dur
        elif kind == "spread":
            self.power, self.shoot_rate, self.power_timer = "spread",  PLAYER_SHOOT_RATE_SPREAD,  dur
        elif kind == "bigshot":
            self.power, self.shoot_rate, self.power_timer = "bigshot", PLAYER_SHOOT_RATE_BIGSHOT, dur
        elif kind == "shield":
            self.shield       = True
            self.shield_timer = dur

    def hit(self, dmg: int = 1) -> bool:
        if self.invincible > 0:
            return False
        if self.shield:
            self.shield = False
            self.shield_timer = 0
            self.invincible = 40
            return False
        self.lives -= dmg
        self.invincible = PLAYER_INVINCIBLE_FRAMES
        if self.lives <= 0:
            self.lives = 0
            self.alive = False
        return True

    def draw(self, surf: pygame.Surface):
        flame_len = 18 + math.sin(self.engine_t * 0.3) * 8
        for i in range(3):
            fy    = self.y + self.h // 4 + i * (self.h // 4)
            flen  = flame_len * (1 - i * 0.2)
            pygame.draw.polygon(surf, ORANGE, [
                (self.x,        fy),
                (self.x - flen, fy - 5),
                (self.x - flen, fy + 5),
            ])

        if self.invincible % 8 < 4:
            draw_ship(surf, self.x, self.y, self.w, self.h, CYAN, WHITE)

        if self.shield:
            t = pygame.time.get_ticks() / 1000
            r = int(self.w * 0.75 + math.sin(t * 6) * 4)
            pygame.draw.circle(surf, PURPLE,
                               (int(self.x + self.w // 2),
                                int(self.y + self.h // 2)), r, 3)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x + 10, self.y + 8, self.w - 14, self.h - 16)

    def draw_lives(self, surf: pygame.Surface, start_x: int, y: int):
        for i in range(MAX_LIVES):
            cx = start_x + i * (HEART_SIZE * 2 + HEART_SPACING)
            draw_heart(surf, cx, y, HEART_SIZE, i < self.lives)
