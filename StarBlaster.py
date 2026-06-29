import pygame
import random
import math
import sys

pygame.init()

# ── Config ──────────────────────────────────────────────────────────────────
W, H = 900, 600
FPS  = 60

BLACK  = (0,   0,   0)
WHITE  = (255, 255, 255)
CYAN   = (0,   220, 255)
YELLOW = (255, 220, 0)
RED    = (255,  50,  50)
GREEN  = (50,  255, 100)
ORANGE = (255, 140,  0)
PURPLE = (180,  80, 255)
GRAY   = (100, 100, 120)
DKBLUE = (10,  10,  40)

screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("STAR BLASTER  ★")
clock  = pygame.time.Clock()

font_big  = pygame.font.SysFont("consolas", 48, bold=True)
font_med  = pygame.font.SysFont("consolas", 28, bold=True)
font_sm   = pygame.font.SysFont("consolas", 20)

# ── Stars background ─────────────────────────────────────────────────────────
stars = [(random.randint(0, W), random.randint(0, H),
          random.uniform(0.3, 2.5)) for _ in range(180)]

def draw_stars():
    for x, y, spd in stars:
        brightness = int(spd / 2.5 * 200 + 55)
        pygame.draw.circle(screen, (brightness, brightness, brightness), (int(x), int(y)), max(1, int(spd * 0.6)))

def scroll_stars():
    global stars
    stars = [((x - spd * 1.5) % W, y, spd) for x, y, spd in stars]

