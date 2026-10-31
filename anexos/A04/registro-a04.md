# A04 — testes do sistema escolar fictício

Código do estudante:
Arquivo e interpretador executados: medias.py e sistema_escolar.py; versão: Python 3.10.11

## Retomada sem consulta
O que deve acontecer ao último registro quando a última entrada é inválida?
Minha resposta inicial:
Nada.. o último registro confirmado permanece inteiro (nome, turma, notas e média). A mensagem de erro muda, mas o registro só é trocado quando uma tentativa inteira é válida.

O que get devolve? Como vírgula decimal é normalizada na A03?
Minha resposta inicial:
O get devolve o valor da chave informada ou, se ela não existir, o valor padrão passado na chamada (aqui, ""). A vírgula é normalizada com strip e replace: " 7,5 " vira "7.5", e então float converte para 7.5.

Digitar um novo nome confirma uma nova consulta? Por quê?
Minha resposta inicial:
Não. Digitar só altera a edição (a Entry e os campos). A consulta e o registro só mudam depois de Calcular média com tudo válido.
Exibir lê apenas o registro.

## Antes de programar
Quais valores pertencem ao mesmo registro confirmado? 
Nome, turma, a lista das cinco notas numéricas e a média, todos da mesma tentativa, confirmados de uma só vez.
Quantidade de notas exigida e intervalo permitido:
Exatamente cinco notas, cada uma de 0 a 10, com os limites incluídos (zero é nota válida).
Minha previsão para a média de 6, 7, 8, 9 e 10:
Minha previsão para a média de 6, 7, 8, 9 e 10: 8.0 (soma 40 dividida por 5).
Por que validar a quantidade antes de dividir?
Porque len(notas) é o divisor, com quatro ou seis notas a média sairia com outro divisor e o sistema aceitaria uma tentativa que não cumpre o requisito de cinco notas. Em lista vazia, dividiria por zero.

## Preveja e depois execute
Use identificação e notas fictícias. Nos casos com sequência, refaça o válido indicado.
| Caso | Entrada/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Calcular média | "Nenhum registro escolar confirmado nesta sessão." | Igual à previsão | Nenhum |
| T02 | Lia / T1 / notas 6, 7, 8, 9, 10 | Confirmado; média 8.0 | Lia / T1 / 6.0, 7.0, 8.0, 9.0, 10.0 / média 8.0 | Nenhum |
| T03 | Cinco notas zero, com identificação preenchida | Aceito (limite inferior); média 0.0 | Igual à previsão | Nenhum |
| T04 | Cinco notas 10, com identificação preenchida | Aceito (limite superior); média 10.0 | Igual à previsão | Nenhum |
| T05 | Notas 7,5 / 8 / 6,5 / 9 / 7; repetir usando ponto decimal | Os dois aceitos e iguais: soma 38, média 7.6 | Igual; as duas tentativas deram 7.6 | Nenhum |
| T06 | Após registrar T02, editar para Rui / T2 / cinco notas 5; somente Exibir | Continua o conjunto da Lia | Igual; Exibir leu só o registro | Nenhum |
| T07 | Após T02, tentar Rui / T2 / 5, 5, 5, 5, abc | "Nota 5: informe um número." e registro da Lia intacto | Igual: nome, turma, notas e média da Lia permaneceram | Nenhum |
| T08 | Corrigir a última nota de T07 para 5 e Calcular média | Confirmado; o conjunto inteiro troca para Rui / T2 / 5.0 x5 / média 5.0 | Igual à previsão | Nenhum |
| T09 | Nome vazio ou só espaços; repetir com turma vazia ou só espaços | "Informe o nome." / "Informe a turma."; registro intacto | Igual nos quatro casos | Nenhum |
| T10 | Cada nota vazia, só espaços ou letras; uma alteração por vez | 15 recusas "Nota N: informe um número."; registro intacto | Igual: a mensagem é a mesma para vazio, espaços e letras | Possivel mensagem para colocar: mensagem diferente para campo vazio (aplicar e retestar) |
| T11 | Cada nota -0,1 ou 10,1; uma alteração por vez | 10 recusas "Nota N: use um valor de 0 a 10."; registro intacto | Igual à previsão | Nenhum |
| T12 | Nome/turma/notas com espaços nas pontas; nome composto e acentos | Aceito; strip só nas pontas: José da Silva / Turma 1A / média 7.6 | Igual: espaços internos e acentos preservados | Nenhum |
| T13 | Após um válido, Limpar campos e depois Exibir | Campos vazios; Exibir mantém o último registro | Campos "", "" e cinco "" ; Exibir manteve o registro | Nenhum |
| T14 | Notas 6 / 6 / 6 / 6 / 6,4; comparar média guardada e exibida | Guardada perto de 6.08; exibida 6.1 | Guardada 6.08; exibida 6.1 | Nenhum |
| T15 | No terminal, lista com quatro notas e depois seis; uma tentativa por vez | "Informe exatamente cinco notas." nas duas; registro intacto | Igual à previsão | Nenhum |
| T16 | Fechar, reabrir e Exibir | Começa sem registro | Com registro novo vazio: "Nenhum registro escolar confirmado nesta sessão." | Nenhum |

