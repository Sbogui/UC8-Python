# A20: conferir vínculos por ID entre alunos, planos e matrículas (dados fictícios).
# alunos e planos: listas de dicionários com "id" e "nome".
# matrículas: lista de dicionários com "id", "aluno_id" e "plano_id".


def id_valido(valor):
    return type(valor) == int and valor > 0


def coletar_ids(registros, rotulo, problemas):
    ids = []
    for registro in registros:
        if type(registro) != dict:
            problemas.append(rotulo + ": cada registro deve ser um dicionário.")
            continue
        codigo = registro.get("id")
        if not id_valido(codigo):
            problemas.append(rotulo + ": ID inválido (" + repr(codigo) + ").")
        elif codigo in ids:
            problemas.append(rotulo + ": ID repetido (" + str(codigo) + ").")
        else:
            ids.append(codigo)
    return ids


def validar_vinculos(alunos, planos, matriculas):
    problemas = []
    ids_alunos = coletar_ids(alunos, "Aluno", problemas)
    ids_planos = coletar_ids(planos, "Plano", problemas)
    coletar_ids(matriculas, "Matrícula", problemas)
    for matricula in matriculas:
        if type(matricula) != dict:
            continue
        numero = matricula.get("id")
        aluno_id = matricula.get("aluno_id")
        plano_id = matricula.get("plano_id")
        if not id_valido(aluno_id):
            problemas.append("Matrícula " + str(numero) + ": aluno_id inválido (" + repr(aluno_id) + ").")
        elif aluno_id not in ids_alunos:
            problemas.append("Matrícula " + str(numero) + ": o aluno " + str(aluno_id) + " não existe.")
        if not id_valido(plano_id):
            problemas.append("Matrícula " + str(numero) + ": plano_id inválido (" + repr(plano_id) + ").")
        elif plano_id not in ids_planos:
            problemas.append("Matrícula " + str(numero) + ": o plano " + str(plano_id) + " não existe.")
    return problemas


def pode_excluir_aluno(codigo, matriculas):
    if not id_valido(codigo):
        return False
    for matricula in matriculas:
        if matricula.get("aluno_id") == codigo:
            return False
    return True


if __name__ == "__main__":
    alunos = [{"id": 41, "nome": "Lia fictícia"}]
    planos = [{"id": 7, "nome": "Treino"}]
    matriculas = [{"id": 1, "aluno_id": 41, "plano_id": 7}]
    print("Inicial:", validar_vinculos(alunos, planos, matriculas) == [])
    alunos[0]["nome"] = "Lia Silva"
    print("Após nome:", validar_vinculos(alunos, planos, matriculas) == [])
    matriculas[0]["aluno_id"] = 92
    print("Após ID:", validar_vinculos(alunos, planos, matriculas))
    matriculas[0]["aluno_id"] = 41
    print("Pode excluir o aluno 41?", pode_excluir_aluno(41, matriculas))
