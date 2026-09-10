# N-Rainhas (N-Queens)

Solução do problema das N rainhas em Python puro, sem bibliotecas externas.

O objetivo é posicionar `n` rainhas em um tabuleiro `n x n` de forma que
nenhuma ataque outra — ou seja, sem duas rainhas na mesma linha, coluna
ou diagonal.

## Abordagem

Backtracking iterativo, uma rainha por linha, usando uma **lista encadeada
como pilha** (implementada do zero em `ListaEncadeada`):

- `push` / `pop` na cabeça da lista em `O(1)`;
- o vetor `proxima_col` guarda a próxima coluna a testar em cada linha,
  permitindo retomar a busca de onde parou ao retroceder;
- ao esgotar as colunas de uma linha, desempilha a última rainha e avança
  a coluna da linha anterior;
- se as colunas da linha 0 se esgotarem, não existe solução.

### Verificação de conflito

Uma posição `(x, y)` (coluna, linha) é válida se, para toda rainha `(rx, ry)`
já posicionada:

| Restrição | Teste |
|---|---|
| Mesma linha | `ry != y` |
| Mesma coluna | `rx != x` |
| Diagonal principal `\` | `rx - ry != x - y` |
| Diagonal secundária `/` | `rx + ry != x + y` |

## Uso

```bash
python3 nqueens-sol.py             # resolve n = 8
python3 nqueens-sol.py -n 6        # muda o tamanho do tabuleiro
python3 nqueens-sol.py -t          # mostra o processo de comparação
python3 nqueens-sol.py -t -b       # + desenha o tabuleiro a cada rainha
python3 nqueens-sol.py -t --sem-cor > traco.txt
```

| Opção | Efeito |
|---|---|
| `-n N` | Tamanho do tabuleiro (padrão: 8) |
| `-t`, `--traco` | Imprime cada comparação e destaca cada backtracking |
| `-b`, `--tabuleiro` | Com `--traco`, desenha o tabuleiro a cada rainha empilhada |
| `--sem-cor` | Desliga as cores ANSI (útil ao redirecionar a saída) |

Ou importe a função direto:

```python
from nqueens_sol import sol, imprimir_tabuleiro

rainhas = sol(8)
if rainhas is not None:
    imprimir_tabuleiro(rainhas, 8)
```

Para acompanhar a busca a partir do código, passe um `Traco`:

```python
from nqueens_sol import Cores, Traco, sol

rainhas = sol(8, Traco(8, Cores(ativo=True)))
```

Para obter também o tempo gasto, use `resolver`, que devolve
`(solução, segundos)`:

```python
from nqueens_sol import formatar_tempo, resolver

rainhas, decorrido = resolver(8)
print(formatar_tempo(decorrido))   # ex.: "2.14 ms"
```

## Traçado do backtracking (`--traco`)

Cada passo mostra a linha, a coluna testada e o veredito da comparação:

- `OK` — posição válida, rainha empilhada (a pilha é impressa ao lado);
- `CONFLITO` — qual restrição falhou e **com qual rainha** já posicionada;
- `<<< BACKTRACK` — as colunas da linha se esgotaram: a última rainha é
  desempilhada e a linha anterior retoma a busca na coluna seguinte.

Ao final, um resumo conta passos, tentativas, conflitos, backtrackings e o
tempo decorrido.

```
$ python3 nqueens-sol.py -t -n 6
Backtracking para n = 6
----------------------------------------------------------------
[0001] linha 0  testa col 0  OK  empilha (0, 0) | pilha: (0, 0)
[0002] linha 1  testa col 0  CONFLITO  mesma coluna com a rainha (0, 0)
[0003] linha 1  testa col 1  CONFLITO  diagonal principal \ com a rainha (0, 0)
[0004] linha 1  testa col 2  OK  empilha (2, 1) | pilha: (0, 0) -> (2, 1)
...
[0021] linha 5  testa col 5  CONFLITO  diagonal principal \ com a rainha (0, 0)
[0022] linha 5  colunas esgotadas  <<< BACKTRACK  desempilha (3, 4); linha 4 volta a testar a partir da col 4
[0023] linha 4  testa col 4  CONFLITO  mesma coluna com a rainha (4, 2)
...
----------------------------------------------------------------
solução encontrada | passos: 196 | tentativas: 171 | conflitos: 140 | backtracks: 25
tempo: 1.10 ms (inclui a impressão do traço)
```

No terminal, `OK` sai em verde, `CONFLITO` em amarelo e `BACKTRACK` em
vermelho-negrito. As cores são desligadas sozinhas quando a saída não é um
terminal.

## Tempo de execução

Toda execução informa quanto a busca levou, na unidade mais legível
(`µs`, `ms` ou `s`):

```
$ python3 nqueens-sol.py -n 8
tempo de busca: 2.14 ms

$ python3 nqueens-sol.py -n 3
Sem solução para n = 3  (tempo de busca: 74.3 µs)
```

O cronômetro cobre só o laço de backtracking — não a impressão do tabuleiro
final. Com `--traco`, porém, a impressão acontece **dentro** do laço e domina
a medição; por isso o rótulo muda para `tempo de busca + traço`. Para medir o
custo real do algoritmo, rode sem `--traco`.

## Saída de exemplo (`N = 8`)

```
(0, 0) -> (4, 1) -> (7, 2) -> (5, 3) -> (2, 4) -> (6, 5) -> (1, 6) -> (3, 7)
tempo de busca: 2.14 ms

Q . . . . . . .
. . . . Q . . .
. . . . . . . Q
. . . . . Q . .
. . Q . . . . .
. . . . . . Q .
. Q . . . . . .
. . . Q . . . .
```

## API

| Função | Descrição |
|---|---|
| `resolver(n, traco=None)` | Resolve e cronometra: devolve `(solução, segundos)`. A solução é uma `ListaEncadeada` com as posições das rainhas, ou `None` se não houver (`n = 2` e `n = 3`). Com um `Traco`, imprime a busca passo a passo |
| `sol(n, traco=None)` | `resolver` sem o cronômetro: devolve só a solução (ou `None`) |
| `formatar_tempo(segundos)` | Formata a duração em `µs`, `ms` ou `s` |
| `imprimir_tabuleiro(rainhas, n, indent="")` | Imprime o tabuleiro com `Q` nas rainhas e `.` nas casas vazias |
| `verificar_posicao_valida(rainhas, pos)` | Verifica se `pos` não conflita com nenhuma rainha já posicionada |
| `encontrar_conflito(rainhas, pos)` | Versão explicativa: devolve `(rainha, motivo)` do primeiro conflito, ou `None` |
| `Traco(n, cores, mostrar_tabuleiro=False)` | Formata o traçado e conta passos, tentativas, conflitos e backtrackings |
| `Cores(ativo)` | Códigos ANSI usados no traçado (vazios quando `ativo=False`) |

> `sol` continua com a assinatura e o retorno de antes — quem já usava a
> função não precisa mudar nada.

## Requisitos

Python 3.10+ (usa a sintaxe de tipos `X | None`). Sem dependências.
