# -*- coding: utf-8 -*-
"""
Algoritmos de busca: aleatória, DFS, BFS e A*.

Tema do grupo: BUSCA A* (A ESTRELA). BFS e DFS estão aqui só para
comparação durante a apresentação — o A* é o bloco principal, lá embaixo.

Todos os algoritmos têm exatamente a mesma forma (um `while` que tira uma
célula da fronteira, expande os vizinhos dela e guarda uma "foto" do
estado no histórico). O que muda entre eles é a estrutura de dados usada
pra guardar a fronteira e, principalmente, QUAL célula é escolhida a cada
passo:

    aleatória -> lista comum + random.choice   (escolhe qualquer uma)
    DFS       -> pilha (LIFO)                  (a mais recente)
    BFS       -> fila (FIFO)                   (a mais antiga)
    A*        -> fila de prioridade            (a de menor f = g + h)

busca() roda o algoritmo inteiro e devolve uma lista de estados (um
dicionário por passo), na ordem em que aconteceram.

Rode "python busca.py" pra ver os quatro algoritmos resolvendo um
labirinto de exemplo no terminal, passo a passo.
"""

import heapq
import itertools
import random

# Nomes aceitos pelo parâmetro `algoritmo` de busca().
ALGORITMOS = ("aleatoria", "dfs", "bfs", "astar")


def novo_estado():
    """Um retrato do algoritmo em um instante da busca: só dados, sem lógica."""
    return {
        "visitados": set(),   # células já expandidas ("fechadas")
        "fronteira": set(),   # células conhecidas mas ainda não expandidas ("abertas")
        "pai": {},             # pai[celula] = célula anterior no caminho até ela
        "atual": None,         # célula sendo expandida neste passo
        "passos": 0,           # quantos nós já foram expandidos até agora
        "encontrado": False,   # True quando o objetivo foi alcançado
        "falhou": False,       # True quando a fronteira esvaziou sem achar o objetivo
        "caminho": [],         # caminho início -> objetivo, preenchido quando encontrado=True
    }


def _copia_do_estado(estado):
    """Tira uma 'foto' do estado atual, pra guardar no histórico sem que
    mudanças futuras no `estado` original afetem essa foto já tirada."""
    return {
        "visitados": set(estado["visitados"]),
        "fronteira": set(estado["fronteira"]),
        "atual": estado["atual"],
        "passos": estado["passos"],
        "encontrado": estado["encontrado"],
        "falhou": estado["falhou"],
        "caminho": list(estado["caminho"]),
    }


def _reconstruir_caminho(pai, objetivo):
    """Segue os "pais" de trás pra frente, do objetivo até o início."""
    caminho = []
    celula = objetivo
    while celula is not None:
        caminho.append(celula)
        celula = pai.get(celula)
    caminho.reverse()
    return caminho


# ---------------------------------------------------------------------------
# As duas funções que definem o A*: custo real (g) e estimativa (h)
# ---------------------------------------------------------------------------

