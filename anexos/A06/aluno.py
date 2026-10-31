from math import isfinite


class Aluno:
    def __init__(self):
        self.nome = ""
        self.turma = ""
        self.notas = []

    def atualizar(self, nome, turma, notas_texto):
        nome = nome.strip()
        turma = turma.strip()
        if nome == "":
            return "Informe o nome."
        if turma == "":
            return "Informe a turma."
        if len(notas_texto) != 5:
            return "Informe exatamente cinco notas."

        notas = []  
        for posicao, texto in enumerate(notas_texto, start=1):
            try:
                nota = float(texto.strip().replace(",", "."))
            except ValueError:
                return f"Nota {posicao}: informe um número."
            if not isfinite(nota):
                return f"Nota {posicao}: informe um número."
            if nota < 0 or nota > 10: 
                return f"Nota {posicao}: use um valor de 0 a 10."
            notas.append(nota)

        self.nome = nome
        self.turma = turma
        self.notas = notas
        return "Registro confirmado."

    def calcular_media(self):
        if len(self.notas) == 0:
            return None
        return sum(self.notas) / len(self.notas)

    def resumo(self):
        media = self.calcular_media()
        if media is None:
            return "Nenhum registro escolar confirmado nesta sessão."
        textos_notas = []
        for nota in self.notas:
            textos_notas.append(str(nota))
        return (
            f"Aluno: {self.nome} | Turma: {self.turma} | "
            f"Notas: {', '.join(textos_notas)} | Média: {media:.1f}"
        )