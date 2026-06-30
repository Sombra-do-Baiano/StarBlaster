"""
config.py
Arquivo central de configuração do STAR BLASTER.

Tudo que afeta gameplay, visual e caminhos de assets fica aqui.
Os outros módulos importam daqui — nunca hardcodam valores.

Seções:
  1. Resolução e FPS
  2. Cores
  3. Caminhos de assets (sprites, background, estrelas, sons)
  4. Placar
  5. Jogo (regras gerais)
  6. Player
  7. Tiros do Player
  8. Inimigos — Fighter
  9. Inimigos — UFO
  10. Boss
  11. PowerUps
  12. Partículas
  13. Fontes
"""

import pygame
import os

# ═════════════════════════════════════════════════════════════════════════════
# 1. RESOLUÇÃO E FPS
# ═════════════════════════════════════════════════════════════════════════════

W, H       = 900, 600   # largura x altura da janela em pixels
FPS        = 60          # frames por segundo (afeta velocidade geral do jogo)
FULLSCREEN = False       # True = tela cheia

# ═════════════════════════════════════════════════════════════════════════════
# 2. CORES
# ═════════════════════════════════════════════════════════════════════════════

BLACK   = (0,   0,   0)
WHITE   = (255, 255, 255)
CYAN    = (0,   220, 255)
YELLOW  = (255, 220,   0)
RED     = (255,  50,  50)
GREEN   = (50,  255, 100)
ORANGE  = (255, 140,   0)
PURPLE  = (180,  80, 255)
GRAY    = (100, 100, 120)
DKBLUE  = (10,   10,  40)
DKRED   = (20,    0,   0)
DKGREEN = (0,   20,   0)

# ═════════════════════════════════════════════════════════════════════════════
# 3. CAMINHOS DE ASSETS
#    - Deixe o valor como None para usar o desenho procedural padrão.
#    - Coloque o arquivo dentro da pasta assets/ e ajuste o caminho.
#    - Sprites são carregados com pygame.image.load() e convertidos
#      para o tamanho definido nas seções de cada entidade.
# ═════════════════════════════════════════════════════════════════════════════

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def asset(path: str | None) -> str | None:
    """Retorna caminho absoluto dentro de assets/, ou None se path for None."""
    return os.path.join(ASSETS_DIR, path) if path else None

# ── Background ───────────────────────────────────────────────────────────────
# Imagem de fundo que aparece atrás das estrelas.
# None = apenas cor sólida DKBLUE.
BACKGROUND_IMAGE: str | None = asset(None)
# ex.: asset("bg_nebula.png")

# ── Estrelas ─────────────────────────────────────────────────────────────────
# Sprite usado para cada estrela do parallax. None = círculo procedural.
STAR_SPRITE: str | None = asset(None)
# ex.: asset("star.png")

STAR_COUNT       = 180    # quantidade de estrelas na tela
STAR_SPEED_MIN   = 0.3    # velocidade mínima (camada mais distante)
STAR_SPEED_MAX   = 2.5    # velocidade máxima (camada mais próxima)
STAR_SIZE_FACTOR = 0.6    # raio = speed * fator (só no modo procedural)

# ── Player sprite ────────────────────────────────────────────────────────────
# None = desenho procedural (polígono ciano).
PLAYER_SPRITE: str | None = asset(None)
# ex.: asset("ship_player.png")

# ── Inimigos — sprites ───────────────────────────────────────────────────────
ENEMY_FIGHTER_SPRITE: str | None = asset(None)
ENEMY_UFO_SPRITE:     str | None = asset(None)
BOSS_SPRITE:          str | None = asset(None)
# ex.: asset("enemy_fighter.png")

# ── PowerUps — sprites ───────────────────────────────────────────────────────
# Um sprite por tipo; None = círculo com letra.
POWERUP_SPRITES: dict[str, str | None] = {
    "rapid":   asset(None),
    "spread":  asset(None),
    "shield":  asset(None),
    "bigshot": asset(None),
}

# ── Sons ─────────────────────────────────────────────────────────────────────
# None = sem som para aquele evento.
SOUND_SHOOT:      str | None = asset(None)   # ex.: asset("sfx_shoot.wav")
SOUND_EXPLOSION:  str | None = asset(None)
SOUND_POWERUP:    str | None = asset(None)
SOUND_BOSS_ENTER: str | None = asset(None)
SOUND_MUSIC_MENU: str | None = asset(None)   # música de fundo do menu
SOUND_MUSIC_GAME: str | None = asset(None)   # música de fundo do jogo

# ── Placar ───────────────────────────────────────────────────────────────────
SCORES_FILE = os.path.join(BASE_DIR, "scores.json")

# ═════════════════════════════════════════════════════════════════════════════
# 4. PLACAR
# ═════════════════════════════════════════════════════════════════════════════

MAX_SCORES = 5   # quantos recordes são guardados no arquivo

# ═════════════════════════════════════════════════════════════════════════════
# 5. JOGO — REGRAS GERAIS
# ═════════════════════════════════════════════════════════════════════════════

