"""
enemies.py
Inimigos: EnemyFighter, EnemyUFO, Boss.
Todos os parâmetros vêm de config.py.
"""

import pygame
import random
import math
from src.config import (
    W, H,
    # fighter
    FIGHTER_W, FIGHTER_H, FIGHTER_HP,
    FIGHTER_SPEED_MIN, FIGHTER_SPEED_MAX,
    FIGHTER_WAVE_AMP,
    FIGHTER_SHOOT_CD_MIN, FIGHTER_SHOOT_CD_MAX,
    FIGHTER_SCORE,
    # UFO
    UFO_RADIUS, UFO_HP,
    UFO_SPEED_MIN, UFO_SPEED_MAX,
    UFO_SHOOT_CD_MIN, UFO_SHOOT_CD_MAX,
    UFO_SCORE,
    # boss
    BOSS_W, BOSS_H, BOSS_HP,
    BOSS_ENTER_SPEED, BOSS_FIGHT_SPEED, BOSS_VERT_SPEED,
    BOSS_SHOOT_CD, BOSS_SCORE, BOSS_STOP_X_FRACTION,
    # tiros inimigos
    BULLET_FIGHTER_W, BULLET_FIGHTER_H, BULLET_FIGHTER_VX,
    BULLET_FIGHTER_DMG, BULLET_FIGHTER_COLOR,
    BULLET_UFO_W, BULLET_UFO_H, BULLET_UFO_SPEED,
    BULLET_UFO_ANGLES, BULLET_UFO_DMG, BULLET_UFO_COLOR,
    BULLET_BOSS_W, BULLET_BOSS_H, BULLET_BOSS_SPEED,
    BULLET_BOSS_STEP, BULLET_BOSS_DMG, BULLET_BOSS_COLOR,
    RED,
)
from src.entities import Bullet
from src.draw_utils import draw_enemy_fighter, draw_enemy_ufo, draw_boss


# ── Fighter ───────────────────────────────────────────────────────────────────

class EnemyFighter:
    def __init__(self):
        self.w, self.h = FIGHTER_W, FIGHTER_H
        self.x = float(W + self.w)
        self.y = float(random.randint(60, H - 60))
        self.spd = random.uniform(FIGHTER_SPEED_MIN, FIGHTER_SPEED_MAX)
        self.hp  = FIGHTER_HP
        self.max_hp = FIGHTER_HP
        self.alive  = True
        self.score  = FIGHTER_SCORE
        self.shoot_cd   = random.randint(FIGHTER_SHOOT_CD_MIN, FIGHTER_SHOOT_CD_MAX)
        self.color = (
            random.randint(150, 255),
            random.randint(30,   80),
            random.randint(30,   80),
        )
        self.wave_amp   = random.uniform(0, FIGHTER_WAVE_AMP)
        self.wave_freq  = random.uniform(0.03, 0.06)
        self.wave_phase = random.uniform(0, math.pi * 2)
        self.t = 0

    def update(self):
        self.x -= self.spd
        self.t += 1
        self.y += math.sin(self.t * self.wave_freq + self.wave_phase) * self.wave_amp * 0.04
        self.y  = max(40.0, min(float(H - 40), self.y))
        self.shoot_cd -= 1
        if self.x < -self.w:
            self.alive = False

    def try_shoot(self, bullets: list):
        if self.shoot_cd <= 0:
            self.shoot_cd = random.randint(FIGHTER_SHOOT_CD_MIN, FIGHTER_SHOOT_CD_MAX)
            bullets.append(Bullet(
                self.x, self.y + self.h // 2,
                BULLET_FIGHTER_VX, 0,
                BULLET_FIGHTER_COLOR,
                dmg=BULLET_FIGHTER_DMG,
                w=BULLET_FIGHTER_W, h=BULLET_FIGHTER_H,
            ))

    def draw(self, surf: pygame.Surface):
        draw_enemy_fighter(surf, self.x, self.y, self.w, self.h, self.color)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)


