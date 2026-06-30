"""
scenes/game.py
Cena principal do jogo.

Estados internos: "playing" → "gameover" / "win"
Ao terminar, define next_scene:
  - "name_input" se o placar entrar no top 5
  - "menu" caso contrário
Passa score e wave via contexto.
"""

import pygame
import random
import math

from config import (
    W, H,
    CYAN, YELLOW, WHITE, ORANGE, GREEN, RED, GRAY, DKBLUE, PURPLE,
    BOSS_WAVE_INTERVAL, MAX_WAVES, fonts,
    SCORE_KILL_FIGHTER, SCORE_KILL_BOSS, SCORE_POWERUP,
    PARTICLES_SMALL, PARTICLES_MEDIUM, PARTICLES_LARGE, PARTICLES_HIT,
    SPAWN_RATE_INITIAL, SPAWN_RATE_MINIMUM, SPAWN_RATE_DECAY,
    ENEMIES_BASE, ENEMIES_PER_WAVE, POWERUP_DROP_CHANCE,
    HEART_SIZE,
)
from background import StarField
from entities import Player, Bullet, PowerUp, Particle, explode, POWERUP_TYPES
from enemies import EnemyFighter, EnemyUFO, Boss
from scores import load_scores, qualifies


class GameScene:
    def __init__(self):
        self.next_scene: str | None = None
        self.context: dict = {}          # dados passados ao próximo scene

        self.stars  = StarField()
        self.player = Player()

        self.p_bullets:  list[Bullet]   = []
        self.e_bullets:  list[Bullet]   = []
        self.enemies:    list           = []
        self.powerups:   list[PowerUp]  = []
        self.particles:  list[Particle] = []
        self.boss:       Boss | None    = None

        self.score = 0
        self.wave  = 1

        self.spawn_timer        = 0
        self.spawn_rate         = SPAWN_RATE_INITIAL
        self.enemies_per_wave   = ENEMIES_BASE
        self.enemies_killed     = 0
        self.wave_threshold     = ENEMIES_BASE

        self.state = "playing"   # playing / gameover / win
        self.end_timer = 0       # tempo na tela de fim antes de avançar

        # flash ao levar dano
        self._damage_flash = 0

    # ── Eventos ───────────────────────────────────────────────────────────────

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.next_scene = "quit"

        if event.type == pygame.KEYDOWN:
            if self.state in ("gameover", "win"):
                if event.key == pygame.K_RETURN:
                    self._finish()
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = "menu"
            else:
                if event.key == pygame.K_ESCAPE:
                    self.next_scene = "menu"

    # ── Update ────────────────────────────────────────────────────────────────

    def update(self):
        self.stars.update()

        if self.state in ("gameover", "win"):
            self.end_timer += 1
            # avança automaticamente após 4 segundos
            if self.end_timer >= 240:
                self._finish()
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        if keys[pygame.K_SPACE]:
            self.player.shoot(self.p_bullets)

        self._spawn_enemies()
        self._update_enemies()
        self._update_bullets()
        self._check_collisions()
        self._update_powerups()
        self._update_particles()
        self._check_wave_advance()

        if self._damage_flash > 0:
            self._damage_flash -= 1

        if not self.player.alive:
            self.state = "gameover"

    # ── Spawn ─────────────────────────────────────────────────────────────────

    def _spawn_enemies(self):
        if self.boss is not None:
            return
        self.spawn_timer -= 1
        if self.spawn_timer <= 0:
            self.spawn_timer = self.spawn_rate
            kind = random.choices(["fighter", "ufo"], weights=[70, 30])[0]
            self.enemies.append(EnemyFighter() if kind == "fighter" else EnemyUFO())

        # boss
        if (self.wave % BOSS_WAVE_INTERVAL == 0
                and not self.enemies
                and self.boss is None):
            self.boss = Boss()

    # ── Enemies ───────────────────────────────────────────────────────────────

    def _update_enemies(self):
        for e in self.enemies:
            e.update()
            e.try_shoot(self.e_bullets)
        self.enemies = [e for e in self.enemies if e.alive]

        if self.boss:
            self.boss.update()
            self.boss.try_shoot(self.e_bullets)
            if not self.boss.alive:
                explode(self.particles,
                        self.boss.x + self.boss.w // 2,
                        self.boss.y + self.boss.h // 2,
                        ORANGE, PARTICLES_LARGE)
                self.score += SCORE_KILL_BOSS
                self.boss = None
                self._advance_wave()
                if self.wave > MAX_WAVES:
                    self.state = "win"

    # ── Bullets ───────────────────────────────────────────────────────────────

    def _update_bullets(self):
        for b in self.p_bullets: b.update()
        for b in self.e_bullets: b.update()
        self.p_bullets = [b for b in self.p_bullets if b.alive]
        self.e_bullets = [b for b in self.e_bullets if b.alive]

    # ── Collisions ────────────────────────────────────────────────────────────

    def _check_collisions(self):
        # tiros do jogador vs inimigos
        for b in self.p_bullets:
            for e in self.enemies:
                if b.alive and b.rect().colliderect(e.rect()):
                    e.hp -= b.dmg
                    explode(self.particles, b.x, b.y, CYAN, PARTICLES_SMALL)
                    b.alive = False
                    if e.hp <= 0:
                        explode(self.particles,
                                e.rect().centerx, e.rect().centery, ORANGE, PARTICLES_MEDIUM)
                        self.score += e.score
                        self.enemies_killed += 1
                        if random.random() < POWERUP_DROP_CHANCE:
                            self.powerups.append(
                                PowerUp(e.rect().centerx, e.rect().centery,
                                        random.choice(POWERUP_TYPES)))
                        e.alive = False
                    break
            # boss
            if self.boss and b.alive and b.rect().colliderect(self.boss.rect()):
                self.boss.hp -= b.dmg
                explode(self.particles, b.x, b.y, YELLOW, 6)
                b.alive = False

        # tiros dos inimigos vs jogador
        for b in self.e_bullets:
            if b.rect().colliderect(self.player.rect()):
                if self.player.hit(b.dmg):
                    explode(self.particles,
                            self.player.x + self.player.w // 2,
                            self.player.y + self.player.h // 2,
                            CYAN, PARTICLES_HIT)
                    self._damage_flash = 12
                b.alive = False

        # inimigos colidem com jogador
        for e in self.enemies:
            if e.rect().colliderect(self.player.rect()):
                if self.player.hit(2):
                    explode(self.particles,
                            e.rect().centerx, e.rect().centery, RED, PARTICLES_MEDIUM)
                    self._damage_flash = 20
                e.alive = False

    # ── PowerUps ─────────────────────────────────────────────────────────────

    def _update_powerups(self):
        for p in self.powerups:
            p.update()
            if p.rect().colliderect(self.player.rect()):
                self.player.apply_power(p.kind)
                self.score += SCORE_POWERUP
                p.alive = False
        self.powerups = [p for p in self.powerups if p.alive]

    # ── Particles ────────────────────────────────────────────────────────────

    def _update_particles(self):
        for pt in self.particles: pt.update()
        self.particles = [pt for pt in self.particles if pt.life > 0]

    # ── Wave ─────────────────────────────────────────────────────────────────

    def _check_wave_advance(self):
        if (self.wave % BOSS_WAVE_INTERVAL != 0
                and self.enemies_killed >= self.wave_threshold):
            self._advance_wave()

    def _advance_wave(self):
        self.wave += 1
        self.enemies_killed   = 0
        self.spawn_rate       = max(SPAWN_RATE_MINIMUM,
                                    SPAWN_RATE_INITIAL - self.wave * SPAWN_RATE_DECAY)
        self.enemies_per_wave = ENEMIES_BASE + self.wave * ENEMIES_PER_WAVE
        self.wave_threshold   = self.enemies_per_wave

    # ── Fim de jogo ───────────────────────────────────────────────────────────

    def _finish(self):
        scores = load_scores()
        if qualifies(scores, self.score):
            self.context = {"score": self.score, "wave": self.wave}
            self.next_scene = "name_input"
        else:
            self.next_scene = "menu"

    # ── Draw ─────────────────────────────────────────────────────────────────

    def draw(self, surf: pygame.Surface):
        # flash de dano (vermelho semitransparente)
        surf.fill(DKBLUE)
        if self._damage_flash > 0:
            flash = pygame.Surface((W, H), pygame.SRCALPHA)
            alpha = int(self._damage_flash / 20 * 80)
            flash.fill((255, 0, 0, alpha))
            surf.blit(flash, (0, 0))

        self.stars.draw(surf)

        for pt in self.particles: pt.draw(surf)
        for p  in self.powerups:  p.draw(surf)
        for e  in self.enemies:   e.draw(surf)
        if self.boss:             self.boss.draw(surf)
        for b  in self.p_bullets: b.draw(surf)
        for b  in self.e_bullets: b.draw(surf)
        self.player.draw(surf)

        self._draw_hud(surf)

        if self.state == "gameover":
            self._draw_overlay_gameover(surf)
        elif self.state == "win":
            self._draw_overlay_win(surf)

    # ── HUD ──────────────────────────────────────────────────────────────────

    def _draw_hud(self, surf: pygame.Surface):
        # corações de vida
        self.player.draw_lives(surf, 16, 16 + HEART_SIZE)

        # power ativo
        if self.player.power != "normal":
            secs = self.player.power_timer // 60 + 1
            pwr  = fonts["sm"].render(
                f"PWR: {self.player.power.upper()}  {secs}s", True, YELLOW)
            surf.blit(pwr, (16, 52))

        # pontuação (centro)
        sc = fonts["med"].render(f"SCORE  {self.score:07d}", True, WHITE)
        surf.blit(sc, (W // 2 - sc.get_width() // 2, 10))

        # wave (direita)
        wv = fonts["sm"].render(f"WAVE {self.wave}", True, CYAN)
        surf.blit(wv, (W - wv.get_width() - 16, 10))

        if self.boss:
            bl = fonts["med"].render("★  BOSS  ★", True, RED)
            surf.blit(bl, (W // 2 - bl.get_width() // 2, H - 36))

    # ── Overlays de fim ──────────────────────────────────────────────────────

    def _draw_overlay_gameover(self, surf: pygame.Surface):
        self._draw_end_overlay(surf,
                               "GAME  OVER", RED,
                               f"Pontuação: {self.score:,}   Wave: {self.wave}")

    def _draw_overlay_win(self, surf: pygame.Surface):
        self._draw_end_overlay(surf,
                               "VITÓRIA!", YELLOW,
                               f"Pontuação Final: {self.score:,}")

    def _draw_end_overlay(self, surf: pygame.Surface,
                          title: str, title_color,
                          subtitle: str):
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surf.blit(overlay, (0, 0))

        t1 = fonts["big"].render(title, True, title_color)
        t2 = fonts["med"].render(subtitle, True, WHITE)
        t3 = fonts["sm"].render("ENTER = continuar    ESC = menu", True, GRAY)

        surf.blit(t1, (W // 2 - t1.get_width() // 2, H // 2 - 80))
        surf.blit(t2, (W // 2 - t2.get_width() // 2, H // 2))
        surf.blit(t3, (W // 2 - t3.get_width() // 2, H // 2 + 60))
