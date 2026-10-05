# -*- coding: utf-8 -*-
"""
Teste: o A* acha sempre o caminho mínimo?

A BFS, com todos os passos custando igual, é garantidamente ótima — então
ela serve de gabarito. Aqui rodamos as duas partindo de TODAS as células
livres do labirinto da aula e conferimos, uma por uma, se o A* achou um
caminho do mesmo tamanho. De quebra, medimos quantas células cada um
precisou expandir.

    python testes.py
"""

from busca import busca
from estrutura_labirinto import CELL, LARGURA, ALTURA, OBJETIVO, PAREDES, vizinhos


def main():
    livres = [(x * CELL, y * CELL)
              for y in range(ALTURA) for x in range(LARGURA)
              if (x * CELL, y * CELL) not in PAREDES]

    divergencias = []
    total_bfs = total_astar = 0
    astar_melhor = 0

    for inicio in livres:
        bfs = busca(inicio, OBJETIVO, vizinhos, "bfs")[-1]
        astar = busca(inicio, OBJETIVO, vizinhos, "astar")[-1]

        if len(bfs["caminho"]) != len(astar["caminho"]):
            divergencias.append((inicio, len(bfs["caminho"]), len(astar["caminho"])))

        total_bfs += bfs["passos"]
        total_astar += astar["passos"]
        if astar["passos"] < bfs["passos"]:
            astar_melhor += 1

    print(f"Testadas {len(livres)} células de partida, todas até o objetivo {OBJETIVO}.\n")

    if divergencias:
        print("FALHOU: o A* achou caminho diferente da BFS em:")
        for inicio, n_bfs, n_astar in divergencias:
            print(f"  {inicio}: BFS {n_bfs} x A* {n_astar}")
    else:
        print("OK: em TODAS as partidas o A* achou um caminho do mesmo")
        print("    tamanho que a BFS, ou seja, o caminho mínimo.\n")

    print(f"Células expandidas somando todas as partidas:")
    print(f"  BFS  : {total_bfs}")
    print(f"  A*   : {total_astar}  ({100.0 * (total_bfs - total_astar) / total_bfs:.0f}% a menos)")
    print(f"O A* expandiu menos que a BFS em {astar_melhor} das {len(livres)} partidas.")


if __name__ == "__main__":
    main()