# ── UFO ───────────────────────────────────────────────────────────────────────

class EnemyUFO:
    def __init__(self):
        self.r   = UFO_RADIUS
        self.x   = float(W + self.r)
        self.y   = float(random.randint(80, H - 80))
        self.spd = random.uniform(UFO_SPEED_MIN, UFO_SPEED_MAX)
        self.hp  = UFO_HP
        self.max_hp = UFO_HP
        self.alive  = True
        self.score  = UFO_SCORE
        self.shoot_cd = random.randint(UFO_SHOOT_CD_MIN, UFO_SHOOT_CD_MAX)
        self.color = (
            random.randint(100, 180),
            random.randint(30,   80),
            random.randint(180, 255),
        )
        self.t = 0

    def update(self):
        self.x -= self.spd
        self.t += 1
        self.y += math.sin(self.t * 0.04) * 1.5
        self.y  = max(60.0, min(float(H - 60), self.y))
        self.shoot_cd -= 1
        if self.x < -self.r * 2:
            self.alive = False

    def try_shoot(self, bullets: list):
        if self.shoot_cd <= 0:
            self.shoot_cd = random.randint(UFO_SHOOT_CD_MIN, UFO_SHOOT_CD_MAX)
            for angle in BULLET_UFO_ANGLES:
                rad = math.radians(180 + angle)
                bullets.append(Bullet(
                    self.x - self.r, self.y,
                    math.cos(rad) * BULLET_UFO_SPEED,
                    math.sin(rad) * BULLET_UFO_SPEED,
                    BULLET_UFO_COLOR,
                    dmg=BULLET_UFO_DMG,
                    w=BULLET_UFO_W, h=BULLET_UFO_H,
                ))

    def draw(self, surf: pygame.Surface):
        draw_enemy_ufo(surf, int(self.x), int(self.y), self.r, self.color)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - self.r, self.y - self.r // 2, self.r * 2, self.r)


# ── Boss ──────────────────────────────────────────────────────────────────────

class Boss:
    def __init__(self):
        self.w, self.h = BOSS_W, BOSS_H
        self.x  = float(W + self.w)
        self.y  = float(H // 2 - self.h // 2)
        self.hp = BOSS_HP
        self.max_hp = BOSS_HP
        self.alive  = True
        self.score  = BOSS_SCORE
        self.phase  = "enter"    # enter → fight → (dead)
        self.shoot_cd = BOSS_SHOOT_CD
        self.t  = 0
        self.vy = BOSS_VERT_SPEED
        self._stop_x = W * (1 - BOSS_STOP_X_FRACTION)

    def update(self):
        self.t += 1
        if self.phase == "enter":
            self.x -= BOSS_ENTER_SPEED
            if self.x <= self._stop_x:
                self.phase = "fight"
        elif self.phase == "fight":
            self.x += math.sin(self.t * 0.02) * BOSS_FIGHT_SPEED
            self.y += self.vy
            if self.y <= 30 or self.y >= H - self.h - 30:
                self.vy *= -1
            self.shoot_cd -= 1
        if self.hp <= 0:
            self.alive = False

    def try_shoot(self, bullets: list):
        if self.phase != "fight" or self.shoot_cd > 0:
            return
        self.shoot_cd = BOSS_SHOOT_CD
        cx = self.x
        cy = self.y + self.h // 2
        for angle in range(180, 361, BULLET_BOSS_STEP):
            rad = math.radians(angle)
            bullets.append(Bullet(
                cx, cy,
                math.cos(rad) * BULLET_BOSS_SPEED,
                math.sin(rad) * BULLET_BOSS_SPEED,
                BULLET_BOSS_COLOR,
                dmg=BULLET_BOSS_DMG,
                w=BULLET_BOSS_W, h=BULLET_BOSS_H,
            ))

    def draw(self, surf: pygame.Surface):
        draw_boss(surf, int(self.x), int(self.y), self.w, self.h, RED, self.hp / self.max_hp)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.w, self.h)
