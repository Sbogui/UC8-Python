"""A01 — prática 1. Use somente nome e idade fictícios."""

def conferir(nome, idade_texto):
    nomeLimpo = nome.strip()                            # TODO: retirar espaços nas pontas e recusar nome sem texto.

    if not nomeLimpo:
        return "O nome não pode ficar vazio!"

    try:                                                # TODO: converter idade para int, tratar ValueError e exigir idade > 0.
        idade_numero = int(idade_texto)
    except ValueError:
        return "Coloque a idade como número inteiro!"

    if idade_numero <= 0:                               # TODO: retornar mensagem coerente; não gravar arquivos.
        return "A idade tem que ser maior que 0!"

    return f"\nCadastro Realizado\nNome: {nomeLimpo}\nIdade: {idade_numero} anos"


if __name__ == "__main__":
    nome = input("Nome fictício: ")
    idade_texto = input("Idade fictícia: ")
    print(conferir(nome, idade_texto))