# ── Draw helpers ─────────────────────────────────────────────────────────────
def draw_ship(surf, x, y, w, h, color, highlight):
    """Player ship polygon"""
    pts = [
        (x + w,     y + h//2),   # nose
        (x + w*0.3, y),           # top wing tip
        (x,         y + h//4),    # top fuselage
        (x,         y + h*3//4),  # bottom fuselage
        (x + w*0.3, y + h),       # bottom wing tip
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, highlight, pts, 2)
    # cockpit
    pygame.draw.ellipse(surf, highlight,
                        (x + w*0.45, y + h*0.35, w*0.3, h*0.3))

def draw_enemy_a(surf, x, y, w, h, color):
    """Angular enemy ship"""
    pts = [
        (x,         y + h//2),
        (x + w*0.3, y),
        (x + w,     y + h//4),
        (x + w,     y + h*3//4),
        (x + w*0.3, y + h),
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, RED, pts, 2)
    pygame.draw.circle(surf, ORANGE, (x + w*2//3, y + h//2), h//5)

def draw_enemy_b(surf, x, y, r, color):
    """Round UFO enemy"""
    pygame.draw.ellipse(surf, color, (x - r, y - r//2, r*2, r))
    pygame.draw.ellipse(surf, (color[0]//2, color[1]//2, color[2]//2),
                        (x - r//2, y - r*3//4, r, r//2))
    pygame.draw.ellipse(surf, RED, (x - r, y - r//2, r*2, r), 2)

def draw_boss(surf, x, y, w, h, color, hp_ratio):
    pts = [
        (x,         y + h//2),
        (x + w*0.2, y),
        (x + w*0.6, y + h*0.1),
        (x + w,     y + h//2),
        (x + w*0.6, y + h*0.9),
        (x + w*0.2, y + h),
    ]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.polygon(surf, ORANGE, pts, 3)
    # HP bar on boss
    bar_w = int(w * hp_ratio)
    pygame.draw.rect(surf, RED,   (x, y - 14, w, 8))
    pygame.draw.rect(surf, GREEN, (x, y - 14, bar_w, 8))
    # eye
    pygame.draw.circle(surf, YELLOW, (x + w*2//3, y + h//2), h//5)
    pygame.draw.circle(surf, RED,    (x + w*2//3, y + h//2), h//8)

# ── Particle ─────────────────────────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color, vx=None, vy=None, life=None, size=None):
        self.x, self.y = x, y
        self.color = color
        self.vx = vx if vx is not None else random.uniform(-3, 3)
        self.vy = vy if vy is not None else random.uniform(-3, 3)
        self.life = life or random.randint(15, 35)
        self.max_life = self.life
        self.size = size or random.uniform(2, 5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.05
        self.life -= 1

    def draw(self, surf):
        alpha = self.life / self.max_life
        r = int(self.color[0] * alpha)
        g = int(self.color[1] * alpha)
        b = int(self.color[2] * alpha)
        s = max(1, int(self.size * alpha))
        pygame.draw.circle(surf, (r, g, b), (int(self.x), int(self.y)), s)

def explode(particles, x, y, color, n=25):
    for _ in range(n):
        particles.append(Particle(x, y, color))

# ── Bullet ───────────────────────────────────────────────────────────────────
class Bullet:
    def __init__(self, x, y, vx, vy, color, dmg=1, w=14, h=5):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.dmg = dmg
        self.w, self.h = w, h
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        if self.x > W+20 or self.x < -20 or self.y < -20 or self.y > H+20:
            self.alive = False

    def draw(self, surf):
        glow = pygame.Surface((self.w+8, self.h+8), pygame.SRCALPHA)
        r,g,b = self.color
        pygame.draw.ellipse(glow, (r,g,b,60), (0,0,self.w+8,self.h+8))
        surf.blit(glow, (self.x - self.w//2 - 4, self.y - self.h//2 - 4))
        pygame.draw.ellipse(surf, self.color,
                            (self.x - self.w//2, self.y - self.h//2, self.w, self.h))

    def rect(self):
        return pygame.Rect(self.x - self.w//2, self.y - self.h//2, self.w, self.h)

# ── PowerUp ───────────────────────────────────────────────────────────────────
POWERUP_TYPES = ["rapid", "spread", "shield", "bigshot"]

class PowerUp:
    COLORS = {"rapid": CYAN, "spread": GREEN, "shield": PURPLE, "bigshot": YELLOW}
    LABELS = {"rapid": "R", "spread": "S", "shield": "★", "bigshot": "B"}

    def __init__(self, x, y, kind):
        self.x, self.y = x, y
        self.kind = kind
        self.alive = True
        self.r = 14
        self.t = 0

    def update(self):
        self.x -= 2
        self.t += 0.08
        if self.x < -30:
            self.alive = False

    def draw(self, surf):
        bob = math.sin(self.t) * 4
        c = self.COLORS[self.kind]
        pygame.draw.circle(surf, c, (int(self.x), int(self.y + bob)), self.r)
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y + bob)), self.r, 2)
        lbl = font_sm.render(self.LABELS[self.kind], True, BLACK)
        surf.blit(lbl, (self.x - lbl.get_width()//2, self.y + bob - lbl.get_height()//2))

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r, self.r*2, self.r*2)

# ── Enemy A (fighter) ─────────────────────────────────────────────────────────
class EnemyFighter:
    def __init__(self):
        self.w, self.h = 50, 36
        self.x = W + self.w
        self.y = random.randint(60, H - 60)
        self.spd = random.uniform(2.5, 4.5)
        self.hp = 2
        self.max_hp = 2
        self.alive = True
        self.shoot_cd = random.randint(60, 120)
        self.color = (random.randint(150,255), random.randint(30,80), random.randint(30,80))
        self.wave_amp = random.uniform(0, 40)
        self.wave_freq = random.uniform(0.03, 0.06)
        self.wave_phase = random.uniform(0, math.pi*2)
        self.t = 0

    def update(self):
        self.x -= self.spd
        self.t += 1
        self.y += math.sin(self.t * self.wave_freq + self.wave_phase) * self.wave_amp * 0.04
        self.y = max(40, min(H-40, self.y))
        self.shoot_cd -= 1
        if self.x < -self.w:
            self.alive = False

    def try_shoot(self, bullets):
        if self.shoot_cd <= 0:
            self.shoot_cd = random.randint(90, 180)
            bullets.append(Bullet(self.x, self.y + self.h//2,
                                  -6, 0, ORANGE, dmg=1, w=12, h=4))

    def draw(self, surf):
        draw_enemy_a(surf, self.x, self.y, self.w, self.h, self.color)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

# ── Enemy B (UFO) ─────────────────────────────────────────────────────────────
class EnemyUFO:
    def __init__(self):
        self.r = 28
        self.x = W + self.r
        self.y = random.randint(80, H - 80)
        self.spd = random.uniform(1.5, 3.0)
        self.hp = 5
        self.max_hp = 5
        self.alive = True
        self.shoot_cd = random.randint(40, 80)
        self.color = (random.randint(100,180), random.randint(30,80), random.randint(180,255))
        self.t = 0

    def update(self):
        self.x -= self.spd
        self.t += 1
        self.y += math.sin(self.t * 0.04) * 1.5
        self.y = max(60, min(H-60, self.y))
        self.shoot_cd -= 1
        if self.x < -self.r*2:
            self.alive = False

    def try_shoot(self, bullets):
        if self.shoot_cd <= 0:
            self.shoot_cd = random.randint(50, 100)
            for angle in [0, 20, -20]:
                rad = math.radians(180 + angle)
                bullets.append(Bullet(self.x - self.r, self.y,
                                      math.cos(rad)*5, math.sin(rad)*5,
                                      PURPLE, dmg=1, w=10, h=4))

    def draw(self, surf):
        draw_enemy_b(surf, int(self.x), int(self.y), self.r, self.color)

    def rect(self):
        return pygame.Rect(self.x - self.r, self.y - self.r//2, self.r*2, self.r)

# ── Boss ─────────────────────────────────────────────────────────────────────
class Boss:
    def __init__(self):
        self.w, self.h = 120, 100
        self.x = W + self.w
        self.y = H//2 - self.h//2
        self.spd = 1.8
        self.hp = 80
        self.max_hp = 80
        self.alive = True
        self.phase = "enter"   # enter -> fight -> dead
        self.shoot_cd = 60
        self.t = 0
        self.vy = 1.5

    def update(self):
        self.t += 1
        if self.phase == "enter":
            self.x -= self.spd * 2
            if self.x <= W - self.w - 60:
                self.phase = "fight"
        elif self.phase == "fight":
            self.x += math.sin(self.t * 0.02) * 1.2
            self.y += self.vy
            if self.y <= 30 or self.y >= H - self.h - 30:
                self.vy *= -1
            self.shoot_cd -= 1
        if self.hp <= 0:
            self.alive = False

    def try_shoot(self, bullets):
        if self.phase != "fight" or self.shoot_cd > 0:
            return
        self.shoot_cd = 35
        cx, cy = self.x, self.y + self.h//2
        for angle in range(180, 361, 30):
            rad = math.radians(angle)
            bullets.append(Bullet(cx, cy, math.cos(rad)*5, math.sin(rad)*5,
                                  ORANGE, dmg=2, w=12, h=5))

    def draw(self, surf):
        hp_ratio = self.hp / self.max_hp
        draw_boss(surf, int(self.x), int(self.y), self.w, self.h, RED, hp_ratio)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

# ── Player ───────────────────────────────────────────────────────────────────
class Player:
    def __init__(self):
        self.w, self.h = 70, 44
        self.x = 80
        self.y = H//2 - self.h//2
        self.spd = 5
        self.hp = 5
        self.max_hp = 5
        self.shoot_cd = 0
        self.shoot_rate = 18       # frames between shots
        self.power = "normal"       # normal / rapid / spread / bigshot
        self.power_timer = 0
        self.shield = False
        self.shield_timer = 0
        self.invincible = 0
        self.alive = True
        self.engine_t = 0

    def update(self, keys):
        dx = dy = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:    dy -= self.spd
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  dy += self.spd
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  dx -= self.spd
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: dx += self.spd
        self.x = max(0, min(W//2, self.x + dx))
        self.y = max(0, min(H - self.h, self.y + dy))

        if self.shoot_cd > 0:
            self.shoot_cd -= 1

        if self.power_timer > 0:
            self.power_timer -= 1
            if self.power_timer == 0:
                self.power = "normal"
                self.shoot_rate = 18
        if self.shield_timer > 0:
            self.shield_timer -= 1
            if self.shield_timer == 0:
                self.shield = False
        if self.invincible > 0:
            self.invincible -= 1
        self.engine_t += 1

    def shoot(self, bullets):
        if self.shoot_cd > 0:
            return
        self.shoot_cd = self.shoot_rate
        cx = self.x + self.w
        cy = self.y + self.h//2

        if self.power == "rapid" or self.power == "normal":
            bullets.append(Bullet(cx, cy, 14, 0, CYAN, dmg=1))
        if self.power == "spread":
            for angle in [-12, 0, 12]:
                rad = math.radians(angle)
                bullets.append(Bullet(cx, cy,
                                      math.cos(rad)*13, math.sin(rad)*13,
                                      GREEN, dmg=1))
        if self.power == "bigshot":
            bullets.append(Bullet(cx, cy, 12, 0, YELLOW, dmg=3, w=22, h=10))

    def apply_power(self, kind):
        if kind == "rapid":
            self.power = "rapid"
            self.shoot_rate = 7
            self.power_timer = 360
        elif kind == "spread":
            self.power = "spread"
            self.shoot_rate = 14
            self.power_timer = 360
        elif kind == "bigshot":
            self.power = "bigshot"
            self.shoot_rate = 22
            self.power_timer = 360
        elif kind == "shield":
            self.shield = True
            self.shield_timer = 360

    def hit(self, dmg=1):
        if self.invincible > 0:
            return False
        if self.shield:
            self.shield = False
            self.shield_timer = 0
            self.invincible = 40
            return False
        self.hp -= dmg
        self.invincible = 60
        if self.hp <= 0:
            self.alive = False
        return True

    def draw(self, surf):
        # engine flame
        flame_len = 18 + math.sin(self.engine_t * 0.3) * 8
        for i in range(3):
            fy = self.y + self.h//4 + i * (self.h//4)
            flen = flame_len * (1 - i * 0.2)
            pygame.draw.polygon(surf, ORANGE,
                [(self.x, fy),
                 (self.x - flen, fy - 5),
                 (self.x - flen, fy + 5)])

        # blink when invincible
        if self.invincible % 8 < 4:
            draw_ship(surf, self.x, self.y, self.w, self.h, CYAN, WHITE)

        # shield ring
        if self.shield:
            t = pygame.time.get_ticks() / 1000
            r = int(self.w*0.75 + math.sin(t*6)*4)
            pygame.draw.circle(surf, PURPLE,
                               (self.x + self.w//2, self.y + self.h//2), r, 3)

    def rect(self):
        return pygame.Rect(self.x + 10, self.y + 8, self.w - 14, self.h - 16)

# ── HUD ───────────────────────────────────────────────────────────────────────
def draw_hud(surf, player, score, wave, boss_active):
    # HP bar
    bar_w = 160
    pygame.draw.rect(surf, GRAY, (16, 16, bar_w, 16), border_radius=4)
    hp_w = int(bar_w * player.hp / player.max_hp)
    bar_color = GREEN if player.hp > 2 else RED
    pygame.draw.rect(surf, bar_color, (16, 16, hp_w, 16), border_radius=4)
    hp_lbl = font_sm.render(f"HP {player.hp}/{player.max_hp}", True, WHITE)
    surf.blit(hp_lbl, (16, 36))

    # power indicator
    if player.power != "normal":
        pwr = font_sm.render(f"PWR: {player.power.upper()}  {player.power_timer//60+1}s", True, YELLOW)
        surf.blit(pwr, (16, 58))

    # score
    sc = font_med.render(f"SCORE  {score:07d}", True, WHITE)
    surf.blit(sc, (W//2 - sc.get_width()//2, 10))

    # wave
    wv = font_sm.render(f"WAVE {wave}", True, CYAN)
    surf.blit(wv, (W - wv.get_width() - 16, 10))

    if boss_active:
        boss_lbl = font_med.render("★  BOSS  ★", True, RED)
        surf.blit(boss_lbl, (W//2 - boss_lbl.get_width()//2, H - 36))

# ── Screens ───────────────────────────────────────────────────────────────────
def draw_title():
    screen.fill(DKBLUE)
    draw_stars()
    t = font_big.render("STAR  BLASTER", True, CYAN)
    sub = font_med.render("WASD / Arrows = mover    SPACE = atirar", True, WHITE)
    start = font_med.render("Pressione  ENTER  para começar", True, YELLOW)
    screen.blit(t,     (W//2 - t.get_width()//2,     H//2 - 100))
    screen.blit(sub,   (W//2 - sub.get_width()//2,   H//2 - 20))
    screen.blit(start, (W//2 - start.get_width()//2, H//2 + 40))

def draw_gameover(score, wave):
    screen.fill((20, 0, 0))
    draw_stars()
    go   = font_big.render("GAME  OVER", True, RED)
    sc   = font_med.render(f"Pontuação: {score:07d}    Wave: {wave}", True, WHITE)
    rest = font_med.render("ENTER = reiniciar    ESC = sair", True, YELLOW)
    screen.blit(go,   (W//2 - go.get_width()//2,   H//2 - 80))
    screen.blit(sc,   (W//2 - sc.get_width()//2,   H//2))
    screen.blit(rest, (W//2 - rest.get_width()//2, H//2 + 60))

def draw_win(score):
    screen.fill((0, 20, 0))
    draw_stars()
    win  = font_big.render("VITÓRIA!", True, YELLOW)
    sc   = font_med.render(f"Pontuação Final: {score:07d}", True, WHITE)
    rest = font_med.render("ENTER = jogar de novo    ESC = sair", True, CYAN)
    screen.blit(win,  (W//2 - win.get_width()//2,  H//2 - 80))
    screen.blit(sc,   (W//2 - sc.get_width()//2,   H//2))
    screen.blit(rest, (W//2 - rest.get_width()//2, H//2 + 60))

# ── Main game loop ────────────────────────────────────────────────────────────
def run_game():
    player      = Player()
    p_bullets   = []   # player bullets
    e_bullets   = []   # enemy bullets
    enemies     = []
    powerups    = []
    particles   = []
    boss        = None

    score = 0
    wave  = 1
    spawn_timer = 0
    spawn_rate  = 90        # frames between spawns
    enemies_per_wave = 6
    enemies_killed  = 0
    boss_wave_interval = 3  # boss every 3 waves
    wave_threshold  = enemies_per_wave  # kills to advance wave

    screen_state = "play"  # play / gameover / win

    while True:
        dt = clock.tick(FPS)

        # ── Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if screen_state != "play":
                    if event.key == pygame.K_RETURN:
                        return "restart"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()

        if screen_state != "play":
            screen.fill(DKBLUE)
            if screen_state == "gameover":
                draw_gameover(score, wave)
            else:
                draw_win(score)
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit(); sys.exit()

        # ── Update
        scroll_stars()
        player.update(keys)
        if keys[pygame.K_SPACE]:
            player.shoot(p_bullets)

        # spawn enemies
        if boss is None:
            spawn_timer -= 1
            if spawn_timer <= 0:
                spawn_timer = spawn_rate
                kind = random.choices(["fighter","ufo"], weights=[70,30])[0]
                if kind == "fighter":
                    enemies.append(EnemyFighter())
                else:
                    enemies.append(EnemyUFO())

        # boss spawn
        if boss is None and wave % boss_wave_interval == 0 and not enemies:
            boss = Boss()

        # update enemies
        for e in enemies:
            e.update()
            e.try_shoot(e_bullets)
        enemies = [e for e in enemies if e.alive]

        # boss
        if boss:
            boss.update()
            boss.try_shoot(e_bullets)
            if not boss.alive:
                explode(particles, boss.x + boss.w//2, boss.y + boss.h//2, ORANGE, 60)
                score += 500
                boss = None
                wave += 1
                enemies_killed = 0
                spawn_rate = max(40, 90 - wave * 8)
                enemies_per_wave = 6 + wave * 2
                wave_threshold   = enemies_per_wave
                if wave > 9:
                    screen_state = "win"

        # update bullets
        for b in p_bullets: b.update()
        for b in e_bullets: b.update()
        p_bullets = [b for b in p_bullets if b.alive]
        e_bullets = [b for b in e_bullets if b.alive]

        # player bullets vs enemies
        for b in p_bullets:
            for e in enemies:
                if b.rect().colliderect(e.rect()):
                    e.hp -= b.dmg
                    explode(particles, b.x, b.y, CYAN, 8)
                    b.alive = False
                    if e.hp <= 0:
                        explode(particles, e.rect().centerx, e.rect().centery, ORANGE, 20)
                        score += 100
                        enemies_killed += 1
                        # maybe drop power-up
                        if random.random() < 0.25:
                            powerups.append(PowerUp(
                                e.rect().centerx, e.rect().centery,
                                random.choice(POWERUP_TYPES)))
                        e.alive = False
                    break
            # boss
            if boss and b.alive and b.rect().colliderect(boss.rect()):
                boss.hp -= b.dmg
                explode(particles, b.x, b.y, YELLOW, 6)
                b.alive = False

        # enemy bullets vs player
        for b in e_bullets:
            if b.rect().colliderect(player.rect()):
                if player.hit(b.dmg):
                    explode(particles, player.x + player.w//2,
                            player.y + player.h//2, CYAN, 15)
                b.alive = False

        # enemies collide player
        for e in enemies:
            if e.rect().colliderect(player.rect()):
                if player.hit(2):
                    explode(particles, e.rect().centerx, e.rect().centery, RED, 18)
                e.alive = False

        # powerups
        for p in powerups:
            p.update()
            if p.rect().colliderect(player.rect()):
                player.apply_power(p.kind)
                score += 50
                p.alive = False
        powerups = [p for p in powerups if p.alive]

        # particles
        for pt in particles: pt.update()
        particles = [pt for pt in particles if pt.life > 0]

        # wave advance (non-boss)
        if wave % boss_wave_interval != 0 and enemies_killed >= wave_threshold:
            wave += 1
            enemies_killed = 0
            spawn_rate   = max(40, 90 - wave * 8)
            enemies_per_wave = 6 + wave * 2
            wave_threshold   = enemies_per_wave

        if not player.alive:
            screen_state = "gameover"

        # ── Draw
        screen.fill(DKBLUE)
        draw_stars()

        for pt in particles: pt.draw(screen)
        for p in powerups:   p.draw(screen)

        for e in enemies:    e.draw(screen)
        if boss:             boss.draw(screen)

        for b in p_bullets:  b.draw(screen)
        for b in e_bullets:  b.draw(screen)

        player.draw(screen)
        draw_hud(screen, player, score, wave, boss is not None)

        pygame.display.flip()


# ── Entry point ───────────────────────────────────────────────────────────────
def main():
    # Title screen
    while True:
        screen.fill(DKBLUE)
        draw_stars()
        scroll_stars()
        draw_title()
        pygame.display.flip()
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    while run_game() == "restart":
                        pass
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

if __name__ == "__main__":
    main()