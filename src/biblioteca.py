from abc import ABC, abstractmethod
from datetime import date


# ==========================================================
# CLASSES DE DOMÍNIO
# ==========================================================

class Livro:
    def __init__(self, codigo, titulo, autor, categoria):
        self._codigo = codigo
        self._titulo = titulo
        self._autor = autor
        self._categoria = categoria
        self._disponivel = True

    @property
    def codigo(self):
        return self._codigo

    @property
    def titulo(self):
        return self._titulo

    @property
    def autor(self):
        return self._autor

    @property
    def categoria(self):
        return self._categoria

    @property
    def disponivel(self):
        return self._disponivel

    def _alterar_disponibilidade(self, disponivel):
        self._disponivel = disponivel

    def __str__(self):
        status = "Disponível" if self.disponivel else "Emprestado"
        return (
            f"{self.titulo} - {self.autor} "
            f"({self.categoria}) | {status}"
        )


class Leitor:
    def __init__(self, codigo, nome):
        self._codigo = codigo
        self._nome = nome

    @property
    def codigo(self):
        return self._codigo

    @property
    def nome(self):
        return self._nome

    def obter_tipo(self):
        return "Leitor"

    def __str__(self):
        return f"{self.nome} ({self.obter_tipo()})"


class Aluno(Leitor):
    def __init__(self, codigo, nome, curso):
        super().__init__(codigo, nome)
        self._curso = curso

    @property
    def curso(self):
        return self._curso

    def obter_tipo(self):
        return "Aluno"


class Professor(Leitor):
    def __init__(self, codigo, nome, departamento):
        super().__init__(codigo, nome)
        self._departamento = departamento

    @property
    def departamento(self):
        return self._departamento

    def obter_tipo(self):
        return "Professor"


class Emprestimo:
    def __init__(self, codigo, livro, leitor):
        self._codigo = codigo
        self._livro = livro
        self._leitor = leitor
        self._data_emprestimo = date.today()
        self._data_devolucao = None
        self._ativo = True

    @property
    def codigo(self):
        return self._codigo

    @property
    def livro(self):
        return self._livro

    @property
    def leitor(self):
        return self._leitor

    @property
    def data_emprestimo(self):
        return self._data_emprestimo

    @property
    def data_devolucao(self):
        return self._data_devolucao

    @property
    def ativo(self):
        return self._ativo

    def finalizar(self):
        if not self._ativo:
            raise ValueError("Este empréstimo já foi finalizado.")

        self._ativo = False
        self._data_devolucao = date.today()


# ==========================================================
# NOTIFICAÇÕES E POLIMORFISMO
# ==========================================================

class Notificador(ABC):
    @abstractmethod
    def notificar(self, evento, mensagem):
        pass


class NotificadorConsole(Notificador):
    def notificar(self, evento, mensagem):
        print(f"[NOTIFICAÇÃO - {evento}] {mensagem}")


class NotificadorLista(Notificador):
    def __init__(self):
        self.mensagens = []

    def notificar(self, evento, mensagem):
        self.mensagens.append(f"[{evento}] {mensagem}")


# ==========================================================
# SISTEMA PRINCIPAL
# ==========================================================

