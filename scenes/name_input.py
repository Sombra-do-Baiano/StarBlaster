"""
scenes/name_input.py
Cena de entrada de nome quando o jogador entra no Top 5.

Recebe 'score' e 'wave' via contexto do SceneManager.
Após confirmar, salva o placar e vai para o menu.
"""

import pygame
from src.config import W, H, CYAN, YELLOW, WHITE, GRAY, DKBLUE, GREEN, RED, fonts
from src.background import StarField
from src.scores import load_scores, insert_score, save_scores

MAX_NAME_LEN = 12


class NameInputScene:
    def __init__(self, score: int, wave: int):
        self.next_scene: str | None = None
        self.score = score
        self.wave  = wave
        self.name  = ""
        self.stars = StarField()
        self.t     = 0
        self.cursor_blink = 0
        self._saved = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self.next_scene = "quit"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.name.strip():
                self._save_and_proceed()
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.key == pygame.K_ESCAPE:
                # sai sem salvar
                self.next_scene = "menu"
            else:
                char = event.unicode
                if char.isprintable() and len(self.name) < MAX_NAME_LEN:
                    self.name += char

    def _save_and_proceed(self):
        if self._saved:
            return
        self._saved = True
        scores = load_scores()
        scores = insert_score(scores, self.name, self.score, self.wave)
        save_scores(scores)
        self.next_scene = "menu"

    def update(self):
        self.t += 1
        self.cursor_blink += 1
        self.stars.update()

    def draw(self, surf: pygame.Surface):
        surf.fill(DKBLUE)
        self.stars.draw(surf)

        # fundo semitransparente
        overlay = pygame.Surface((500, 280), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        surf.blit(overlay, (W // 2 - 250, H // 2 - 155))

        # título
        t1 = fonts["big"].render("NOVO RECORDE!", True, YELLOW)
        surf.blit(t1, (W // 2 - t1.get_width() // 2, H // 2 - 140))

        sc = fonts["med"].render(f"Pontuação: {self.score:,}   Wave: {self.wave}", True, GREEN)
        surf.blit(sc, (W // 2 - sc.get_width() // 2, H // 2 - 85))

        # instrução
        instr = fonts["sm"].render("Digite seu nome e pressione ENTER", True, GRAY)
        surf.blit(instr, (W // 2 - instr.get_width() // 2, H // 2 - 45))

        # caixa de texto
        box = pygame.Rect(W // 2 - 180, H // 2 - 5, 360, 46)
        pygame.draw.rect(surf, (20, 20, 60), box, border_radius=6)
        pygame.draw.rect(surf, CYAN, box, 2, border_radius=6)

        cursor = "_" if (self.cursor_blink // 30) % 2 == 0 else " "
        display_text = self.name + cursor
        name_surf = fonts["med"].render(display_text, True, WHITE)
        surf.blit(name_surf, (box.x + 12, box.y + 8))

        # dica ESC
        esc = fonts["tiny"].render("ESC = pular sem salvar", True, GRAY)
        surf.blit(esc, (W // 2 - esc.get_width() // 2, H // 2 + 60))
