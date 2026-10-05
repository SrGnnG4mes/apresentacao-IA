# Busca A* (A estrela) — roteiro da apresentação

**Trabalho:** Microapresentações sobre algoritmos de busca — 10 minutos.
**Integrantes:** Gabriel Nascimento Nogueira e Hugo Benjamim de Oliveira.

**Pergunta que a apresentação tem que responder:**
> Como o A\* combina o custo do caminho já percorrido com uma estimativa do
> custo restante, e por que isso pode torná-lo mais eficiente que a BFS?

**Resposta em três frases (é isso que o professor quer ouvir):**
1. O A\* dá uma nota `f(n) = g(n) + h(n)` para cada célula conhecida: `g` é o
   custo **real** já gasto do início até ela, `h` é uma **estimativa** do que
   ainda falta até o objetivo.
2. A cada passo ele expande a célula de **menor f**, ou seja, a que parece
   estar no melhor caminho completo — não a mais próxima do início (BFS) nem
   a que parece mais perto do objetivo (Gulosa).
3. Como `h` nunca superestima (é **admissível**), o A\* continua achando o
   caminho mínimo igual à BFS, mas **descarta antes** as regiões que não levam
   ao objetivo — por isso expande menos células.

---

## Os 10 minutos, bloco a bloco

| Tempo | Bloco | Slides | Quem | Seções aqui |
|---|---|---|---|---|
| 0:00 – 0:30 | Abertura e a pergunta do trabalho | 1–2 | Hugo | — |
| 0:30 – 2:30 | A fronteira e os três números: `g`, `h`, `f` | 3–4 | Hugo | 1 |
| 2:30 – 4:00 | Manhattan e `g+h` × só `g` × só `h` | 5–6 | Hugo | 2 |
| 4:00 – 5:30 | O código do A\* em `busca.py` | 7–8 | Gabriel | 3 |
| 5:30 – 8:00 | Demo ao vivo, mapas e números | 9–12 | Gabriel | 4 e 5 |
| 8:00 – 9:30 | Vantagem, limitação e aplicações | 13–14 | Gabriel | 6 e 7 |
| 9:30 – 10:00 | Fecho e perguntas | 15 | os dois | 8 e colinha |

**A troca é no slide 7**, quando sai o conceito e entra o código — Gabriel
escreveu a implementação, então é natural que ele assuma daí em diante.
Combinem uma frase de passagem ("e é assim que isso vira código — Gabriel")
para não ficar aquele silêncio de troca de teclado.

**Nas perguntas, os dois respondem.** Divisão que funciona: Hugo pega o que
for conceito (por que `h` não pode superestimar, diferença para a gulosa,
`h = 0`), Gabriel pega o que for implementação (o desempate por `-g`, o
recálculo do `g`, os números). Mas **os dois precisam saber tudo** — o
professor pode perguntar a qualquer um, e a seção 8 aqui tem as respostas.

**Risco de tempo:** o bloco da demo é o que mais escapa. Deixem a janela do
`maze.py` **já aberta** antes de começar e, se estiverem atrasados, cortem a
busca aleatória e a DFS — mostrem só BFS (tecla 3) e A\* (tecla 4).

---

## 1. A ideia: três números por célula

Todo algoritmo de busca mantém uma **fronteira** (células conhecidas mas ainda
não expandidas) e, a cada passo, escolhe uma para expandir. A única diferença
entre os algoritmos é **quem ele escolhe**:

| Algoritmo | Escolhe... | Fronteira é... |
|---|---|---|
| Aleatória | qualquer uma | uma lista |
| DFS | a mais recente | pilha (LIFO) |
| BFS | a mais antiga | fila (FIFO) |
| Gulosa | a de menor `h` | fila de prioridade |
| **A\*** | **a de menor `f = g + h`** | **fila de prioridade** |

- `g(n)` — **custo real** do início até `n`. É o que já foi gasto, é um fato.
- `h(n)` — **heurística**: estimativa do custo de `n` até o objetivo. É um
  palpite, calculado sem executar busca nenhuma.
- `f(n) = g(n) + h(n)` — estimativa do **custo total do caminho que passa por `n`**.

No nosso labirinto `h` é a **distância de Manhattan** (`|Δx| + |Δy|`): quantos
passos faltariam se não houvesse parede nenhuma. Como ignorar paredes só pode
deixar o caminho mais curto, ela **nunca superestima** o custo real — é o que
se chama heurística **admissível**, e é exatamente essa propriedade que garante
que o A\* ainda ache o caminho ótimo.

## 2. Por que `g + h` e não só um dos dois

