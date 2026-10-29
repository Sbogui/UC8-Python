# A03 — testes do conversor fictício

Código do estudante:
Arquivo e interpretador executados:
calculos_moedas.py; versão: Python 3.12.6.

## Retomada sem consulta
O que Exibir deve ler quando os campos foram editados sem confirmação?
Minha resposta inicial:
Ele só deve ler o último registro confirmado. Quando estão sendo editados, não devem entrar para o registro, sem a confimação.
Por que um erro não pode alterar parte do último registro válido?
Minha resposta inicial:
Porque um registro tem que representar uma tentativa inteira e válida. Se for enviado um registro incompleto, quando exibir o registro ele irá mostra o registro de outro juntamente com o ultimo incompleto.
O que get devolve? Por que int não serve para uma idade escrita como 2.5?
Minha resposta inicial:
o get devolve o valor da chave informada ou, se a chave não existir, o valor padrão passado na chamada. E int("2.5") dá ValueError, porque o texto "2.5" não representa um número inteiro; 

## Antes de programar
Unidade das cotações:
reais por 1 dólar (R$ por 1 USD) e reais por 1 euro (R$ por 1 EUR).

Operação escolhida para converter reais; justificativa por unidades:
divisão, reais / cotação. R$ dividido por (R$ por USD) deixa USD, pois os reais se cancelam. Multiplicar daria R$ ao quadrado por USD, que não é uma quantidade de dólares.

Quais entradas e resultados precisam pertencer à mesma tentativa?
Reais, cotação do dólar e cotação do euro, junto com os dois resultados (dolares e euros), confirmados no registro de uma só vez.

## Preveja e depois execute
As cotações desta tabela são fictícias. Mantenha a ordem quando o caso indicar.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular | "Nenhuma conversão confirmada nesta sessão." | Igual à previsão | Nenhum |
| T02 | Calcular reais 100, cotação USD 5 e EUR 4 | Confirmada; 20.00 USD e 25.00 EUR | Igual à previsão | Nenhum |
| T03 | Editar para 200 / 10 / 8; somente Exibir | Continua 100 / 5 / 4 com 20.00 USD e 25.00 EUR | Igual; Exibir lê só o registro | Nenhum |
| T04 | Após T02, Calcular com 200 / 10 / abc | Mensagem de erro; registro 100 / 5 / 4 intacto | Mensagem "Informe números válidos..." e registro intacto | Nenhum |
| T05 | Corrigir para 200 / 10 / 8 e Calcular | Confirmada; conjunto inteiro trocado: 200 / 10 / 8 com 20.00 USD e 25.00 EUR | Igual à previsão | Nenhum |
| T06 | Calcular com 100,50 / 5 / 4; repetir com 100.50 | Os dois aceitos e iguais: 20.10 USD e 25.12 EUR | Igual; o euro dá 25.125 e aparece 25.12 (arredondamento do :.2f) | Nenhum |
| T07 | Calcular com 0 / 5 / 4 | Aceito: 0.00 USD e 0.00 EUR | Igual à previsão | Nenhum |
| T08 | Reais negativos; cada cotação 0 e negativa, um teste por campo | Todos recusados; registro anterior mantido | Reais negativo: "O valor em reais não pode ser negativo."; cotações: "As cotações devem ser maiores que zero."; registro intacto nos cinco | Nenhum |
| T09 | Cada campo vazio, só espaços ou abc, um por vez | Todos recusados com mensagem de número inválido | Os nove casos recusados com a mesma mensagem genérica | |
| T10 | Texto 1.000,50 ou 1,000.50; depois 1000,50 sem milhares | Os com milhares recusados; 1000,50 aceito | Igual: com milhares recusados; 1000,50 virou 1000.5 e deu 200.10 USD e 250.12 EUR | |
| T11 | Após um válido, Limpar campos e depois Exibir | Campos vazios; Exibir mantém o último válido | Campos ficaram "" e Exibir manteve o registro | Nenhum |
| T12 | Calcular com 10 / 3 / 6; observar arredondamento de exibição | Exibe 3.33 USD e 1.67 EUR; em memória ficam valores longos | Tela: 3.33 e 1.67; em memória: 3.3333333333333335 e 1.6666666666666667 | Nenhum |
| T13 | Fechar, reabrir e Exibir | Começa sem conversão confirmada | Com registro novo vazio: "Nenhuma conversão confirmada nesta sessão." | Nenhum |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab: Tudo nos conformes
Usei o teclado para acionar um botão: Não funcionou o enter
Mensagem que precisei melhorar: Nenhuma
Colega que testou (código combinado): 

## Fechamento sem consulta
Por que a cotação precisa ser maior que zero, mas o valor em reais pode ser zero?
dividir por zero não tem resultado, e uma cotação negativa não faz sentido como preço de uma moeda. Já zero reais é um valor válido de entrada: dividido por uma cotação positiva dá 0 dólar e 0 euro, que é uma conversão correta.

Como evitar mostrar uma entrada atual com um resultado anterior?
validar tudo antes de calcular e confirmar entradas e resultados juntos, num único update do registro. Exibir lê só o registro, nunca os campos em edição.

Formatar com duas casas muda o número guardado no registro?
não. O :.2f só muda o texto exibido. Em 10 / 3 / 6, o registro guarda 3.3333333333333335 e a tela mostra 3.33.

Minha dificuldade, correção e próximo passo:
Pensar em como fazer as converções para exibir corretamente, pesquisei mais sobre calculos e como implementar em python, testar conversor.py com um colega.

Entregas: calculos_moedas.py, conversor.py e este registro preenchido.
