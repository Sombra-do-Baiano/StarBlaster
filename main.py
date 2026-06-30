"""
main.py
Entry point do STAR BLASTER.

SceneManager:
  Mantém a cena ativa e troca quando cena.next_scene != None.

Cenas registradas:
  "menu"       → MenuScene
  "game"       → GameScene
  "name_input" → NameInputScene
"""

import sys
import pygame

# ── Inicialização do pygame ANTES de importar módulos que usam fontes ─────────
pygame.init()
pygame.display.set_caption("STAR BLASTER  ★")

from config import W, H, FPS, init_fonts

screen = pygame.display.set_mode((W, H))
clock  = pygame.time.Clock()

init_fonts()   # inicializa o dict de fontes após pygame.init()

# imports das cenas após init para garantir que fontes existem
from scenes.menu       import MenuScene
from scenes.game       import GameScene
from scenes.name_input import NameInputScene


# ── SceneManager ──────────────────────────────────────────────────────────────

class SceneManager:
    """
    Gerencia a cena ativa e as transições entre cenas.
    Cada cena pode definir:
      self.next_scene  (str)  → nome da próxima cena
      self.context     (dict) → dados passados para a próxima cena (opcional)
    """

    def __init__(self):
        self.scene = MenuScene()

    def _build_scene(self, name: str, context: dict):
        """Instancia a cena pelo nome, injetando contexto quando necessário."""
        if name == "menu":
            return MenuScene()
        if name == "game":
            return GameScene()
        if name == "name_input":
            score = context.get("score", 0)
            wave  = context.get("wave",  1)
            return NameInputScene(score, wave)
        raise ValueError(f"Cena desconhecida: {name!r}")

    def run(self):
        while True:
            clock.tick(FPS)

            # ── Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.scene.handle_event(event)

            # ── Transição de cena
            if self.scene.next_scene:
                target  = self.scene.next_scene
                context = getattr(self.scene, "context", {})

                if target == "quit":
                    pygame.quit()
                    sys.exit()

                self.scene = self._build_scene(target, context)

            # ── Update & Draw
            self.scene.update()
            self.scene.draw(screen)
            pygame.display.flip()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    SceneManager().run()