```
        só g (BFS)              só h (Gulosa)             g + h (A*)

    . . o o o . . . .       . . . . . . . . .       . . . . . . . . .
    . o o o o o . . .       . . S > > > > . .       . . S > > > . . .
    o o o S o o o . .       . . . . . . v . .       . . . . o o v . .
    . o o o o o . . .       . . . . . . v . .       . . . . . o v . .
    . . o o o . . . E       . . . . . . > > E       . . . . . . > > E

    cresce igual para       vai direto na direção   vai na direção do
    todos os lados: acha    do objetivo: rápida,    objetivo SEM esquecer
    o mínimo, mas olha      mas o caminho pode      o custo já gasto: acha
    para o mapa inteiro     não ser o mínimo        o mínimo olhando menos
```

- **Só `g`** (BFS com custo uniforme): o algoritmo é ótimo, mas **cego** — não
  tem nenhuma informação sobre onde o objetivo está, então cresce igualmente
  em todas as direções.
- **Só `h`** (Gulosa): é rápida, mas **não é ótima** — ela ignora o que já
  gastou, então aceita um caminho longo só porque o próximo passo parece perto
  do objetivo.
- **`g + h`** (A\*): junta as duas informações. O `h` dá a direção (eficiência),
  o `g` mantém a contabilidade honesta (otimalidade).

**A frase-chave:** *a BFS pergunta "o que está mais perto de onde eu comecei?";
a Gulosa pergunta "o que parece mais perto de onde eu quero chegar?"; o A\*
pergunta "qual caminho inteiro parece mais barato?"*.

## 3. O código (`busca.py`, bloco `if algoritmo == "astar"`)

Três pedaços para mostrar na tela:

**(a) A fronteira é uma fila de prioridade.** Cada item é a tupla
`(f, -g, ordem, celula)` e o `heapq` sempre devolve o menor:

```python
fronteira = [(heuristica(inicio, objetivo), 0, next(contador), inicio)]
...
_, _, _, celula = heapq.heappop(fronteira)   # a célula de menor f = g + h
```

O `-g` é um **desempate**: entre dois `f` iguais, prefere quem já andou mais
(está mais adiantado). Sem ele, num corredor aberto quase todo mundo empata e
o A\* acaba varrendo o mapa como a BFS — na sala aberta de `comparar.py` são
**37 células com o desempate contra 361 sem ele**.

O pseudocódigo clássico **não especifica** o desempate, e qualquer critério
continua correto — o `-g` muda só a ordem de expansão, nunca o tamanho do
caminho. Se perguntarem, o `comparar.py` imprime as duas linhas lado a lado
(é o parâmetro `busca(..., desempate=False)`), então dá para provar o número
rodando na hora em vez de citar de memória.

**(b) O `g` é recalculado quando se acha um caminho melhor** — é isso que o
`_expandir()` das outras buscas não faz:

```python
novo_g = custo_g[celula] + custo_do_passo(celula, viz)
if viz in custo_g and novo_g >= custo_g[viz]:
    continue          # já conhecíamos um caminho igual ou melhor até `viz`
custo_g[viz] = novo_g
estado["pai"][viz] = celula
heapq.heappush(fronteira, (novo_g + heuristica(viz, objetivo), -novo_g, next(contador), viz))
```

**(c) A heurística**, que é a única parte "inteligente" do algoritmo:

```python
def distancia_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
```

> Detalhe que dá para citar: como a mesma célula pode entrar no heap mais de
> uma vez (com custos diferentes), ao tirar uma célula já visitada o código
> simplesmente ignora aquela entrada velha (`if celula in estado["visitados"]: continue`).

## 4. Demonstração ao vivo

```bash
python maze.py
```

Com a janela aberta: **tecla 3 = BFS**, **tecla 4 = A\***, `R` reinicia,
`+`/`-` muda a velocidade.

O que apontar na tela:
- **azul escuro** = já visitado, **amarelo** = fronteira, **verde** = caminho final;
- na **BFS** a mancha azul cresce como uma onda circular em volta do início;
- no **A\*** a mancha "estica" na direção do objetivo e deixa cantos do mapa
  intocados — o painel de baixo mostra `Passos` e `Visitados` para comparar;
- no fim, **o caminho verde tem o mesmo tamanho nos dois** (33 células).

Depois, os números no terminal:

```bash
python comparar.py    # tabela + mapas em texto dos dois cenários
python testes.py      # confere a otimalidade do A* em 168 pontos de partida
```

## 5. Os números (reais, medidos com `comparar.py` e `testes.py`)

**Labirinto da aula** (20×15, 168 células livres), do início até a saída:

| Algoritmo | Células expandidas | Tamanho do caminho |
|---|---:|---:|
| Aleatória | 159 | 35 |
| DFS | 60 | **35 (não é o mínimo)** |
| BFS | 161 | 33 |
| **A\*** | **136** | **33** |

**Sala aberta 21×21** (sem obstáculos), de um canto ao canto oposto:

| Algoritmo | Células expandidas | Tamanho do caminho |
|---|---:|---:|
| BFS | 361 (100% da sala) | 37 |
| **A\*** | **37 (10% da sala)** | 37 |