MAX_LIVES          = 3   # vidas iniciais do jogador (corações)
BOSS_WAVE_INTERVAL = 3   # a cada N waves aparece um boss
MAX_WAVES          = 9   # número de waves até a vitória

# Pontuação
SCORE_KILL_FIGHTER = 100   # pontos por matar um fighter
SCORE_KILL_UFO     = 150   # pontos por matar um UFO
SCORE_KILL_BOSS    = 500   # pontos por matar o boss
SCORE_POWERUP      =  50   # pontos por coletar um powerup

# Dificuldade — spawn
SPAWN_RATE_INITIAL = 90    # frames entre spawns no wave 1
SPAWN_RATE_MINIMUM = 40    # limite mínimo de frames entre spawns
SPAWN_RATE_DECAY   =  8    # redução de frames por wave (spawn_rate - wave*decay)
ENEMIES_BASE       =  6    # inimigos para completar o wave 1
ENEMIES_PER_WAVE   =  2    # inimigos extras adicionados a cada wave

# Probabilidade de drop de powerup ao matar inimigo (0.0 – 1.0)
POWERUP_DROP_CHANCE = 0.25

# ═════════════════════════════════════════════════════════════════════════════
# 6. PLAYER
# ═════════════════════════════════════════════════════════════════════════════

PLAYER_W          = 70     # largura do sprite/hitbox do player em pixels
PLAYER_H          = 44     # altura
PLAYER_SPEED      =  5     # pixels por frame de movimento
PLAYER_START_X    = 80     # posição X inicial
PLAYER_INVINCIBLE_FRAMES = 90  # frames de invencibilidade após levar dano

# Limita o quanto o jogador pode avançar para a direita (fração da tela)
PLAYER_MAX_X_FRACTION = 0.5   # 0.5 = metade da tela

# ── Corações (vidas) ─────────────────────────────────────────────────────────
# Sprite usado para os corações de vida no HUD.
# None = coração desenhado via polígono matemático.
HEART_SPRITE_FULL:  str | None = asset(None)   # coração cheio  (vida disponível)
# ex.: asset("hud_heart_full.png")
HEART_SPRITE_EMPTY: str | None = asset(None)   # coração vazio  (vida perdida)
# ex.: asset("hud_heart_empty.png")

HEART_SIZE    = 14   # tamanho em pixels (raio no modo procedural; lado no modo sprite)
HEART_SPACING =  6   # espaço em pixels entre cada coração

# ── Tiro do player (modo normal) ─────────────────────────────────────────────
PLAYER_SHOOT_RATE_NORMAL  = 18   # frames entre tiros (normal)
PLAYER_SHOOT_RATE_RAPID   =  7   # frames entre tiros (power "rapid")
PLAYER_SHOOT_RATE_SPREAD  = 14   # frames entre tiros (power "spread")
PLAYER_SHOOT_RATE_BIGSHOT = 22   # frames entre tiros (power "bigshot")
PLAYER_POWER_DURATION     = 360  # frames que um power-up dura (~6 s a 60 fps)

# ═════════════════════════════════════════════════════════════════════════════
# 7. TIROS
# ═════════════════════════════════════════════════════════════════════════════

# Tiro normal / rapid (player)
BULLET_PLAYER_W    = 14    # largura em pixels
BULLET_PLAYER_H    =  5    # altura em pixels
BULLET_PLAYER_VX   = 14    # velocidade horizontal (px/frame)
BULLET_PLAYER_DMG  =  1    # dano por acerto
BULLET_PLAYER_COLOR = CYAN

# Tiro spread (player)
BULLET_SPREAD_W    = 12
BULLET_SPREAD_H    =  5
BULLET_SPREAD_VX   = 13    # módulo da velocidade (ângulo varia)
BULLET_SPREAD_ANGLES = (-12, 0, 12)   # ângulos em graus
BULLET_SPREAD_DMG  =  1
BULLET_SPREAD_COLOR = GREEN

# Tiro bigshot (player)
BULLET_BIG_W    = 22
BULLET_BIG_H    = 10
BULLET_BIG_VX   = 12
BULLET_BIG_DMG  =  3
BULLET_BIG_COLOR = YELLOW

# Tiro fighter (inimigo)
BULLET_FIGHTER_W    = 12
BULLET_FIGHTER_H    =  4
BULLET_FIGHTER_VX   = -6   # negativo = vai para a esquerda
BULLET_FIGHTER_DMG  =  1
BULLET_FIGHTER_COLOR = ORANGE

# Tiro UFO (inimigo, leque)
BULLET_UFO_W    = 10
BULLET_UFO_H    =  4
BULLET_UFO_SPEED =  5      # módulo da velocidade
BULLET_UFO_ANGLES = (0, 20, -20)   # desvio em graus a partir de 180°
BULLET_UFO_DMG  =  1
BULLET_UFO_COLOR = PURPLE

