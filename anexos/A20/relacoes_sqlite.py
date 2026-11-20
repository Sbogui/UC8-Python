# A20: comparar o vínculo em memória com uma chave estrangeira do SQLite.
from contextlib import closing
import sqlite3


def criar_tabelas(con):
    con.execute("CREATE TABLE alunos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL)")
    con.execute("CREATE TABLE planos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL)")
    con.execute("CREATE TABLE matriculas ("
                "id INTEGER PRIMARY KEY, "
                "aluno_id INTEGER NOT NULL REFERENCES alunos(id) ON DELETE RESTRICT, "
                "plano_id INTEGER NOT NULL REFERENCES planos(id) ON DELETE RESTRICT)")


def contar(con, tabela):
    return con.execute("SELECT COUNT(*) FROM " + tabela).fetchone()[0]


def demonstrar(mostrar=True):
    resultados = {}

    with closing(sqlite3.connect(":memory:")) as con:
        con.execute("PRAGMA foreign_keys = ON")  
        criar_tabelas(con)
        with con:
            con.execute("INSERT INTO alunos (id, nome) VALUES (1, 'Lia fictícia')")
            con.execute("INSERT INTO planos (id, nome) VALUES (7, 'Treino')")
            con.execute("INSERT INTO matriculas (id, aluno_id, plano_id) VALUES (1, 1, 7)")
        resultados["vinculo_valido"] = contar(con, "matriculas") == 1

        try:
            with con:
                con.execute("INSERT INTO matriculas (id, aluno_id, plano_id) VALUES (2, 99, 7)")
            resultados["id_inexistente_bloqueado"] = False
        except sqlite3.IntegrityError:
            resultados["id_inexistente_bloqueado"] = True

        try:
            with con:
                con.execute("DELETE FROM alunos WHERE id = 1")
            resultados["exclusao_vinculada_bloqueada"] = False
        except sqlite3.IntegrityError:
            resultados["exclusao_vinculada_bloqueada"] = True

        resultados["dados_preservados"] = (contar(con, "alunos") == 1
                                        and contar(con, "matriculas") == 1)

        with con:
            con.execute("DELETE FROM matriculas WHERE id = 1")
            con.execute("DELETE FROM alunos WHERE id = 1")
        resultados["correcao_revalidada"] = (contar(con, "alunos") == 0
                                            and contar(con, "matriculas") == 0)

    with closing(sqlite3.connect(":memory:")) as con:
        criar_tabelas(con)
        with con:
            con.execute("INSERT INTO planos (id, nome) VALUES (7, 'Treino')")
            con.execute("INSERT INTO matriculas (id, aluno_id, plano_id) VALUES (1, 99, 7)")
        resultados["sem_chave_estrangeira_aceita_orfa"] = contar(con, "matriculas") == 1

    if mostrar:
        for nome, valor in resultados.items():
            print(nome + ":", valor)
    return resultados


if __name__ == "__main__":
    demonstrar()
