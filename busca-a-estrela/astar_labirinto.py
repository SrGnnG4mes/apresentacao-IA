"""
Comparacao BFS x A* no problema do labirinto.
Apresentacao - Algoritmos de Busca / Inteligencia Artificial

Rodar:  python3 astar_labirinto.py
Sem dependencias externas (so biblioteca padrao).
"""

import heapq
from collections import deque

# ---------------------------------------------------------------
# O LABIRINTO
# '#' = parede   '.' = livre   'S' = inicio   'G' = objetivo
# Para usar o labirinto de sala, basta trocar este bloco.
# ---------------------------------------------------------------
MAPA = """
###############################
#S#....#.#..#..#..............#
#...#.........#.###.#....#....#
##..#...#.###.........##....###
###.#..#...#....##..........#.#
#.#........#.#.##..####..#...##
#.........##.##..#.....##.....#
##.....#..#..#.##..###........#
#..#.##......#....#..#.#......#
#....###.#..#..###...#...#....#
#...#....#..##.........##.#...#
#.#...#..#.....##.#.#....#....#
###...#..###...............##.#
##..##..#..#......##.##...#...#
#....#...##......###.#.....####
###.....#...#...#.......#....G#
###############################
"""

# Coloque False se o terminal nao mostrar as cores direito
USAR_COR = True

VERDE  = "\033[42m  \033[0m"   # caminho final
AZUL   = "\033[46m  \033[0m"   # celulas exploradas
PAREDE = "\033[100m  \033[0m"  # parede
VAZIO  = "  "                  # nunca visitado
INICIO = "\033[43m S\033[0m"
FIM    = "\033[41m G\033[0m"


def carregar(mapa_txt):
    grade = mapa_txt.strip().split("\n")
    inicio = objetivo = None
    for y, linha in enumerate(grade):
        for x, c in enumerate(linha):
            if c == "S":
                inicio = (x, y)
            elif c == "G":
                objetivo = (x, y)
    return grade, inicio, objetivo


def vizinhos(pos, grade):
    """Movimento em 4 direcoes: cima, baixo, esquerda, direita."""
    x, y = pos
    for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grade) and 0 <= nx < len(grade[ny]):
            if grade[ny][nx] != "#":
                yield (nx, ny)


def reconstruir(veio_de, atual):
    caminho = [atual]
    while atual in veio_de:
        atual = veio_de[atual]
        caminho.append(atual)
    return caminho[::-1]


# ---------------------------------------------------------------
# BFS -- fila comum (FIFO). Nao usa heuristica nenhuma.
# ---------------------------------------------------------------
def bfs(grade, inicio, objetivo):
    fila = deque([inicio])
    veio_de = {}
    visitados = {inicio}
    expandidos = []

    while fila:
        atual = fila.popleft()           # <-- sempre o MAIS ANTIGO da fila
        expandidos.append(atual)

        if atual == objetivo:
            return reconstruir(veio_de, atual), expandidos

        for viz in vizinhos(atual, grade):
            if viz not in visitados:
                visitados.add(viz)
                veio_de[viz] = atual
                fila.append(viz)

    return None, expandidos


# ---------------------------------------------------------------
# A* -- fila de PRIORIDADE ordenada por  f = g + h
# ---------------------------------------------------------------
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_estrela(grade, inicio, objetivo, peso=1):
    """peso=1 -> heuristica admissivel  -> caminho OTIMO
       peso=3 -> heuristica superestima -> explora pouco, mas caminho PIOR"""

    h = lambda p: manhattan(p, objetivo) * peso

    contador = 0                              # desempate estavel na fila
    fila = [(h(inicio), contador, inicio)]    # tuplas (f, ordem, posicao)
    veio_de = {}
    melhor_g = {inicio: 0}                    # menor custo conhecido ate cada celula
    expandidos = []

    while fila:
        f, _, atual = heapq.heappop(fila)     # <-- sempre o MENOR f da fila
        expandidos.append(atual)

        if atual == objetivo:
            return reconstruir(veio_de, atual), expandidos

        for viz in vizinhos(atual, grade):
            novo_g = melhor_g[atual] + 1      # cada passo custa 1

            # so reabre a celula se achamos um caminho MAIS BARATO ate ela
            if viz not in melhor_g or novo_g < melhor_g[viz]:
                melhor_g[viz] = novo_g
                veio_de[viz] = atual
                contador += 1
                heapq.heappush(fila, (novo_g + h(viz), contador, viz))

    return None, expandidos


# ---------------------------------------------------------------
# DESENHO
# ---------------------------------------------------------------
def desenhar(grade, inicio, objetivo, caminho, expandidos, titulo):
    cam = set(caminho or [])
    exp = set(expandidos)

    print("\n" + titulo)
    for y, linha in enumerate(grade):
        saida = ""
        for x, c in enumerate(linha):
            p = (x, y)
            if p == inicio:
                saida += INICIO if USAR_COR else " S"
            elif p == objetivo:
                saida += FIM if USAR_COR else " G"
            elif c == "#":
                saida += PAREDE if USAR_COR else "##"
            elif p in cam:
                saida += VERDE if USAR_COR else " *"
            elif p in exp:
                saida += AZUL if USAR_COR else " ."
            else:
                saida += VAZIO
        print(saida)

    passos = len(caminho) - 1 if caminho else None
    print(f"  nos expandidos: {len(expandidos):>4}    "
          f"caminho: {passos if passos is not None else 'NAO ENCONTRADO'} passos")


def main():
    grade, inicio, objetivo = carregar(MAPA)
    if inicio is None or objetivo is None:
        print("ERRO: o mapa precisa ter um 'S' e um 'G'.")
        return

    print("\n" + "=" * 62)
    print("   BFS  x  A*   --   mesmo labirinto, mesmo objetivo")
    print("=" * 62)
    print("   azul = celulas exploradas     verde = caminho final")

    c1, e1 = bfs(grade, inicio, objetivo)
    desenhar(grade, inicio, objetivo, c1, e1,
             "[1] BUSCA EM LARGURA (BFS) -- sem heuristica")

    c2, e2 = a_estrela(grade, inicio, objetivo)
    desenhar(grade, inicio, objetivo, c2, e2,
             "[2] A* com Manhattan -- heuristica ADMISSIVEL")

    c3, e3 = a_estrela(grade, inicio, objetivo, peso=3)
    desenhar(grade, inicio, objetivo, c3, e3,
             "[3] A* com Manhattan x3 -- heuristica que SUPERESTIMA")

    if not (c1 and c2 and c3):
        print("\nAviso: nao existe caminho de S ate G neste mapa.")
        return

    print("\n" + "=" * 62)
    print("   RESUMO")
    print("=" * 62)
    print(f"   BFS ................ {len(e1):>4} nos expandidos | {len(c1)-1:>3} passos")
    print(f"   A* admissivel ...... {len(e2):>4} nos expandidos | {len(c2)-1:>3} passos")
    print(f"   A* com Manhattan x3  {len(e3):>4} nos expandidos | {len(c3)-1:>3} passos")

    reducao = 100 - len(e2) * 100 // len(e1)
    print()
    print(f"   -> O A* explorou {reducao}% menos celulas que a BFS")
    print(f"      e encontrou o MESMO caminho otimo de {len(c2)-1} passos.")
    if len(c3) > len(c2):
        print()
        print(f"   -> Ja a heuristica que superestima explorou pouco,")
        print(f"      mas devolveu um caminho {len(c3)-len(c2)} passos MAIS LONGO.")
        print(f"      Sem admissibilidade, o A* perde a garantia de otimalidade.")
    print()


if __name__ == "__main__":
    main()
