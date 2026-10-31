# Meu registro A06 — objetos e módulos

Nome/código individual: Lucas Miranda Fernandez
Turma e data: 14268

## Hipóteses sem consulta
O que fica confirmado após erro na quinta nota?
Tudo continua como estava: nome, turma, as cinco notas e a média do último registro válido. Só a mensagem de erro muda.

Qual a diferença entre editar, confirmar e limpar?
Editar é digitar nos campos (não confirma nada). Confirmar é o método atualizar aceitar um conjunto inteiro válido e gravar os três atributos. Limpar só esvazia os campos de edição; o confirmado e as consultas ficam.

O que aconteceria se dois nomes apontassem para o mesmo objeto?
Alterar por um dos nomes mudaria o que se vê pelo outro, porque seria um único objeto com dois nomes (rui = lia não cria um aluno novo).

## Arquitetura antes do código
Pasta com aluno.py, verificar_modelo.py e main.py:
A06/aluno.py (modelo), A06/verificar_modelo.py (verificações em texto) e A06/main.py (interface), todos na mesma pasta.

Qual arquivo contém regras? Qual cria widgets? Quem importa quem?
As regras ficam em aluno.py (classe Aluno). Os widgets são criados em main.py. verificar_modelo.py importa Aluno; main.py importa Aluno. aluno.py não importa ninguém do projeto nem Tkinter, então a dependência vai em uma direção só (duas setas apontando para aluno.py).

O que __init__ cria em cada nova instância?
nome e turma vazios e uma lista de notas nova e vazia, própria daquele objeto.

Por que duas chamadas Aluno() diferem de rui = lia?
Aluno() cria dois objetos independentes, cada um com a sua lista. rui = lia só dá outro nome ao mesmo objeto.

O que self identifica em uma chamada de método?
O objeto que recebeu a chamada. Em lia.atualizar(...), self é a lia, a chamada não repete lia como argumento.

## Testes executados
Preencha para cada caso: previsão | resultado observado | correção e nova tentativa.
Não marque como executado um teste ainda pendente.
- T01: Importar aluno sem Tk, sem janela e sem leitura de teclado.
  Previsão: importar só define a classe; nada abre.
  Observado: ao importar aluno, o módulo tkinter não foi carregado e nenhuma janela abriu.
  Correção/reteste: nenhuma.
- T02: Criar dois objetos; listas distintas; ambos sem média antes de confirmar.
  Previsão: lia is not rui; listas diferentes; calcular_media() devolve None nos dois.
  Observado: igual à previsão (também Aluno() duas vezes dá False em "primeiro is segundo").
  Correção/reteste: nenhuma.
- T03: Lia/T1/[6,7,8,9,10] e Rui/T2/[5,5,5,5,5]; médias 8.0 e 5.0.
  Previsão: "Registro confirmado." nos dois; médias 8.0 e 5.0.
  Observado: igual à previsão.
  Correção/reteste: nenhuma.
- T04: Atualizar só Lia; Rui mantém identificação, notas e média.
  Previsão: Lia passa a 10.0; o resumo do Rui fica idêntico.
  Observado: igual; Rui continuou Rui / T2 / média 5.0.
  Correção/reteste: nenhuma.
- T05: Após válido, tentar nome/turma vazios; preservar todo o registro.
  Previsão: "Informe o nome." / "Informe a turma."; registro intacto.
  Observado: igual, com nome vazio e turma só com espaços.
  Correção/reteste: nenhuma.
- T06: Após válido, erro na quinta nota; preservar os três atributos e resumo.
  Previsão: "Nota 5: informe um número." e nome, turma, notas, média e resumo iguais ao de antes.
  Observado: igual; comparei a tupla antes/depois do erro.
  Correção/reteste: nenhuma.
- T07: Testar 0 e 10, vírgula/ponto, negativos, >10, nan, inf, vazio e texto.
  Previsão: 0 e 10 aceitos; vírgula = ponto; os demais recusados com "Nota N: ...".
  Observado: cinco notas 0 deram média 0.0 (válida, não None); 7,5 e 7.5 deram o mesmo resultado (média 7.6); -0,1, 10,1, vazio, só espaços, abc, nan e inf foram recusados na nota 5 sem alterar o válido.
  Correção/reteste: nenhuma.
- T08: Recusar quantidade diferente de cinco notas, sem alterar o válido.
  Previsão: "Informe exatamente cinco notas." com quatro e com seis.
  Observado: igual; registro intacto.
  Correção/reteste: nenhuma.
