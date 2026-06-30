# Proposta Inicial do Jogo

## 1. Nome provisório do jogo
STAR BLASTER

## 2. Integrantes do grupo
- Nome 1: Joaquim de Assis Santana
- Nome 2: Gabriel Lucas Telles Vilaça
- Nome 3: João Vitor Vasconcelos de Souza
- Nome 4: Eduardo Gomes Andrade

## 3. Tipo de jogo
Shoot 'em up sidescroller espacial

## 4. Descrição geral do jogo
Você pilota uma nave espacial e deve sobreviver a ondas crescentes de inimigos enquanto avança por waves cada vez mais difíceis. Colete power-ups para potencializar sua nave e enfrente bosses poderosos ao final de cada ciclo de waves.

## 5. Objetivo do jogador
Sobreviver ao maior número de waves possível, eliminando inimigos e bosses para acumular a maior pontuação e entrar no ranking dos 5 melhores jogadores.

## 6. Regras principais
- O jogador começa com 5 vidas representadas por corações no HUD
- Inimigos surgem continuamente da direita da tela em spawn progressivo
- Ao completar um ciclo de waves, um boss aparece antes de avançar para o próximo ciclo
- Inimigos eliminados têm chance de dropar power-ups coletáveis
- O jogador perde uma vida ao ser atingido por tiros inimigos ou duas ao colidir com uma nave inimiga
- O jogo encerra quando todas as vidas são perdidas ou ao completar a wave 9

## 7. Condição de vitória
Completar todas as 9 waves, incluindo os 3 bosses que aparecem nas waves 3, 6 e 9.

## 8. Condição de derrota ou encerramento
O jogador perde quando todas as 5 vidas (corações) se esgotam. Caso a pontuação final entre no top 5 do ranking, o jogo solicita o nome do jogador antes de retornar ao menu.

## 9. Elementos previstos no jogo
- **Nave do jogador** com sistema de tiro e movimento em 4 direções
- **2 tipos de inimigos comuns:** Fighter (movimento senoidal, tiro reto) e UFO (movimento oscilatório, tiro em leque)
- **Boss** com padrão de tiro em anel e barra de HP visível
- **4 power-ups:** Rapid (cadência aumentada), Spread (tiro em 3 direções), Bigshot (projétil com 3x de dano) e Shield (absorve 1 hit)
- **Sistema de waves** com dificuldade crescente (spawn mais rápido e mais inimigos por wave)
- **Ranking local** com top 5 placares salvos em arquivo JSON
- **Sistema de cenas:** Menu Principal, Jogo e Entrada de Nome

## 10. Controles
- **WASD** ou **Setas direcionais** — movimentar a nave
- **Espaço (segurado)** — atirar continuamente
- **ESC** — voltar ao menu principal
- **Enter** — confirmar seleção nos menus

## 11. Organização do código
- `main.py` — inicializa o pygame e gerencia as transições entre cenas via `SceneManager`
- `config.py` — todas as configurações do jogo: resolução, FPS, tamanhos, velocidades, danos, caminhos de assets e cores
- `scores.py` — leitura e escrita do ranking em arquivo JSON (`scores.json`)
- `background.py` — campo de estrelas com parallax scrolling; suporta imagem de fundo e sprite de estrela configuráveis
- `draw_utils.py` — funções de desenho procedural das entidades (nave, inimigos, boss, corações)
- `entities.py` — classes `Player`, `Bullet`, `PowerUp` e `Particle`
- `enemies.py` — classes `EnemyFighter`, `EnemyUFO` e `Boss`
- `scenes/menu.py` — cena do menu principal com top 5 e botões clicáveis
- `scenes/game.py` — loop principal do jogo com spawn, colisões, HUD e overlays de fim
- `scenes/name_input.py` — cena de entrada de nome ao bater recorde

## 12. Recursos externos previstos
Todos os sprites, sons e fontes serão buscados em sites de assets gratuitos:
- https://www.freegameassets.com/
- https://itch.io/game-assets/free
- https://opengameart.org/

O jogo já funciona inteiramente com gráficos procedurais (desenhados via código), então assets externos são melhorias opcionais. Todos os caminhos são configuráveis em `config.py` — basta apontar o arquivo e o jogo troca o visual automaticamente.

## 13. Principais dificuldades esperadas
- Detecção de colisão entre múltiplos objetos simultâneos (tiros, inimigos, player)
- Organização modular do código em cenas independentes com transições limpas
- Balanceamento de dificuldade progressiva entre waves
- Implementação do sistema de ranking com leitura e escrita de arquivo
- Controle de cooldown e cadência de tiro para player e inimigos
- Uso do GitHub para controle de versão em grupo

## 14. Escopo mínimo para a entrega final
- Nave do jogador com movimentação e tiro funcionando
- Ao menos um tipo de inimigo com spawn e IA básica
- Sistema de vidas com corações no HUD
- Menu principal e tela de game over
- Ranking salvo em arquivo

## 15. Possíveis melhorias, caso haja tempo
- Sprites desenhados por artistas no lugar dos gráficos procedurais atuais
- Sons de tiro, explosão e música de fundo (infraestrutura já prevista em `config.py`)
- Mais tipos de inimigos e padrões de movimento
- Novos power-ups (ex.: recuperação de vida, tiro traseiro)
- Efeito de shake de câmera ao levar dano
- Animações de entrada e saída entre cenas