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
python3 nqueens-sol.py
```

Para mudar o tamanho do tabuleiro, altere `N` no bloco `__main__`:

```python
if __name__ == "__main__":
    N = 8
    resultado = sol(N)
```

Ou importe a função direto:

```python
from nqueens_sol import sol, imprimir_tabuleiro

rainhas = sol(8)
if rainhas is not None:
    imprimir_tabuleiro(rainhas, 8)
```

## Saída de exemplo (`N = 8`)

```
(0, 0) -> (4, 1) -> (7, 2) -> (5, 3) -> (2, 4) -> (6, 5) -> (1, 6) -> (3, 7)

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
| `sol(n)` | Retorna uma `ListaEncadeada` com as posições das rainhas, ou `None` se não houver solução (`n = 2` e `n = 3`) |
| `imprimir_tabuleiro(rainhas, n)` | Imprime o tabuleiro com `Q` nas rainhas e `.` nas casas vazias |
| `verificar_posicao_valida(rainhas, pos)` | Verifica se `pos` não conflita com nenhuma rainha já posicionada |

## Requisitos

Python 3.10+ (usa a sintaxe de tipos `X | None`). Sem dependências.