## Uso da interface
Percorri nome, turma, cinco notas e botões com Tab/Shift+Tab: Percorreu corretamente.
Acionei um botão usando o teclado: 
Conferi rótulos e redimensionamento: Tudo certo
Mensagem que precisei melhorar: Distinguir campo vazio de texto inválido na mesma nota.
Colega que testou (código combinado): -

## Fechamento sem consulta
Qual a diferença entre sum(notas) e len(notas)?
sum soma os valores da lista (em 6, 7, 8, 9, 10 dá 40) e len conta quantos elementos ela tem (5). A média simples é sum dividido por len.

Por que uma lista nova de números ajuda a preservar a confirmação?
Porque a lista numérica da tentativa é montada à parte e só entra no registro depois de tudo validar. Ela é independente da lista de textos em edição, então editar uma não muda a outra e um erro no meio do laço não deixa o registro pela metade.

Qual dado o painel deve mostrar se eu editar a quinta nota sem calcular?
O último registro confirmado, com a quinta nota antiga e a média antiga, porque a edição não confirma nada.

Formatar com uma casa muda a média guardada?
Não. O :.1f só muda o texto exibido. Em 6 / 6 / 6 / 6 / 6,4, o registro guarda 6.08 e a tela mostra 6.1.

Minha dificuldade, ajuste e próxima tentativa: Foi pensar nos teste e como mostrar eles. 

Entregas: medias.py, sistema_escolar.py e este registro preenchido.

## Teoria e transferência
Consigo explicar o que sum e len calculam.
sum soma todos os valores da lista e len conta quantos elementos ela tem; a média simples é a soma dividida pela quantidade, por isso a quantidade precisa ser conferida antes.

Consigo distinguir uma lista de widgets de uma lista de textos/números.
entradas_notas guarda os widgets Entry (os campos da janela), só depois de chamar get em cada um eu tenho a lista de textos, e a lista de números é criada na validação, com float.

Consigo prever o registro após erro na quinta nota.
o registro continua exatamente o anterior, com nome, turma, notas e média, porque o update só roda depois de todas as validações.
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados: medias.py e sistema_escolar.py; Python 3.10.11 .
Pasta e comando usados: pasta A04: `python medias.py` e `python sistema_escolar.py`

Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos: 
Usei uma lista de cinco textos em edição e, a cada tentativa, crio uma lista nova de números com um laço for. Antes de dividir, confiro que há exatamente cinco notas, porque o len é o divisor. Cada nota é convertida e validada de 0 a 10, incluindo os limites. Só depois de validar tudo calculo a média com sum e len e faço um único update do registro com nome, turma, notas e média. Assim um erro na quinta nota não troca parte do conjunto anterior. A média é guardada como número e só formatada com uma casa na exibição.

Decisão do meu código sobre lista, laço, sum/len, cinco notas e confirmação integral: a lista numérica é local a cada tentativa, o laço com enumerate informa qual nota corrigir, sum/len só rodam com cinco notas válidas, o registro é atualizado de uma vez, nunca durante o laço.

Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
ainda não rodei a janela com um colega.
Caso para nova tentativa em sala:
