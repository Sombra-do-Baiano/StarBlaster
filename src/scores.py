"""
scores.py
Leitura e escrita do ranking de placares em JSON.

Estrutura do arquivo:
[
  {"name": "AAA", "score": 9999, "wave": 5},
  ...
]
"""

import json
import os
from config import SCORES_FILE, MAX_SCORES


def load_scores() -> list[dict]:
    """Carrega a lista de placares do arquivo JSON.
    Retorna lista vazia se o arquivo não existir ou estiver corrompido."""
    if not os.path.exists(SCORES_FILE):
        return []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # valida estrutura básica
        if isinstance(data, list):
            return data[:MAX_SCORES]
    except (json.JSONDecodeError, IOError):
        pass
    return []


def save_scores(scores: list[dict]) -> None:
    """Salva a lista de placares no arquivo JSON."""
    try:
        with open(SCORES_FILE, "w", encoding="utf-8") as f:
            json.dump(scores[:MAX_SCORES], f, ensure_ascii=False, indent=2)
    except IOError as e:
        print(f"[scores] Erro ao salvar: {e}")


def insert_score(scores: list[dict], name: str, score: int, wave: int) -> list[dict]:
    """Insere uma nova entrada e retorna a lista ordenada e truncada."""
    entry = {"name": name.strip() or "???", "score": score, "wave": wave}
    scores.append(entry)
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:MAX_SCORES]


def qualifies(scores: list[dict], score: int) -> bool:
    """Verifica se o placar entra no top MAX_SCORES."""
    if len(scores) < MAX_SCORES:
        return True
    return score > scores[-1]["score"]