**Teste de otimalidade** (`testes.py`, partindo de todas as 168 células livres):
o A\* achou um caminho do mesmo tamanho que a BFS em **168 de 168** casos, e
expandiu no total **13.077 células contra 20.708 da BFS — 37% a menos**.

Leitura desses números (importante dizer, é o que mostra domínio do tema):
> O ganho do A\* **depende de quanto a heurística informa**. Na sala aberta a
> distância de Manhattan é exata e o A\* vai quase direto (10× menos células).
> No labirinto da aula, cheio de paredes e desvios, ela subestima bastante
> (chuta 20 passos onde o caminho real tem 32), então o A\* se aproxima da BFS
> — mas mesmo ali ainda expande 16% menos, e nunca perde a otimalidade.

## 6. Vantagem e limitação

**Vantagem:** encontra o caminho **ótimo** (como a BFS), mas guiado — expande
menos nós, porque a heurística deixa ele descartar cedo as regiões que só podem
levar a caminhos caros. É o melhor dos dois mundos: a garantia da BFS com a
direção da Gulosa. Tecnicamente: com heurística admissível o A\* é **ótimo**, e
é **otimamente eficiente** (nenhum outro algoritmo com a mesma heurística
expande menos nós e garante o ótimo).

**Limitação:** ele guarda **todos** os nós conhecidos na memória (fronteira +
visitados + os custos `g`), então em problemas grandes o gargalo é a **memória**,
não o tempo — o mesmo problema da BFS. E a eficiência **depende inteiramente
da qualidade da heurística**: com `h = 0` ele vira Busca de Custo Uniforme; com
uma `h` que superestima, ele fica rápido mas **perde a garantia do caminho
mínimo**. Além disso, precisa existir uma heurística que faça sentido para o
problema — em um problema sem noção de "distância até o objetivo", não há o que
estimar.

## 7. Aplicações

- **GPS e rotas** (Waze, Google Maps): `g` = distância/tempo já percorrido,
  `h` = distância em linha reta até o destino. É o exemplo clássico e o mais
  fácil de todos entenderem.
- **Jogos**: movimentação de NPCs e unidades em mapas de tiles — é o uso mais
  comum do A\* na prática, e é literalmente o nosso labirinto.
- **Robótica**: planejamento de trajetória de um robô móvel em um mapa de
  ocupação (com variantes como D\* para mapas que mudam).
- **Quebra-cabeças**: 8-puzzle / 15-puzzle, com `h` = número de peças fora do
  lugar ou soma das distâncias de Manhattan de cada peça.

## 8. Perguntas que podem cair (e as respostas)

**"Por que a heurística não pode superestimar?"**
Se `h` chuta a mais, o A\* pode achar que o caminho bom é caro e fechar o
objetivo por um caminho pior antes de olhar o certo — perde a otimalidade.
Enquanto `h` nunca passa do custo real, isso não acontece.

**"E se `h = 0` para todas as células?"**
Vira Busca de Custo Uniforme (e, como aqui todo passo custa igual, praticamente
a BFS). Ou seja: BFS/Custo Uniforme é um caso particular do A\*.

**"O A\* é sempre melhor que a BFS?"**
Em nós expandidos, com uma heurística boa, sim. Mas ele gasta mais por nó
(calcular `h`, manter a fila de prioridade) e a mesma memória; com uma
heurística fraca o ganho some, como acontece no nosso labirinto (16%).

**"Qual a diferença para a Busca Gulosa?"**
A Gulosa usa só `h` e ignora `g` — é mais rápida, mas o caminho que ela acha
pode não ser o mínimo. O A\* soma os dois e por isso mantém a garantia.

**"Por que vocês usaram Manhattan e não distância em linha reta (euclidiana)?"**
Porque no labirinto só se anda em 4 direções (sem diagonal). A euclidiana
também seria admissível, mas subestima mais ainda (chuta menos que o real),
então informaria menos e o A\* expandiria mais células.

**"O que acontece se não houver caminho até o objetivo?"**
A fronteira esvazia, o `while` termina e o estado é marcado com
`falhou = True` — a tela mostra "Sem caminho até o objetivo!".

---

## Colinha de 30 segundos

> O A\* é uma busca informada. Para cada célula conhecida ele calcula
> `f = g + h`: `g`, o custo real já percorrido, e `h`, uma estimativa
> admissível do que falta (aqui, a distância de Manhattan até a saída). Ele
> sempre expande a de menor `f`, isto é, a que está no caminho completo mais
> promissor. Como `h` nunca superestima, ele acha o mesmo caminho mínimo que a
> BFS — mas, por ter uma noção de direção, expande bem menos células: 16% menos
> no trajeto do labirinto da aula (37% na média de todas as partidas possíveis)
> e 10 vezes menos numa sala aberta.
