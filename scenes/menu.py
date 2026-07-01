"""
scenes/menu.py
Cena do Menu Principal.

Exibe:
  - Título animado
  - Top 5 placares lidos do arquivo
  - Botões: "Nova Partida" e "Sair"

Retorna para o SceneManager via self.next_scene.
"""

import pygame
import math
from src.config import W, H, CYAN, YELLOW, WHITE, GRAY, DKBLUE, GREEN, ORANGE, RED, fonts
from src.background import StarField
from src.scores import load_scores


# ── Botão simples ─────────────────────────────────────────────────────────────

class Button:
    def __init__(self, x, y, w, h, text: str, color, hover_color):
        self.rect  = pygame.Rect(x, y, w, h)
        self.text  = text
        self.color = color
        self.hover_color = hover_color
        self._hovered = False

    def update(self, mouse_pos):
        self._hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surf: pygame.Surface):
        color = self.hover_color if self._hovered else self.color
        pygame.draw.rect(surf, color, self.rect, border_radius=10)
        pygame.draw.rect(surf, WHITE, self.rect, 2, border_radius=10)
        lbl = fonts["med"].render(self.text, True, WHITE)
        surf.blit(lbl, (self.rect.centerx - lbl.get_width() // 2,
                        self.rect.centery - lbl.get_height() // 2))

    def clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


# ── Cena ──────────────────────────────────────────────────────────────────────

class MenuScene:
    def __init__(self):
        self.next_scene: str | None = None
        self.stars = StarField()
        self.t = 0

        btn_w, btn_h = 260, 52
        cx = W // 2

        self.btn_play = Button(cx - btn_w // 2, 390, btn_w, btn_h,
                               "Nova Partida", (30, 100, 180), (50, 150, 240))
        self.btn_quit = Button(cx - btn_w // 2, 460, btn_w, btn_h,
                               "Sair", (120, 30, 30), (200, 50, 50))

        self.scores = load_scores()

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.next_scene = "quit"

        if self.btn_play.clicked(event):
            self.next_scene = "game"

        if self.btn_quit.clicked(event):
            self.next_scene = "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_scene = "game"
            if event.key == pygame.K_ESCAPE:
                self.next_scene = "quit"

    def update(self):
        self.t += 1
        self.stars.update()
        mouse = pygame.mouse.get_pos()
        self.btn_play.update(mouse)
        self.btn_quit.update(mouse)

    def draw(self, surf: pygame.Surface):
        surf.fill(DKBLUE)
        self.stars.draw(surf)

        # ── Título ──────────────────────────────────────────────────────────
        bob = math.sin(self.t * 0.05) * 6
        title = fonts["big"].render("STAR  BLASTER", True, CYAN)
        star  = fonts["big"].render("★", True, YELLOW)
        tx = W // 2 - (title.get_width() + star.get_width() + 10) // 2
        ty = int(80 + bob)
        surf.blit(title, (tx, ty))
        surf.blit(star,  (tx + title.get_width() + 10, ty))

        sub = fonts["sm"].render("WASD / Setas = mover    ESPAÇO = atirar", True, GRAY)
        surf.blit(sub, (W // 2 - sub.get_width() // 2, 148))

        # ── Linha divisória ──────────────────────────────────────────────────
        pygame.draw.line(surf, GRAY, (W // 4, 175), (3 * W // 4, 175), 1)

        # ── TOP 5 ────────────────────────────────────────────────────────────
        top_lbl = fonts["med"].render("🏆  TOP  5", True, YELLOW)
        surf.blit(top_lbl, (W // 2 - top_lbl.get_width() // 2, 188))

        if self.scores:
            medal_colors = [YELLOW, GRAY, ORANGE, WHITE, WHITE]
            for i, entry in enumerate(self.scores[:5]):
                color = medal_colors[i]
                rank  = fonts["sm"].render(f"#{i+1}", True, color)
                name  = fonts["sm"].render(f"{entry['name'][:12]:<12}", True, WHITE)
                sc    = fonts["sm"].render(f"{entry['score']:>8}", True, GREEN)
                wave  = fonts["sm"].render(f"wave {entry['wave']}", True, GRAY)

                row_y = 228 + i * 28
                surf.blit(rank, (W // 2 - 220, row_y))
                surf.blit(name, (W // 2 - 175, row_y))
                surf.blit(sc,   (W // 2 + 20,  row_y))
                surf.blit(wave, (W // 2 + 130, row_y))
        else:
            empty = fonts["sm"].render("Nenhum placar ainda — seja o primeiro!", True, GRAY)
            surf.blit(empty, (W // 2 - empty.get_width() // 2, 240))

        # ── Botões ────────────────────────────────────────────────────────────
        self.btn_play.draw(surf)
        self.btn_quit.draw(surf)
