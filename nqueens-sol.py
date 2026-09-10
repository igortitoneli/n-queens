import argparse
import sys
import time
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


# ---------------------------------------------------------------- verificações


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


def encontrar_conflito(
    rainhas: ListaEncadeada, pos: tuple[int, int]
) -> tuple[tuple[int, int], str] | None:
    """Versão explicativa de `verificar_posicao_valida`.

    Percorre a pilha do topo para a base e devolve a primeira rainha que ataca
    `pos`, junto do motivo. Devolve `None` se a posição for válida.
    """
    x, y = pos
    for rainha in rainhas:
        rx, ry = rainha
        if ry == y:
            return rainha, "mesma linha"
        if rx == x:
            return rainha, "mesma coluna"
        if rx - ry == x - y:
            return rainha, "diagonal principal \\"
        if rx + ry == x + y:
            return rainha, "diagonal secundária /"
    return None


# -------------------------------------------------------------------- tempo


def formatar_tempo(segundos: float) -> str:
    """Formata a duração na unidade mais legível (µs, ms ou s)."""
    if segundos < 1e-3:
        return f"{segundos * 1e6:.1f} µs"
    if segundos < 1:
        return f"{segundos * 1e3:.2f} ms"
    return f"{segundos:.3f} s"


# ------------------------------------------------------------------- traçado


class Cores:
    """Códigos ANSI (vazios quando a saída não é um terminal ou --sem-cor)."""

    def __init__(self, ativo: bool):
        self.reset = "\033[0m" if ativo else ""
        self.ok = "\033[32m" if ativo else ""
        self.conflito = "\033[33m" if ativo else ""
        self.backtrack = "\033[1;31m" if ativo else ""
        self.fraco = "\033[90m" if ativo else ""
        self.destaque = "\033[1;36m" if ativo else ""


class Traco:
    """Imprime o processo de comparação e contabiliza as estatísticas."""

    def __init__(self, n: int, cores: Cores, mostrar_tabuleiro: bool = False):
        self.n = n
        self.c = cores
        self.mostrar_tabuleiro = mostrar_tabuleiro
        self.passo = 0
        self.tentativas = 0
        self.conflitos = 0
        self.backtracks = 0

    def _prefixo(self, linha: int) -> str:
        self.passo += 1
        return f"{self.c.fraco}[{self.passo:04d}]{self.c.reset} linha {linha}"

    def cabecalho(self) -> None:
        print(f"{self.c.destaque}Backtracking para n = {self.n}{self.c.reset}")
        print(f"{self.c.fraco}{'-' * 64}{self.c.reset}")

    def aceita(
        self, pos: tuple[int, int], rainhas: ListaEncadeada
    ) -> None:
        self.tentativas += 1
        col, linha = pos
        print(
            f"{self._prefixo(linha)}  testa col {col}  "
            f"{self.c.ok}OK{self.c.reset}  "
            f"{self.c.fraco}empilha {pos} | pilha: {rainhas}{self.c.reset}"
        )
        if self.mostrar_tabuleiro:
            imprimir_tabuleiro(rainhas, self.n, indent="        ")

    def rejeita(
        self, pos: tuple[int, int], rainha: tuple[int, int], motivo: str
    ) -> None:
        self.tentativas += 1
        self.conflitos += 1
        col, linha = pos
        print(
            f"{self._prefixo(linha)}  testa col {col}  "
            f"{self.c.conflito}CONFLITO{self.c.reset}  "
            f"{motivo} com a rainha {rainha}"
        )

    def retrocede(
        self, linha: int, removida: tuple[int, int], proxima_col: int
    ) -> None:
        self.backtracks += 1
        print(
            f"{self._prefixo(linha)}  colunas esgotadas  "
            f"{self.c.backtrack}<<< BACKTRACK{self.c.reset}  "
            f"{self.c.backtrack}desempilha {removida}{self.c.reset}; "
            f"linha {linha - 1} volta a testar a partir da col {proxima_col}"
        )

    def sem_solucao(self) -> None:
        print(
            f"{self.c.backtrack}<<< BACKTRACK na linha 0: "
            f"não há mais colunas para testar -> sem solução{self.c.reset}"
        )

    def resumo(self, resolvido: bool, decorrido: float) -> None:
        print(f"{self.c.fraco}{'-' * 64}{self.c.reset}")
        status = (
            f"{self.c.ok}solução encontrada{self.c.reset}"
            if resolvido
            else f"{self.c.backtrack}sem solução{self.c.reset}"
        )
        print(
            f"{status} | passos: {self.passo} | tentativas: {self.tentativas} | "
            f"conflitos: {self.conflitos} | "
            f"{self.c.backtrack}backtracks: {self.backtracks}{self.c.reset}"
        )
        print(
            f"{self.c.fraco}tempo: {formatar_tempo(decorrido)} "
            f"(inclui a impressão do traço){self.c.reset}"
        )
        print()


