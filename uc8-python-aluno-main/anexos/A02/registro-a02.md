# A02 — estados e transições do cadastro

Código do estudante:
Arquivo e interpretador executados: anexos/A02/terminal.py e anexos/A02/cadastro_completo.py, executados com Python 3.

## Retomada sem consulta
1. O que get devolve? Por que int pode falhar?
Minha resposta inicial: O get devolve oque for digitado na interface. Ele pode falhar quando é um digite letras ou um número "quebrado" como 1,5 ou 1.5 .
2. O que muda entre passar uma função e chamá-la ao ligar um botão?
Minha resposta inicial: 
3. Que caso detecta um nome preenchido somente com espaços?
Minha resposta inicial: O Strip() verifica se o texto tem espaço, como quando digitado assim "   " o Strip() ele irá deixar assim "" que permite detectar que o nome não foi informado..

## Preveja e depois execute (nomes sempre fictícios)
| Caso | Estado/ação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Abrir e Exibir antes de Registrar | | | |
| T02 | Registrar Lia / Costa / 18 e Exibir | | | |
| T03 | Editar para Rui / Lima / 22; somente Exibir | | | |
| T04 | Limpar campos e depois Exibir | | | |
| T05 | Após um válido, tentar registrar outro nome com idade abc | | | |
| T06 | Registrar Rui / Lima / 22; depois Exibir | | | |
| T07 | Nome vazio ou somente espaços | | | |
| T08 | Sobrenome vazio ou somente espaços | | | |
| T09 | Idade vazia, 0, -2 e 2.5 (um teste por entrada) | | | |
| T10 | Espaços nas pontas e nome composto | | | |
| T11 | Fechar, reabrir e Exibir | | | |

## Uso da interface
Percorri campos e botões com Tab/Shift+Tab:
Mensagem que precisei melhorar:
Colega que testou (código fictício ou combinado):

## Fechamento sem consulta
Por que Limpar campos não deve apagar o registro confirmado? Porque os campos representam os dados que estão sendo editados, enquanto o registro representa o último cadastro válido. Limpar deve permitir iniciar uma nova tentativa sem perder o cadastro confirmado.

Como uma tentativa inválida pode estragar um cadastro anterior se a ordem do código estiver errada? Se o programa atualizar o registro antes de validar todos os campos, uma tentativa inválida pode sobrescrever os dados válidos anteriores. Sabendo disso, a atualização sempre deve acontecer somente depois de todas as validações, para não ocorrer perda de dados válidos.

Minha dificuldade, ajuste e próximo passo: Minha dificuldade foi compreender a diferença entre os campos em edição e o registro confirmado. Ajustei a ordem das validações para preservar os dados válidos.

Entregas externas: estado_cadastro.py e cadastro_completo.py, além deste registro.
