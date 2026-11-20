# A20: verificações sem janela. Execute com: python verificar.py
from vinculos import validar_vinculos, pode_excluir_aluno
from relacoes_sqlite import demonstrar


def verificar():
    alunos = [{"id": 41, "nome": "Lia fictícia"}]
    planos = [{"id": 7, "nome": "Treino"}]
    matriculas = [{"id": 1, "aluno_id": 41, "plano_id": 7}]

    # T01 - vínculos válidos não apontam para IDs inexistentes
    assert validar_vinculos(alunos, planos, matriculas) == []
    alunos[0]["nome"] = "Lia Silva"  # mudar só o nome não muda o vínculo
    assert validar_vinculos(alunos, planos, matriculas) == []

    # T02 - aluno/plano ausente é identificado sem alterar os dados
    matriculas_ruins = [{"id": 1, "aluno_id": 92, "plano_id": 99}]
    antes_alunos = [dict(a) for a in alunos]
    antes_planos = [dict(p) for p in planos]
    antes_matriculas = [dict(m) for m in matriculas_ruins]
    problemas = validar_vinculos(alunos, planos, matriculas_ruins)
    assert len(problemas) == 2
    assert alunos == antes_alunos
    assert planos == antes_planos
    assert matriculas_ruins == antes_matriculas

    # T03 - IDs duplicados, booleanos, negativos, zero ou em texto são recusados
    casos = [
        ([{"id": 1, "nome": "A"}, {"id": 1, "nome": "B"}], planos, []),
        ([{"id": True, "nome": "A"}], planos, []),
        ([{"id": -3, "nome": "A"}], planos, []),
        ([{"id": 0, "nome": "A"}], planos, []),
        ([{"id": "5", "nome": "A"}], planos, []),
        (alunos, [{"id": 7, "nome": "P"}, {"id": 7, "nome": "Q"}], []),
        (alunos, planos, [{"id": 1, "aluno_id": True, "plano_id": 7}]),
        (alunos, planos, [{"id": 1, "aluno_id": 41, "plano_id": -7}]),
    ]
    for lista_alunos, lista_planos, lista_matriculas in casos:
        assert len(validar_vinculos(lista_alunos, lista_planos, lista_matriculas)) >= 1

    # T04 - aluno com matrícula não pode ser excluído pelo contrato
    assert pode_excluir_aluno(41, matriculas) is False
    assert pode_excluir_aluno(55, matriculas) is True  # aluno sem matrícula
    assert pode_excluir_aluno(True, matriculas) is False
    assert pode_excluir_aluno(-1, matriculas) is False
    assert validar_vinculos(alunos, planos, matriculas) == []  # nada foi alterado

    # T05 e T06 - SQLite com foreign_keys ligado bloqueia e preserva
    resultados = demonstrar(False)
    assert resultados["vinculo_valido"] is True
    assert resultados["id_inexistente_bloqueado"] is True
    assert resultados["exclusao_vinculada_bloqueada"] is True
    assert resultados["dados_preservados"] is True
    assert resultados["correcao_revalidada"] is True
    assert resultados["sem_chave_estrangeira_aceita_orfa"] is True

    return True


if __name__ == "__main__":
    if verificar():
        print("Casos executados: previsões e resultados conferem.")
    else:
        print("Verificações ainda incompletas.")
