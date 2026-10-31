from aluno import Aluno


def verificar_independencia():
    lia = Aluno()
    rui = Aluno()

    assert lia is not rui
    assert lia.notas is not rui.notas
    assert lia.calcular_media() is None
    assert rui.calcular_media() is None

    assert lia.atualizar("Lia", "T1", ["6", "7", "8", "9", "10"]) == "Registro confirmado."
    assert rui.atualizar("Rui", "T2", ["5", "5", "5", "5", "5"]) == "Registro confirmado."
    assert lia.calcular_media() == 8.0
    assert rui.calcular_media() == 5.0

    resumo_rui = rui.resumo()
    lia.atualizar("Lia Maria", "T3", ["10", "10", "10", "10", "10"])
    assert lia.calcular_media() == 10.0
    assert rui.resumo() == resumo_rui
    assert rui.nome == "Rui" and rui.turma == "T2" and rui.calcular_media() == 5.0
    return True


def verificar_validacao():
    aluno = Aluno()
    textos = ["6", "7", "8", "9", "10"]
    assert aluno.atualizar("Lia", "T1", textos) == "Registro confirmado."
    antes = (aluno.nome, aluno.turma, list(aluno.notas), aluno.calcular_media(), aluno.resumo())

    assert aluno.atualizar("Rui", "T2", ["5", "5", "5", "5", "abc"]) == "Nota 5: informe um número."
    depois = (aluno.nome, aluno.turma, list(aluno.notas), aluno.calcular_media(), aluno.resumo())
    assert antes == depois

    assert aluno.atualizar("", "T2", textos) == "Informe o nome."
    assert aluno.atualizar("Rui", "   ", textos) == "Informe a turma."
    assert aluno.atualizar("Rui", "T2", ["5", "5", "5", "5"]) == "Informe exatamente cinco notas."
    assert aluno.atualizar("Rui", "T2", ["5"] * 6) == "Informe exatamente cinco notas."
    assert antes == (aluno.nome, aluno.turma, list(aluno.notas), aluno.calcular_media(), aluno.resumo())

    zero = Aluno()
    assert zero.atualizar("Ana", "T1", ["0"] * 5) == "Registro confirmado."
    assert zero.calcular_media() == 0.0 and zero.calcular_media() is not None

    virgula = Aluno()
    ponto = Aluno()
    virgula.atualizar("Bia", "T1", ["7,5", "8", "6,5", "9", "7"])
    ponto.atualizar("Bia", "T1", ["7.5", "8", "6.5", "9", "7"])
    assert virgula.notas == ponto.notas and virgula.calcular_media() == 7.6

    for ruim in ["-0,1", "10,1", "", "   ", "abc", "nan", "inf"]:
        assert aluno.atualizar("Rui", "T2", ["5", "5", "5", "5", ruim]).startswith("Nota 5:")
    assert antes == (aluno.nome, aluno.turma, list(aluno.notas), aluno.calcular_media(), aluno.resumo())

    originais = ["6", "7", "8", "9", "10"]
    independente = Aluno()
    independente.atualizar("Lia", "T1", originais)
    originais[0] = "0"
    assert independente.notas == [6.0, 7.0, 8.0, 9.0, 10.0]
    return True


if __name__ == "__main__":
    independencia = verificar_independencia()
    validacao = verificar_validacao()
    if independencia and validacao:
        print("Verificações do modelo concluídas.")
    else:
        print("Verificações incompletas; implemente e execute os casos.")