# Tiro boss (inimigo, anel)
BULLET_BOSS_W     = 12
BULLET_BOSS_H     =  5
BULLET_BOSS_SPEED =  5
BULLET_BOSS_STEP  = 30     # graus entre cada projétil do anel (360/step disparos)
BULLET_BOSS_DMG   =  2
BULLET_BOSS_COLOR = ORANGE

# ═════════════════════════════════════════════════════════════════════════════
# 8. INIMIGO — FIGHTER
# ═════════════════════════════════════════════════════════════════════════════

FIGHTER_W          = 50    # largura do sprite em pixels
FIGHTER_H          = 36    # altura
FIGHTER_HP         = 1    # HP inicial
FIGHTER_SPEED_MIN  = 2.5   # velocidade mínima horizontal (px/frame)
FIGHTER_SPEED_MAX  = 4.5   # velocidade máxima horizontal
FIGHTER_WAVE_AMP   = 40    # amplitude máxima do movimento senoidal vertical
FIGHTER_SHOOT_CD_MIN = 90  # cooldown mínimo de tiro (frames)
FIGHTER_SHOOT_CD_MAX = 180 # cooldown máximo de tiro
FIGHTER_SCORE      = SCORE_KILL_FIGHTER

# ═════════════════════════════════════════════════════════════════════════════
# 9. INIMIGO — UFO
# ═════════════════════════════════════════════════════════════════════════════

UFO_RADIUS         = 28    # raio do sprite em pixels
UFO_HP             = 1
UFO_SPEED_MIN      = 1.5
UFO_SPEED_MAX      = 3.0
UFO_SHOOT_CD_MIN   = 50
UFO_SHOOT_CD_MAX   = 100
UFO_SCORE          = SCORE_KILL_UFO

# ═════════════════════════════════════════════════════════════════════════════
# 10. BOSS
# ═════════════════════════════════════════════════════════════════════════════

BOSS_W             = 120   # largura do sprite em pixels
BOSS_H             = 100   # altura
BOSS_HP            = 50    # HP total
BOSS_ENTER_SPEED   = 3.6   # velocidade de entrada (px/frame)
BOSS_FIGHT_SPEED   = 1.8   # velocidade lateral durante o combate
BOSS_VERT_SPEED    = 1.5   # velocidade vertical de oscilação
BOSS_SHOOT_CD      = 35    # frames entre rajadas
BOSS_SCORE         = SCORE_KILL_BOSS

# Posição de parada do boss (fração da largura da tela, a partir da direita)
BOSS_STOP_X_FRACTION = (BOSS_W + 60) / W   # ~0.2 por padrão

# ═════════════════════════════════════════════════════════════════════════════
# 11. POWER-UPS
# ═════════════════════════════════════════════════════════════════════════════

POWERUP_RADIUS     = 14    # raio do círculo de coleta
POWERUP_SPEED      =  2    # velocidade de deslocamento para a esquerda
POWERUP_BOB_AMP    =  4    # amplitude da animação de flutuar (px)
POWERUP_BOB_FREQ   = 0.08  # frequência da animação (rad/frame)

# Cores dos power-ups (modo procedural)
POWERUP_COLORS = {
    "rapid":   CYAN,
    "spread":  GREEN,
    "shield":  PURPLE,
    "bigshot": YELLOW,
}
POWERUP_LABELS = {
    "rapid":   "R",
    "spread":  "S",
    "shield":  "★",
    "bigshot": "B",
}

# ═════════════════════════════════════════════════════════════════════════════
# 12. PARTÍCULAS
# ═════════════════════════════════════════════════════════════════════════════

PARTICLE_LIFE_MIN  = 15    # frames mínimos de vida
PARTICLE_LIFE_MAX  = 35    # frames máximos de vida
PARTICLE_VEL_MIN   = -3.0  # velocidade mínima em X e Y
PARTICLE_VEL_MAX   =  3.0
PARTICLE_SIZE_MIN  =  2.0  # tamanho mínimo inicial
PARTICLE_SIZE_MAX  =  5.0
PARTICLE_GRAVITY   = 0.05  # aceleração vertical por frame

# Quantidade de partículas por tipo de explosão
PARTICLES_SMALL    =  8    # impacto de tiro
PARTICLES_MEDIUM   = 20    # morte de inimigo
PARTICLES_LARGE    = 60    # morte do boss
PARTICLES_HIT      = 15    # player levando dano

# ═════════════════════════════════════════════════════════════════════════════
# 13. FONTES
# ═════════════════════════════════════════════════════════════════════════════

FONT_FAMILY = "consolas"   # família da fonte (SysFont)

FONT_SIZE_BIG  = 48
FONT_SIZE_MED  = 28
FONT_SIZE_SM   = 20
FONT_SIZE_TINY = 16

fonts: dict = {}

def init_fonts():
    """Inicializa o dicionário de fontes. Deve ser chamada após pygame.init()."""
    fonts["big"]  = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_BIG,  bold=True)
    fonts["med"]  = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_MED,  bold=True)
    fonts["sm"]   = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SM)
    fonts["tiny"] = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_TINY)
