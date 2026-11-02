from typing import NamedTuple, Tuple


# ==========================================================
# ESTRUTURA IMUTÁVEL DE DADOS
# ==========================================================

class Livro(NamedTuple):
    codigo: str
    titulo: str
    autor: str
    categoria: str
    disponivel: bool


# ==========================================================
# FUNÇÕES FUNCIONAIS
# ==========================================================

def filtrar_livros_disponiveis(
    livros: Tuple[Livro, ...],
    categoria: str
) -> Tuple[Livro, ...]:
    """
    Retorna os livros disponíveis de uma categoria.
    Não modifica a coleção original.
    """
    return tuple(
        filter(
            lambda livro: (
                livro.categoria.lower() == categoria.lower()
                and livro.disponivel
            ),
            livros
        )
    )


def obter_titulos(livros: Tuple[Livro, ...]) -> Tuple[str, ...]:
    """
    Retorna uma coleção com os títulos dos livros recebidos.
    """
    return tuple(map(lambda livro: livro.titulo, livros))


def contar_livros_disponiveis(
    livros: Tuple[Livro, ...]
) -> int:
    """
    Conta quantos livros estão disponíveis.
    """
    return sum(map(lambda livro: livro.disponivel, livros))


def buscar_livro_por_codigo(
    livros: Tuple[Livro, ...],
    codigo: str
):
    """
    Retorna o livro correspondente ao código.
    Caso não encontre, retorna None.
    """
    encontrados = tuple(
        filter(lambda livro: livro.codigo == codigo, livros)
    )

    return encontrados[0] if encontrados else None


# ==========================================================
# DADOS DE EXEMPLO
# ==========================================================

acervo = (
    Livro(
        "L001",
        "O Alienista",
        "Machado de Assis",
        "Literatura",
        True
    ),
    Livro(
        "L002",
        "Python para Iniciantes",
        "Autor Exemplo",
        "Tecnologia",
        True
    ),
    Livro(
        "L003",
        "Clean Code",
        "Robert C. Martin",
        "Tecnologia",
        True
    ),
    Livro(
        "L004",
        "Dom Casmurro",
        "Machado de Assis",
        "Literatura",
        False
    )
)


# ==========================================================
# EXECUÇÃO E TESTES
# ==========================================================

if __name__ == "__main__":

    # Guardamos a coleção original para verificar sua preservação.
    acervo_original = acervo

    # Filtragem por categoria.
    livros_tecnologia = filtrar_livros_disponiveis(
        acervo,
        "Tecnologia"
    )

    print("--- LIVROS DE TECNOLOGIA DISPONÍVEIS ---")

    for titulo in obter_titulos(livros_tecnologia):
        print(f"- {titulo}")

    # Contagem de livros disponíveis.
    quantidade = contar_livros_disponiveis(acervo)

    print("\nQuantidade de livros disponíveis:", quantidade)

    # Busca por código.
    livro_encontrado = buscar_livro_por_codigo(acervo, "L003")

    print("\n--- CONSULTA POR CÓDIGO ---")

    if livro_encontrado:
        print("Livro encontrado:", livro_encontrado.titulo)
    else:
        print("Livro não encontrado.")

    # Verificação de que os dados originais não foram modificados.
    print("\n--- VERIFICAÇÃO DOS DADOS ---")
    print("Acervo original preservado:", acervo == acervo_original)

    # Testes automatizados simples.
    assert len(livros_tecnologia) == 2
    assert quantidade == 3
    assert livro_encontrado is not None
    assert livro_encontrado.titulo == "Clean Code"
    assert acervo == acervo_original

    print("\nTodos os testes foram aprovados!")