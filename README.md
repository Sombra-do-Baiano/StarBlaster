# Star Blaster

## Integrantes do grupo
- Eduardo Gomes Andrade 
- Gabriel Lucas Teles Vilaça
- João Vítor Vasconcelos de Souza
- Joaquim de Assis Santana 

## Estrutura do projeto

- `main.py`: ponto de entrada da aplicação.
- `src/`: código-fonte principal do jogo (loop, regras, sprites e dados).
- `assets/`: imagens, fontes e sons.
- `data/`: arquivos persistentes (recorde/ranking).
- `docs/`: documentação do projeto, incluindo proposta inicial.

## Descrição do jogo

Você pilota uma nave espacial e deve sobreviver a ondas crescentes de inimigos enquanto avança por waves cada vez mais difíceis. Colete power-ups para potencializar sua nave e enfrente bosses poderosos ao final de cada ciclo de waves.

## Objetivo do jogador

Sobreviver ao maior número de waves possível, eliminando inimigos e bosses para acumular a maior pontuação e entrar no ranking dos 5 melhores jogadores.

## Regras do jogo

- O jogador começa com 5 vidas representadas por corações no HUD
- Inimigos surgem continuamente da direita da tela em spawn progressivo
- Ao completar um ciclo de waves, um boss aparece antes de avançar para o próximo ciclo
- Inimigos eliminados têm chance de dropar power-ups coletáveis
- O jogador perde uma vida ao ser atingido por tiros inimigos ou duas ao colidir com uma nave inimiga
- O jogo encerra quando todas as vidas são perdidas ou ao completar a wave 9

## Controles

- Seta para cima: mover para cima
- Seta para baixo: mover para baixo
- Seta para esquerda: mover para esquerda
- Seta para direita: mover para direita
- Espaço: atira
- ESC: sair do jogo

## Como executar o projeto

### 1. Clonar o repositório

```bash
git clone LINK_DO_REPOSITORIO
cd NOME_DA_PASTA
pip install -r requirements.txt
python main.py
```
### 2. Opção 2 usar o .venv
Com o terminal aberto na pasta do projeto rode:

```bash
.\.venv\Scripts\Activate.ps1
python main.py
```

## Checklist mínimo para entrega

- Preencher este README com nome final, descrição real, regras e controles do jogo.
- Atualizar `docs/proposta.MD` com a proposta do grupo.
- Garantir que o jogo executa com `python main.py`.