- T09: Alterar a lista de textos original após atualizar; notas confirmadas não mudam.
  Previsão: as notas confirmadas continuam [6.0, 7.0, 8.0, 9.0, 10.0].
  Observado: igual, mesmo trocando originais[0] para "0" depois.
  Correção/reteste: nenhuma.
- T10: Executar verificar_modelo.py sem abrir GUI; cada assert corresponde a um caso.
  Previsão: "Verificações do modelo concluídas."; uma previsão errada de propósito dá AssertionError.
  Observado: a mensagem de conclusão apareceu. Troquei de propósito a previsão da média da Lia de 8.0 para 9.0 numa cópia: deu AssertionError na linha da previsão. Depois restaurei e voltou a passar.
  Correção/reteste: previsão errada provocada e restaurada.
- T11: Consultar antes do primeiro válido: orientação e nenhuma janela vazia.
  Previsão: orienta e não abre janela.
  Observado: "Calcule uma média válida antes de consultar." e 0 janelas abertas.
  Correção/reteste: nenhuma.
- T12: Confirmar Lia e abrir C1; editar Rui e errar a última nota: C1 e confirmado permanecem.
  Previsão: erro na nota 5; painel e C1 continuam com a Lia.
  Observado: igual; o painel e C1 mantiveram Lia / T1 / média 8.0.
  Correção/reteste: nenhuma.
- T13: Corrigir e confirmar Rui; C2 mostra Rui e C1 conserva Lia.
  Previsão: C1 com Lia; C2 com Rui, média 5.0.
  Observado: igual.
  Correção/reteste: nenhuma.
- T14: Limpar os sete campos; último registro e consultas continuam disponíveis.
  Previsão: sete campos vazios; painel e C1 intactos.
  Observado: igual; o foco volta ao nome pelo código (conferir na janela real).
  Correção/reteste: nenhuma.
- T15: Fechar consultas por botão, X e Escape; principal e outra consulta continuam funcionando.
  Previsão: cada fechamento destrói só a consulta.
  Observado: botão e Escape fecharam só a consulta; o X foi simulado pelo protocolo da janela (WM_DELETE_WINDOW) e também fechou só a consulta. A principal continuou aberta.
  Correção/reteste: nenhuma.
- T16: Conferir grupos, rótulos, expansão e percurso Tab; funcionar sem PNG.
  Previsão: grupos Identificação, Notas e Ações, entradas crescem, texto no lugar da imagem.
  Observado: grupos e texto conferidos pela criação da janela.
  Correção/reteste: 
- T17: Encerrar a principal e reabrir: começar sem registro; nenhum arquivo de dados gravado.
  Previsão: reaberta, "Nenhum registro escolar confirmado nesta sessão."; nenhum arquivo criado.
  Observado: reaberta, o painel voltou sem registro; o programa não grava arquivos.
  Correção/reteste: nenhuma.

## Explicação individual
Mostre dois objetos independentes e uma tentativa inválida após um válido.
No terminal: lia = Aluno(); rui = Aluno(); atualizar os dois e conferir 8.0 e 5.0; depois lia.atualizar("Rui", "T2", ["5", "5", "5", "5", "abc"]) devolve o erro e o resumo da lia continua igual.
Indique a linha que confirma o conjunto e por que a interface não repete a regra.
Nas linhas 35 a 37 de aluno.py (self.nome, self.turma e self.notas), logo depois de todas as validações. A interface só chama aluno.atualizar com textos e mostra a mensagem; se repetisse a regra, haveria duas fontes de verdade e elas poderiam divergir.
O que um assert verifica? Qual caso ainda falta?
Que uma condição prevista é verdadeira; se for falsa, o Python interrompe com AssertionError e mostra a linha. Ele serve para verificar o comportamento do modelo; a validação dos dados do usuário continua com if e mensagens. Caso que ainda falta:
Minha dificuldade e próximo teste:

Entrega: aluno.py, verificar_modelo.py, main.py e este registro.
Somente dados fictícios. A página não executa Python nem envia arquivos automaticamente.

## Teoria e transferência
Consigo apontar classe, instância, __init__ e self no exemplo.
Minha explicação:
Consigo provar que dois objetos mantêm dados independentes.
Minha explicação:
Consigo explicar a direção dos imports entre modelo, verificador e interface.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre classe, instância, listas próprias, confirmação integral e separação aluno/verificador/GUI:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
