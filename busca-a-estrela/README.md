# Busca A\* (A estrela) — labirinto

Trabalho de Inteligência Artificial: microapresentações sobre algoritmos de
busca. **Tema do grupo: A\* (A estrela).**

Base: [gustavocardial/algoritmos-de-busca](https://github.com/gustavocardial/algoritmos-de-busca)
(o labirinto da aula, onde só a busca aleatória vinha pronta). Aqui o **A\***
está implementado, e BFS/DFS entraram junto para servirem de comparação.

O roteiro da apresentação está em [APRESENTACAO.md](APRESENTACAO.md).

## Arquivos

| Arquivo | O que é |
|---|---|
| `busca.py` | Os algoritmos. O bloco do **A\*** é o principal — `f = g + h` |
| `estrutura_labirinto.py` | O mapa e a função `vizinhos()` (igual ao da aula) |
| `maze.py` | Visualização em pygame; teclas **1/2/3/4** trocam de algoritmo |
| `comparar.py` | Tabela A\* × BFS × DFS × aleatória, em dois cenários |
| `testes.py` | Confere se o A\* acha o caminho mínimo em 168 pontos de partida |
| `porque_recalcular.py` | Mostra o que quebra quando o A\* deixa de recalcular o `g` |

## Como rodar

Sem instalar nada além do Python (modo texto):

```bash
python busca.py
```

```bash
python comparar.py
```

```bash
python testes.py
```

```bash
python porque_recalcular.py
```

Visualização gráfica (precisa do pygame):

```bash
pip install pygame
```

```bash
python maze.py
```

Controles: **1** aleatória · **2** DFS · **3** BFS · **4** A\* · **R** reinicia ·
**+/-** velocidade · **ESC** sai.

## O A\* em uma frase

A fronteira é uma fila de prioridade ordenada por `f(n) = g(n) + h(n)`, onde `g`
é o custo real já percorrido e `h` é a distância de Manhattan até o objetivo.
Como `h` nunca superestima o custo restante (é *admissível*), o A\* acha o mesmo
caminho mínimo que a BFS, porém expandindo menos células.

## Resultados medidos

Labirinto da aula, do início até a saída:

| Algoritmo | Células expandidas | Caminho |
|---|---:|---:|
| Aleatória | ~160 (varia a cada execução) | 35–37 |
| DFS | 60 | 35 (não é o mínimo) |
| BFS | 161 | 33 |
| **A\*** | **136** | **33** |
| A\* sem o desempate por `-g` | 142 | 33 |

A linha da aleatória muda a cada execução, porque ela sorteia a célula; as
outras são determinísticas. O desempate por `-g` muda só a **ordem** de
expansão — o caminho continua sendo o mínimo (`busca(..., desempate=False)`
desliga, para comparar).

Sala aberta 21×21, de um canto ao outro: BFS expande as 361 células, o A\*
expande 37 — ambos com caminho de 37 células.

Partindo de todas as 168 células livres do labirinto: o A\* achou o caminho
mínimo em 168/168 casos, expandindo 37% menos células que a BFS no total.
