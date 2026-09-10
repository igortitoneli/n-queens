from collections.abc import Iterator


class No:
    """Nó da lista encadeada: guarda a posição (x=coluna, y=linha) de uma rainha."""

    def __init__(self, pos: tuple[int, int], prox: "No | None" = None):
        self.pos = pos
        self.prox = prox


class ListaEncadeada:
    """Lista encadeada usada como pilha: topo = cabeça (push/pop em O(1))."""

    def __init__(self):
        self.cabeca: No | None = None
        self.tamanho: int = 0

    def push(self, pos: tuple[int, int]) -> None:
        self.cabeca = No(pos, self.cabeca)
        self.tamanho += 1

    def pop(self) -> tuple[int, int]:
        if self.cabeca is None:
            raise IndexError("pop em lista vazia")
        no = self.cabeca
        self.cabeca = no.prox
        self.tamanho -= 1
        return no.pos

    def topo(self) -> tuple[int, int] | None:
        return self.cabeca.pos if self.cabeca else None

    def __iter__(self) -> Iterator[tuple[int, int]]:
        no = self.cabeca
        while no is not None:
            yield no.pos
            no = no.prox

    def __len__(self) -> int:
        return self.tamanho

    def __repr__(self) -> str:
        return " -> ".join(str(p) for p in reversed(list(self))) or "vazia"


def verificar_col(rainhas: ListaEncadeada, pos: tuple[int, int]) -> bool:
    """Nenhuma rainha já colocada pode estar na mesma coluna."""
    x, _ = pos
    return all(rx != x for rx, _ in rainhas)


def verificar_linha(rainhas: ListaEncadeada, pos: tuple[int, int]) -> bool:
    """Nenhuma rainha já colocada pode estar na mesma linha."""
    _, y = pos
    return all(ry != y for _, ry in rainhas)


def verificar_diagonal_principal(rainhas: ListaEncadeada, pos: tuple[int, int]) -> bool:
    """Diagonal '\\': x - y constante."""
    x, y = pos
    return all(rx - ry != x - y for rx, ry in rainhas)


def verificar_diagonal_secundaria(rainhas: ListaEncadeada, pos: tuple[int, int]) -> bool:
    """Diagonal '/': x + y constante."""
    x, y = pos
    return all(rx + ry != x + y for rx, ry in rainhas)


def verificar_posicao_valida(rainhas: ListaEncadeada, pos: tuple[int, int]) -> bool:
    return (
        verificar_linha(rainhas, pos)
        and verificar_col(rainhas, pos)
        and verificar_diagonal_principal(rainhas, pos)
        and verificar_diagonal_secundaria(rainhas, pos)
    )


def sol(n: int) -> ListaEncadeada | None:
    """Backtracking iterativo: uma rainha por linha, pilha = lista encadeada."""
    rainhas = ListaEncadeada()

    # próxima coluna a testar em cada linha
    proxima_col: list[int] = [0] * n

    while len(rainhas) < n:
        linha = len(rainhas)
        col = proxima_col[linha]

        if col >= n:  # esgotou as colunas desta linha -> retrocede
            proxima_col[linha] = 0
            if linha == 0:
                return None  # não existe solução
            rainhas.pop()
            proxima_col[len(rainhas)] += 1
            continue

        if verificar_posicao_valida(rainhas, (col, linha)):
            rainhas.push((col, linha))
        else:
            proxima_col[linha] += 1

    return rainhas


def imprimir_tabuleiro(rainhas: ListaEncadeada, n: int) -> None:
    colunas = {y: x for x, y in rainhas}
    for y in range(n):
        print(" ".join("Q" if colunas.get(y) == x else "." for x in range(n)))


if __name__ == "__main__":
    N = 8
    resultado = sol(N)

    if resultado is None:
        print(f"Sem solução para n = {N}")
    else:
        print(resultado)
        print()
        imprimir_tabuleiro(resultado, N)
