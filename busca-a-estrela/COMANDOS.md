# Comandos para rodar na apresentação (Windows / cmd)

Colinha de execução. Todos os comandos abaixo são para o **Prompt de Comando
(cmd)**. Rode-os um de cada vez, na ordem em que aparecem nos slides.

---

## 0. Antes de tudo: entrar na pasta

A pasta tem acento e espaços no caminho, então as **aspas são obrigatórias**:

```cmd
cd /d "C:\Users\gabri\OneDrive\Documentos\GitHub\SPI-IFAC\6- périodo\Inteligencia artificial\busca-a-estrela"
```

Confere se está no lugar certo:

```cmd
dir *.py
```

Tem que listar `busca.py`, `comparar.py`, `estrutura_labirinto.py`, `maze.py`,
`porque_recalcular.py` e `testes.py`.

> **Atalho:** abra a pasta no Explorer, clique na barra de endereço, digite
> `cmd` e dê Enter. O prompt já abre dentro dela.

---

## 1. Demo gráfica — `maze.py` *(slide 9)*

**É a demo principal. Deixe esta janela já aberta antes de começar a apresentar.**

```cmd
python maze.py
```

Controles durante a execução:

| Tecla | O que faz |
|---|---|
| `3` | roda a **BFS** |
| `4` | roda o **A\*** |
| `1` / `2` | aleatória / DFS |
| `R` | reinicia |
| `+` / `-` | acelera / desacelera |
| `ESC` | sai |

Roteiro na tela: tecla **3**, deixa a BFS terminar (mancha cresce em onda),
depois tecla **4** para o A\* (mancha estica rumo à saída). No fim, mostre que o
caminho verde tem **33 células nos dois**.

**Precisa do pygame.** Se der `ModuleNotFoundError: No module named 'pygame'`:

```cmd
pip install pygame
```

---

## 2. Tabela e mapas — `comparar.py` *(slides 10, 11 e 12)*

É o script que sustenta todos os números dos slides.

```cmd
python comparar.py
```

O que deve sair:

| Cenário | Resultado esperado |
|---|---|
| Labirinto da aula | BFS **161** expandidas · A\* **136** · ambos caminho **33** |
| | DFS 60 expandidas, mas caminho **35** (não é o mínimo) |
| | A\* sem desempate: **142** |
| Sala aberta 21×21 | BFS **361** · A\* **37** · ambos caminho **37** |

> A linha da **Aleatória** muda a cada execução (ela sorteia a célula). As outras
> três são determinísticas e repetem sempre o mesmo número.

---

## 3. Prova da otimalidade — `testes.py` *(slide 11)*

```cmd
python testes.py
```

Saída esperada: `OK` — o A\* achou o caminho mínimo em **168 de 168** partidas,
expandindo **13.077** células contra **20.708** da BFS (**37% a menos**).

---

## 4. Por que o `g` é recalculado — `porque_recalcular.py` *(slide 8)*

Use se perguntarem *"se todo passo custa igual, por que recalcular?"*.

```cmd
python porque_recalcular.py
```

Saída esperada: sem o recálculo o caminho piora em **91 das 168** partidas, e no
pior caso vai de 26 para 30 células.

---

## 5. Passo a passo do A\* — `busca.py` *(opcional, slide 7)*

Mostra o A\* célula por célula num labirinto pequeno, com `h`, fronteira e
visitados a cada passo. Bom se pedirem para "ver o algoritmo andando" sem gráfico.

```cmd
python busca.py
```

---

## 6. Heurística que superestima — `astar_labirinto.py` *(extra)*

Script independente (labirinto próprio, não usa os outros arquivos). Mostra os
três casos lado a lado e **comprova a limitação** que o slide 13 afirma:

```cmd
python astar_labirinto.py
```

| | nós expandidos | caminho |
|---|---:|---:|
| BFS | 303 | 42 |
| A\* com Manhattan | 95 | 42 |
| A\* com Manhattan ×3 | 94 | **56 — pior!** |

> **Atenção:** os números deste script **não** são os dos slides, porque ele usa
> um labirinto diferente. Só mostre se perguntarem sobre heurística inadmissível,
> e deixe claro que é outro mapa.
>
> Se as cores saírem como lixo no terminal, abra o arquivo e mude
> `USAR_COR = True` para `USAR_COR = False` (linha 36).

---

## Se algo der errado na hora

| Problema | Solução |
|---|---|
| `'python' não é reconhecido` | tente `py` no lugar de `python`: `py comparar.py` |
| `ModuleNotFoundError: pygame` | `pip install pygame` — ou pule para o `comparar.py`, que não precisa de nada |
| `can't open file ...` | você não está na pasta certa — refaça o passo 0 |
| Janela do pygame travada | `ESC` para sair, `python maze.py` de novo |
| Fonte muito pequena no projetor | no cmd: clique direito na barra de título → Propriedades → Fonte → tamanho 20+ |

**Plano B se o pygame falhar na frente da turma:** vá direto para o
`comparar.py`. Ele imprime os mesmos mapas em texto (`.` = visitado,
`*` = caminho) e todos os números, e só precisa do Python puro.
