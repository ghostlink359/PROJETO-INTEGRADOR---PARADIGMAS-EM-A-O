
% ==========================================================
% SISTEMA DE BIBLIOTECA ACADEMICA
% Paradigma: Programacao Logica
% Linguagem: Prolog
% Responsavel: Gabriel
% ==========================================================

% ==========================================================
% 1. BASE DE CONHECIMENTO - FATOS
% ==========================================================

% livro(Codigo, Titulo, Autor, Categoria).

livro(l001, 'O Alienista', 'Machado de Assis', literatura).
livro(l002, 'Python para Iniciantes', 'Autor Exemplo', tecnologia).
livro(l003, 'Clean Code', 'Robert C. Martin', tecnologia).
livro(l004, 'Dom Casmurro', 'Machado de Assis', literatura).
livro(l005, 'Algoritmos', 'Thomas Cormen', tecnologia).
livro(l006, 'O Cortico', 'Aluisio Azevedo', literatura).


% leitor(Codigo, Nome, Tipo).

leitor(a001, 'Ana Souza', aluno).
leitor(a002, 'Bruno Lima', aluno).
leitor(a003, 'Mariana Costa', aluno).
leitor(p001, 'Carlos Lima', professor).


% emprestimo(CodigoEmprestimo, CodigoLivro, CodigoLeitor).

emprestimo(e001, l004, a001).
emprestimo(e002, l003, a002).
emprestimo(e003, l005, p001).


% ==========================================================
% 2. REGRAS LOGICAS
% ==========================================================

% REGRA 1
% Um livro esta disponivel quando existe no acervo
% e nao possui um emprestimo registrado.

disponivel(CodigoLivro) :-
    livro(CodigoLivro, _, _, _),
    \+ emprestimo(_, CodigoLivro, _).


% REGRA 2
% Um livro esta emprestado quando existe
% um registro de emprestimo para ele.

emprestado(CodigoLivro) :-
    emprestimo(_, CodigoLivro, _).


% REGRA 3
% Verifica se um leitor possui algum emprestimo.

leitor_com_emprestimo(CodigoLeitor) :-
    leitor(CodigoLeitor, _, _),
    emprestimo(_, _, CodigoLeitor).


% REGRA 4
% Retorna os livros emprestados por determinado leitor.

livro_do_leitor(CodigoLeitor, Titulo) :-
    emprestimo(_, CodigoLivro, CodigoLeitor),
    livro(CodigoLivro, Titulo, _, _).


% REGRA 5
% Consulta livros disponiveis de determinada categoria.

livro_disponivel_categoria(Categoria, Titulo) :-
    livro(CodigoLivro, Titulo, _, Categoria),
    disponivel(CodigoLivro).


% REGRA 6
% Verifica se um leitor pode realizar o emprestimo
% de determinado livro.
% Nesta versao, basta estar cadastrado e o livro
% estar disponivel.

pode_emprestar(CodigoLeitor, CodigoLivro) :-
    leitor(CodigoLeitor, _, _),
    disponivel(CodigoLivro).


% REGRA 7
% Retorna o nome do leitor e o titulo do livro emprestado.

detalhes_emprestimo(NomeLeitor, TituloLivro) :-
    emprestimo(_, CodigoLivro, CodigoLeitor),
    leitor(CodigoLeitor, NomeLeitor, _),
    livro(CodigoLivro, TituloLivro, _, _).


% REGRA 8
% Identifica alunos que possuem emprestimos.

aluno_com_emprestimo(Nome) :-
    leitor(CodigoLeitor, Nome, aluno),
    leitor_com_emprestimo(CodigoLeitor).


% ==========================================================
% 3. CONSULTAS PARA TESTES
% ==========================================================

% Execute cada consulta separadamente no SWI-Prolog.
%
% CONSULTA 1 - Livro disponivel?
% ?- disponivel(l001).
%
% CONSULTA 2 - Livro emprestado?
% ?- emprestado(l004).
%
% CONSULTA 3 - Leitor possui emprestimo?
% ?- leitor_com_emprestimo(a001).
%
% CONSULTA 4 - Quais livros foram emprestados por Ana?
% ?- livro_do_leitor(a001, Titulo).
%
% CONSULTA 5 - Livros de tecnologia disponiveis.
% ?- livro_disponivel_categoria(tecnologia, Titulo).
%
% CONSULTA 6 - Ana pode emprestar o livro L001?
% ?- pode_emprestar(a001, l001).
%
% CONSULTA 7 - Quais alunos possuem emprestimos?
% ?- aluno_com_emprestimo(Nome).
%
% CONSULTA 8 - Quem emprestou cada livro?
% ?- detalhes_emprestimo(Nome, Titulo).