# ------------------------------------------------------------------- solução


def resolver(
    n: int, traco: "Traco | None" = None
) -> tuple[ListaEncadeada | None, float]:
    """Backtracking iterativo: uma rainha por linha, pilha = lista encadeada.

    Devolve `(solução, segundos)`; a solução é `None` se não existir.
    Passe um `Traco` para imprimir cada comparação e cada retrocesso — nesse
    caso o tempo medido inclui o custo de imprimir o traço.
    """
    rainhas = ListaEncadeada()

    # próxima coluna a testar em cada linha
    proxima_col: list[int] = [0] * n

    if traco:
        traco.cabecalho()

    inicio = time.perf_counter()

    while len(rainhas) < n:
        linha = len(rainhas)
        col = proxima_col[linha]

        if col >= n:  # esgotou as colunas desta linha -> retrocede
            proxima_col[linha] = 0
            if linha == 0:
                decorrido = time.perf_counter() - inicio
                if traco:
                    traco.sem_solucao()
                    traco.resumo(resolvido=False, decorrido=decorrido)
                return None, decorrido  # não existe solução
            removida = rainhas.pop()
            proxima_col[len(rainhas)] += 1
            if traco:
                traco.retrocede(linha, removida, proxima_col[len(rainhas)])
            continue

        pos = (col, linha)
        conflito = encontrar_conflito(rainhas, pos) if traco else None

        if verificar_posicao_valida(rainhas, pos):
            rainhas.push(pos)
            if traco:
                traco.aceita(pos, rainhas)
        else:
            proxima_col[linha] += 1
            if traco and conflito:
                traco.rejeita(pos, *conflito)

    decorrido = time.perf_counter() - inicio

    if traco:
        traco.resumo(resolvido=True, decorrido=decorrido)

    return rainhas, decorrido


def sol(n: int, traco: "Traco | None" = None) -> ListaEncadeada | None:
    """`resolver` sem o cronômetro: devolve só a solução (ou `None`)."""
    return resolver(n, traco)[0]


def imprimir_tabuleiro(rainhas: ListaEncadeada, n: int, indent: str = "") -> None:
    colunas = {y: x for x, y in rainhas}
    for y in range(n):
        print(indent + " ".join("Q" if colunas.get(y) == x else "." for x in range(n)))


# ----------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="N-rainhas por backtracking iterativo com lista encadeada."
    )
    parser.add_argument("-n", type=int, default=8, help="tamanho do tabuleiro (padrão: 8)")
    parser.add_argument(
        "-t",
        "--traco",
        action="store_true",
        help="mostra o processo de comparação e destaca os backtrackings",
    )
    parser.add_argument(
        "-b",
        "--tabuleiro",
        action="store_true",
        help="com --traco, desenha o tabuleiro a cada rainha empilhada",
    )
    parser.add_argument("--sem-cor", action="store_true", help="desliga as cores ANSI")
    args = parser.parse_args(argv)

    if args.n < 1:
        parser.error("n deve ser >= 1")

    cores = Cores(ativo=not args.sem_cor and sys.stdout.isatty())
    traco = Traco(args.n, cores, args.tabuleiro) if args.traco else None

    resultado, decorrido = resolver(args.n, traco)
    rotulo = "tempo de busca" if traco is None else "tempo de busca + traço"

    if resultado is None:
        print(f"Sem solução para n = {args.n}  ({rotulo}: {formatar_tempo(decorrido)})")
        return 1

    print(resultado)
    print(f"{rotulo}: {formatar_tempo(decorrido)}")
    print()
    imprimir_tabuleiro(resultado, args.n)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except BrokenPipeError:  # saída cortada por `head`, `less`, etc.
        sys.stdout = None
        raise SystemExit(0)