def distancia_manhattan(a, b):
    """Distância "andando em L", só na horizontal e na vertical — que é
    exatamente como se anda neste labirinto (não há movimento diagonal).

    É a soma de quantos passos faltam em x mais quantos faltam em y,
    IGNORANDO as paredes. Por ignorar paredes, ela nunca superestima o
    caminho real: o caminho de verdade só pode ser igual ou mais longo.
    Uma heurística com essa propriedade se chama ADMISSÍVEL, e é ela que
    garante que o A* continue achando o caminho ótimo.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def custo_do_passo(a, b):
    """Quanto custa andar de `a` até `b` (células vizinhas).

    Usamos a própria distância percorrida como custo. Assim g (custo real
    acumulado) e h (estimativa) ficam na mesma unidade, sem depender do
    tamanho da célula: no labirinto gráfico cada passo custa 16 (CELL),
    no labirinto de texto cada passo custa 1.
    """
    return distancia_manhattan(a, b)


def heuristica(celula, objetivo):
    """h(n): o "chute" de quanto ainda falta de `celula` até o objetivo."""
    return distancia_manhattan(celula, objetivo)


def _expandir(estado, celula, objetivo, vizinhos, fronteira):
    """Passo comum às buscas aleatória / DFS / BFS:

    1. marca `celula` como visitada;
    2. se `celula` for o objetivo, monta o caminho e termina;
    3. senão, manda os vizinhos ainda não conhecidos pra fronteira.

    (o bloco do A*, lá embaixo, não usa esta função porque também precisa
    comparar custos entre caminhos, então ele é um pouquinho diferente.)
    """
    estado["fronteira"].discard(celula)
    estado["visitados"].add(celula)
    estado["atual"] = celula
    estado["passos"] += 1

    if celula == objetivo:
        estado["encontrado"] = True
        estado["caminho"] = _reconstruir_caminho(estado["pai"], objetivo)
        return

    for viz in vizinhos(celula):
        if viz in estado["visitados"] or viz in estado["fronteira"]:
            continue
        estado["pai"][viz] = celula
        estado["fronteira"].add(viz)
        fronteira.append(viz)


def busca(inicio, objetivo, vizinhos, algoritmo="astar", desempate=True,
          recalcular=True):
    """Roda a busca inteira e devolve o histórico: uma lista com um estado
    (dicionário) por passo, na ordem em que aconteceram.

    `algoritmo` escolhe a estratégia: "astar" (padrão), "bfs", "dfs" ou
    "aleatoria". No maze.py dá pra trocar pelas teclas 1/2/3/4.

    `desempate` só afeta o A*: com False, células com o mesmo f são
    expandidas na ordem em que entraram na fronteira (que é o que o
    pseudocódigo clássico faz, já que ele não especifica o desempate).
    Serve pra medir o efeito do desempate por -g; veja comparar.py.

    `recalcular` também só afeta o A*: com False, ele para de comparar
    custos e passa a perguntar só "já conheço essa célula?", como a BFS
    e a DFS fazem. Isso QUEBRA a otimalidade de propósito — existe só
    pra mostrar por que o recálculo é necessário; veja porque_recalcular.py.
    """
    if algoritmo not in ALGORITMOS:
        raise ValueError(f"algoritmo desconhecido: {algoritmo!r} (use um de {ALGORITMOS})")

    estado = novo_estado()
    estado["fronteira"].add(inicio)
    estado["pai"][inicio] = None
    historico = []

    if algoritmo == "astar":
        # -------------------------------------------------------------
        # BUSCA A* (A ESTRELA)  --  f(n) = g(n) + h(n)
        # -------------------------------------------------------------
        # A fronteira é uma FILA DE PRIORIDADE (heapq): a cada passo sai
        # dela a célula com o menor f, ou seja, a mais promissora.
        #
        #   g(n) = custo REAL do início até n (o que já foi gasto)
        #   h(n) = ESTIMATIVA de n até o objetivo (o que ainda falta)
        #   f(n) = g(n) + h(n) = estimativa do custo total do caminho
        #                        que passa por n
        #
        # É essa soma que diferencia o A* dos outros:
        #   - só g  -> Busca de Custo Uniforme / BFS (expande em círculos
        #              ao redor do início, sem saber pra onde ir);
        #   - só h  -> Busca Gulosa (corre pro objetivo, mas pode se
        #              enfiar num caminho ruim e não achar o mais curto);
        #   - g + h -> A*: puxa na direção do objetivo SEM esquecer o que
        #              já gastou, então continua achando o caminho ótimo.
        # Cada item do heap é a tupla (f, -g, ordem, celula), comparada
        # nessa ordem:
        #   f     -> quem tem menor custo total estimado sai primeiro;
        #   -g    -> DESEMPATE: entre dois f iguais, prefere quem já andou
        #            mais (g maior), porque esse está mais adiantado rumo
        #            ao objetivo. Sem esse desempate, num corredor aberto o
        #            A* empata com quase todo mundo e acaba varrendo o mapa
        #            como a BFS (o parâmetro desempate=False desliga isso,
        #            e o comparar.py mostra os dois números lado a lado);
        #   ordem -> só pra nunca precisar comparar tuplas de coordenadas.
        custo_g = {inicio: 0}          # menor custo real conhecido até cada célula
        contador = itertools.count()   # ordem de entrada, usada só como último desempate
        fronteira = [(heuristica(inicio, objetivo), 0, next(contador), inicio)]

        while fronteira:
            # tira da fronteira a célula de menor f = g + h
            _, _, _, celula = heapq.heappop(fronteira)

            # a mesma célula pode ter entrado no heap mais de uma vez (com
            # custos diferentes); se já foi expandida, essa entrada é velha
            if celula in estado["visitados"]:
                continue

            estado["fronteira"].discard(celula)
            estado["visitados"].add(celula)
            estado["atual"] = celula
            estado["passos"] += 1

            if celula == objetivo:
                estado["encontrado"] = True
                estado["caminho"] = _reconstruir_caminho(estado["pai"], objetivo)
                historico.append(_copia_do_estado(estado))
                return historico

            for viz in vizinhos(celula):
                if viz in estado["visitados"]:
                    continue
                novo_g = custo_g[celula] + custo_do_passo(celula, viz)
                # só aceita o vizinho se este caminho for melhor (mais
                # barato) do que o melhor caminho já conhecido até ele
                if viz in custo_g:
                    if not recalcular:
                        continue  # "já conheço": o jeito BFS/DFS, e errado aqui
                    if novo_g >= custo_g[viz]:
                        continue
                custo_g[viz] = novo_g
                estado["pai"][viz] = celula
                estado["fronteira"].add(viz)
                f = novo_g + heuristica(viz, objetivo)
                criterio_g = -novo_g if desempate else 0
                heapq.heappush(fronteira, (f, criterio_g, next(contador), viz))

            historico.append(_copia_do_estado(estado))

    else:
        # -------------------------------------------------------------
        # ALEATÓRIA / DFS / BFS  --  mesma estrutura, fronteira diferente
        # -------------------------------------------------------------
        fronteira = [inicio]

        if algoritmo == "aleatoria":
            # lista comum: sorteia uma célula qualquer. Sem estratégia,
            # serve de linha de base pra comparar com os outros.
            def retirar(f):
                celula = random.choice(f)
                f.remove(celula)
                return celula
        elif algoritmo == "dfs":
            # pilha (LIFO): sempre a célula mais recente -> "mergulha"
            def retirar(f):
                return f.pop()
        else:  # bfs
            # fila (FIFO): sempre a célula mais antiga -> avança em camadas
            def retirar(f):
                return f.pop(0)

        while fronteira:
            celula = retirar(fronteira)
            _expandir(estado, celula, objetivo, vizinhos, fronteira)
            historico.append(_copia_do_estado(estado))
            if estado["encontrado"]:
                return historico

    estado["falhou"] = True
    historico.append(_copia_do_estado(estado))
    return historico


if __name__ == "__main__":
    # Demonstração em modo texto, sem pygame: mostra os quatro algoritmos
    # resolvendo o mesmo labirinto pequeno e compara os números no fim.
    grade_exemplo = [
        "#########",
        "#S..#...#",
        "#.#.#.#.#",
        "#.#...#.#",
        "#.#####.#",
        "#.......#",
        "#.#####E#",
        "#########",
    ]

    paredes = set()
    inicio = objetivo = None
    for y, linha in enumerate(grade_exemplo):
        for x, c in enumerate(linha):
            if c == "#":
                paredes.add((x, y))
            elif c == "S":
                inicio = (x, y)
            elif c == "E":
                objetivo = (x, y)

    largura, altura = len(grade_exemplo[0]), len(grade_exemplo)

    def vizinhos_exemplo(celula):
        cx, cy = celula
        livres = []
        for nx, ny in ((cx, cy - 1), (cx, cy + 1), (cx - 1, cy), (cx + 1, cy)):
            if 0 <= nx < largura and 0 <= ny < altura and (nx, ny) not in paredes:
                livres.append((nx, ny))
        return livres

    print("Labirinto de exemplo (S=início, E=objetivo):")
    for linha in grade_exemplo:
        print(" ", linha)
    print()

    print("A* passo a passo (f = g + h):")
    historico = busca(inicio, objetivo, vizinhos_exemplo, "astar")
    for estado in historico:
        atual = estado["atual"]
        print(f"  passo {estado['passos']:2d}: atual={atual}  "
              f"h={heuristica(atual, objetivo):2d}  "
              f"fronteira={len(estado['fronteira']):2d}  "
              f"visitados={len(estado['visitados']):2d}")

    estado_final = historico[-1]
    if estado_final["encontrado"]:
        print(f"\n  Achou o objetivo em {estado_final['passos']} passos "
              f"(caminho com {len(estado_final['caminho'])} células).\n")
    else:
        print("\n  Não achou o objetivo.\n")

    print("Comparação no mesmo labirinto:")
    print(f"  {'algoritmo':<12} {'células expandidas':>19} {'tamanho do caminho':>20}")
    for nome in ALGORITMOS:
        h = busca(inicio, objetivo, vizinhos_exemplo, nome)[-1]
        caminho = len(h["caminho"]) if h["encontrado"] else 0
        print(f"  {nome:<12} {h['passos']:>19} {caminho:>20}")
