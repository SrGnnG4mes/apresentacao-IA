# -*- coding: utf-8 -*-
"""
Por que o A* precisa recalcular o custo g?

No bloco do A* tem um trecho que as outras buscas não têm: quando um
vizinho já é conhecido, ele ainda compara os custos e, se o caminho novo
for mais barato, reescreve o g e o pai daquela célula.

Parece desnecessário num labirinto onde todo passo custa igual — afinal,
a BFS não precisa disso. Mas precisa, e por um motivo específico: a BFS
expande na ordem da distância do início, então a primeira vez que ela
descobre uma célula já é pelo caminho mais curto. O A* expande na ordem
do f, não da distância — ele pode descobrir uma célula cedo por um desvio
comprido e só depois encontrar a rota curta até ela.

Este script mede o estrago: roda o A* normal e o A* sem o recálculo
(perguntando só "já conheço essa célula?", como a BFS faz) partindo de
todas as células livres, e compara os caminhos.

    python porque_recalcular.py
"""

from busca import busca
from estrutura_labirinto import CELL, LARGURA, ALTURA, INICIO, OBJETIVO, PAREDES, vizinhos


def caminho_de(inicio, recalcular):
    final = busca(inicio, OBJETIVO, vizinhos, "astar", recalcular=recalcular)[-1]
    return len(final["caminho"]) if final["encontrado"] else 0


def main():
    livres = [(x * CELL, y * CELL)
              for y in range(ALTURA) for x in range(LARGURA)
              if (x * CELL, y * CELL) not in PAREDES]

    print(f"Objetivo: {OBJETIVO}.  Partidas testadas: {len(livres)} células livres.\n")

    com = caminho_de(INICIO, True)
    sem = caminho_de(INICIO, False)
    print(f"Partindo do início oficial {INICIO}:")
    print(f"  A* como está no código ....... caminho de {com} células")
    print(f"  A* sem recalcular o g ........ caminho de {sem} células")
    print()

    piores = []
    for inicio in livres:
        n_com, n_sem = caminho_de(inicio, True), caminho_de(inicio, False)
        if n_sem != n_com:
            piores.append((inicio, n_com, n_sem))

    if not piores:
        print("Sem o recálculo o caminho não mudou em nenhuma partida.")
        return

    pior = max(piores, key=lambda item: item[2] - item[1])
    print(f"Sem o recálculo, o caminho fica mais longo em "
          f"{len(piores)} das {len(livres)} partidas.")
    print(f"Pior caso: partindo de {pior[0]}, o caminho vai de "
          f"{pior[1]} para {pior[2]} células (+{pior[2] - pior[1]}).\n")
    print("Ou seja: o recálculo não é detalhe de implementação. Sem ele o A*")
    print("guarda o pai errado e deixa de achar o caminho mínimo — mesmo aqui,")
    print("onde todos os passos custam a mesma coisa.")
    print()
    print("E é ele também que deixa o algoritmo pronto para custos diferentes")
    print("(lama custando 3, corredor custando 1): basta mudar custo_do_passo().")
    print("É aí que a BFS passa a responder a pergunta errada, porque 'menos")
    print("passos' deixa de significar 'mais barato'.")


if __name__ == "__main__":
    main()