class Biblioteca:
    def __init__(self, nome):
        self._nome = nome
        self._livros = {}
        self._leitores = {}
        self._emprestimos = {}
        self._notificadores = []
        self._proximo_emprestimo = 1

    @property
    def nome(self):
        return self._nome

    def adicionar_livro(self, livro):
        if livro.codigo in self._livros:
            raise ValueError("Já existe um livro com esse código.")

        self._livros[livro.codigo] = livro

    def adicionar_leitor(self, leitor):
        if leitor.codigo in self._leitores:
            raise ValueError("Já existe um leitor com esse código.")

        self._leitores[leitor.codigo] = leitor

    def adicionar_notificador(self, notificador):
        if not isinstance(notificador, Notificador):
            raise TypeError("O notificador deve implementar Notificador.")

        self._notificadores.append(notificador)

    def _disparar_evento(self, evento, mensagem):
        for notificador in self._notificadores:
            notificador.notificar(evento, mensagem)

    def consultar_livros(self):
        return list(self._livros.values())

    def consultar_livros_disponiveis(self):
        return [
            livro
            for livro in self._livros.values()
            if livro.disponivel
        ]

    def consultar_emprestimos_por_leitor(self, codigo_leitor):
        if codigo_leitor not in self._leitores:
            raise ValueError("Leitor não encontrado.")

        return [
            emprestimo
            for emprestimo in self._emprestimos.values()
            if emprestimo.leitor.codigo == codigo_leitor
        ]

    def emprestar_livro(self, codigo_livro, codigo_leitor):
        if codigo_livro not in self._livros:
            raise ValueError("Livro não encontrado.")

        if codigo_leitor not in self._leitores:
            raise ValueError("Leitor não encontrado.")

        livro = self._livros[codigo_livro]
        leitor = self._leitores[codigo_leitor]

        if not livro.disponivel:
            raise ValueError("O livro não está disponível.")

        emprestimo = Emprestimo(
            self._proximo_emprestimo,
            livro,
            leitor
        )

        self._emprestimos[emprestimo.codigo] = emprestimo
        self._proximo_emprestimo += 1

        livro._alterar_disponibilidade(False)

        mensagem = (
            f'Livro "{livro.titulo}" emprestado para {leitor.nome}.'
        )
        self._disparar_evento("EMPRÉSTIMO", mensagem)

        return emprestimo

    def devolver_livro(self, codigo_emprestimo):
        if codigo_emprestimo not in self._emprestimos:
            raise ValueError("Empréstimo não encontrado.")

        emprestimo = self._emprestimos[codigo_emprestimo]

        if not emprestimo.ativo:
            raise ValueError("Este empréstimo já foi finalizado.")

        emprestimo.finalizar()
        emprestimo.livro._alterar_disponibilidade(True)

        mensagem = (
            f'Livro "{emprestimo.livro.titulo}" '
            f'devolvido por {emprestimo.leitor.nome}.'
        )
        self._disparar_evento("DEVOLUÇÃO", mensagem)

        return emprestimo


# ==========================================================
# EXECUÇÃO DE EXEMPLO
# ==========================================================

if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca Acadêmica")

    # Cadastro de livros
    livro1 = Livro(
        "L001",
        "O Alienista",
        "Machado de Assis",
        "Literatura"
    )

    livro2 = Livro(
        "L002",
        "Python para Iniciantes",
        "Autor Exemplo",
        "Tecnologia"
    )

    biblioteca.adicionar_livro(livro1)
    biblioteca.adicionar_livro(livro2)

    # Cadastro de leitores
    aluno = Aluno("A001", "Ana Souza", "Engenharia de Software")
    professor = Professor("P001", "Carlos Lima", "Computação")

    biblioteca.adicionar_leitor(aluno)
    biblioteca.adicionar_leitor(professor)

    # Registro de notificadores
    notificador = NotificadorConsole()
    biblioteca.adicionar_notificador(notificador)

    # Empréstimo
    emprestimo = biblioteca.emprestar_livro("L001", "A001")

    print("\n--- SITUAÇÃO APÓS O EMPRÉSTIMO ---")
    print("Empréstimo ativo:", emprestimo.ativo)
    print("Livro disponível?", livro1.disponivel)

    # Devolução
    biblioteca.devolver_livro(emprestimo.codigo)

    print("\n--- SITUAÇÃO APÓS A DEVOLUÇÃO ---")
    print("Empréstimo ativo:", emprestimo.ativo)
    print("Livro disponível?", livro1.disponivel)

    # Demonstração de herança e polimorfismo
    print("\n--- LEITORES CADASTRADOS ---")
    for leitor in [aluno, professor]:
        print(leitor)