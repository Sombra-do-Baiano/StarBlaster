import os

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, r"assets")

def asset(path: str | None) -> str | None:
    """Retorna caminho absoluto dentro de assets/, ou None se path for None."""
    return os.path.join(ASSETS_DIR, path) if path else None

pathi = asset(r"sons\boss_sound.ogg")

print(os.path.exists(pathi))
print(os.path.isfile(pathi))
print(pathi)