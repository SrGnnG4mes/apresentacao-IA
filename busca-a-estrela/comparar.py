# -*- coding: utf-8 -*-
"""
Comparação dos algoritmos no labirinto da aula (sem pygame).

Roda os quatro algoritmos no MESMO labirinto e mostra:
  1. uma tabela com células expandidas x tamanho do caminho;
  2. o mapa do labirinto marcando o que cada algoritmo precisou visitar.

É o número que sustenta a frase da apresentação: "o A* acha o mesmo
caminho mínimo que a BFS, mas expandindo bem menos células".

    python comparar.py
"""

from busca import ALGORITMOS, busca
from estrutura_labirinto import CELL, LARGURA, ALTURA, INICIO, OBJETIVO, PAREDES, vizinhos

NOMES = {
    "aleatoria": "Aleatória",
    "dfs": "DFS (pilha)",
    "bfs": "BFS (fila)",
    "astar": "A* (fila de prioridade)",
}


def desenhar_mapa(estado, titulo):
    """Mapa em texto: # parede, . visitado, o fronteira, * caminho final."""
    visitados = estado["visitados"]
    fronteira = estado["fronteira"]
    caminho = set(estado["caminho"])

    print(titulo)
    for y in range(ALTURA):
        linha = []
        for x in range(LARGURA):
            celula = (x * CELL, y * CELL)
            if celula in PAREDES:
                linha.append("#")
            elif celula == INICIO:
                linha.append("S")
            elif celula == OBJETIVO:
                linha.append("E")
            elif celula in caminho:
                linha.append("*")
            elif celula in visitados:
                linha.append(".")
            elif celula in fronteira:
                linha.append("o")
            else:
                linha.append(" ")
        print("  " + "".join(linha))
    print()


def sala_aberta(lado=21):
    """Segundo cenário: uma sala quadrada vazia, só com as paredes da borda.

    Serve pra mostrar o A* no melhor caso: sem obstáculos, a distância de
    Manhattan é EXATA, então a heurística aponta direto pro objetivo e o
    A* praticamente anda em linha reta — enquanto a BFS precisa varrer a
    sala inteira em camadas, porque ela não faz ideia de onde o objetivo está.
    """
    paredes = set()
    for i in range(lado):
        paredes |= {(i, 0), (i, lado - 1), (0, i), (lado - 1, i)}

    def vizinhos_sala(celula):
        cx, cy = celula
        livres = []
        for nx, ny in ((cx, cy - 1), (cx, cy + 1), (cx - 1, cy), (cx + 1, cy)):
            if 0 <= nx < lado and 0 <= ny < lado and (nx, ny) not in paredes:
                livres.append((nx, ny))
        return livres

    inicio, objetivo = (1, 1), (lado - 2, lado - 2)
    livres = lado * lado - len(paredes)

    print(f"CENÁRIO 2: sala aberta {lado}x{lado} ({livres} células livres), "
          f"de um canto ao canto oposto\n")
    cab = f"{'algoritmo':<26}{'expandidas':>12}{'% da sala':>16}{'caminho':>10}"
    print(cab)
    print("-" * len(cab))
    for nome in ("bfs", "astar"):
        final = busca(inicio, objetivo, vizinhos_sala, nome)[-1]
        pct = 100.0 * final["passos"] / livres
        print(f"{NOMES[nome]:<26}{final['passos']:>12}{pct:>15.0f}%"
              f"{len(final['caminho']):>10}")
    sem = busca(inicio, objetivo, vizinhos_sala, "astar", desempate=False)[-1]
    pct = 100.0 * sem["passos"] / livres
    print(f"{'A* sem desempate por -g':<26}{sem['passos']:>12}{pct:>15.0f}%"
          f"{len(sem['caminho']):>10}")
    print("\nMesmo caminho mínimo, mas aqui a heurística é perfeita: o A* vai")
    print("quase direto ao objetivo e a BFS varre a sala toda.")
    print("E é aqui que o desempate aparece inteiro: sem ele, TODA célula de")
    print("um caminho mínimo empata no mesmo f, e o A* expande o platô todo.\n")


def main():
    total_livres = LARGURA * ALTURA - len(PAREDES)
    print("=" * 64)
    print("CENÁRIO 1: o labirinto da aula")
    print("=" * 64)
    print(f"Labirinto da aula: {LARGURA}x{ALTURA} células, {total_livres} livres.")
    print(f"Início {INICIO}  ->  Objetivo {OBJETIVO}   (cada passo custa {CELL})\n")

    resultados = {}
    for nome in ALGORITMOS:
        resultados[nome] = busca(INICIO, OBJETIVO, vizinhos, nome)[-1]

    cab = f"{'algoritmo':<26}{'expandidas':>12}{'% do labirinto':>16}{'caminho':>10}"
    print(cab)
    print("-" * len(cab))
    for nome in ALGORITMOS:
        final = resultados[nome]
        caminho = len(final["caminho"]) if final["encontrado"] else 0
        pct = 100.0 * final["passos"] / total_livres
        print(f"{NOMES[nome]:<26}{final['passos']:>12}{pct:>15.0f}%{caminho:>10}")

    # o mesmo A*, mas sem o desempate por -g: mostra que o desempate muda só
    # a ORDEM de expansão, nunca o tamanho do caminho
    sem_desempate = busca(INICIO, OBJETIVO, vizinhos, "astar", desempate=False)[-1]
    pct = 100.0 * sem_desempate["passos"] / total_livres
    print(f"{'A* sem desempate por -g':<26}{sem_desempate['passos']:>12}"
          f"{pct:>15.0f}%{len(sem_desempate['caminho']):>10}")
    print("\n(a linha da busca aleatória muda a cada execução: ela sorteia a")
    print(" célula; as outras três são determinísticas e repetem sempre)")
    print()

    bfs, astar = resultados["bfs"], resultados["astar"]
    print(f"BFS e A* acham o mesmo tamanho de caminho? "
          f"{'SIM' if len(bfs['caminho']) == len(astar['caminho']) else 'NÃO'} "
          f"(BFS {len(bfs['caminho'])} x A* {len(astar['caminho'])} células)")
    economia = 100.0 * (bfs["passos"] - astar["passos"]) / bfs["passos"]
    print(f"O A* expandiu {economia:.0f}% menos células que a BFS "
          f"({astar['passos']} contra {bfs['passos']}).\n")

    desenhar_mapa(bfs, "BFS  ( . = célula visitada,  * = caminho final )")
    desenhar_mapa(astar, "A*   ( . = célula visitada,  * = caminho final )")

    print("=" * 64)
    sala_aberta()


if __name__ == "__main__":
    main()
