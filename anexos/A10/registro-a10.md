# Meu registro A10 — Pizzaria: transferir o modelo de pedido

Nome/código individual, turma e data:
Lucas Miranda Fernandez - 14268

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Como eu pensei em diferenciar adicionar novamente e atualizar quantidade? Adicionar de novo soma na quantidade que já tinha, atualizar troca a quantidade por outra.
- Na A06, atribuir rui = lia cria outro objeto? Não, são dois nomes para o mesmo objeto.
- Por que a classe da A06 não precisa conhecer grid ou Entry? Porque ela só cuida dos dados e das regras, a janela fica em outro arquivo.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- modelos.py: quantidade, formatar, Produto, Pizza, Bebida, Item e Pedido. Não usa Tkinter.
- pagamento.py: igual ao da A08, sem mudança.
- verificar.py: testes com assert, sem janela. Importa modelos e pagamento.
- main.py: a janela. Importa modelos e pagamento.
- comparar_pysimplegui.py: só para comparar eventos..
Os dados ficam só enquanto a janela está aberta. Nenhum arquivo é gravado.
- Pizza e Bebida criam um Produto dentro delas (composição) para guardar código, nome e preço.
- Pizza ainda guarda o tamanho (Média ou Grande).
- O Item e o Pedido não mudaram por causa da pizza: só precisam de codigo, nome e preco_centavos.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Mussarela média 35,00 + dois refrigerantes 6,00: total 47,00.
Previsão: total 4700 centavos e "R$ 47,00".
Observado: Ocorreu tudo como esperado, Subtotal: R$47,00 | Desconto: R$ 0,00 (Credito em 1x), R$ 6,11 (Dinheirou ou pix) e R$3,76 (Debito)
Correção/reteste ou pendência: Tudo como o esperado.
 
T02 — Pizza com tamanho desconhecido: recusar.
Previsão: Pizza com tamanho "Gigante" dá ValueError.
Observado: Como o usuario não tem como "Escrever" o tamanho que quiser, não é pra acontecer esse erro.
Correção/reteste ou pendência:

T03 — Bebida e pizza coexistem com IDs distintos.
Previsão: PZ01, PZ02 e BB01 ficam em linhas separadas, 3 linhas no total. Total 3500 + 4500 + 600 = 8600.
Observado: igual. Ficaram 3 linhas e o total deu R$86,00.
Correção/reteste ou pendência: nenhuma.

T04 — Atualizar/remover preserva alvo por ID.
Previsão: atualizar BB01 para 5 muda só o refrigerante, remover PZ01 tira só essa linha.
Observado: igual. O refrigerante foi para 5, só ele mudou, e depois de remover PZ01 sobraram 2 linhas. O total ficou 6500.
Correção/reteste ou pendência: nenhuma.

T05 — Quantidades inválidas mantêm o pedido anterior.
Previsão: "0" e "abc" dão erro e o total continua igual.
Observado: igual. Os dois deram erro e o total não mudou.
Correção/reteste ou pendência: nenhuma.

T06 — Pagamento usa as mesmas regras da A08, sem desconto acumulado.
Previsão: subtotal 47,00. Dinheiro/PIX = 40,89; Débito = 43,24; Crédito 1x = 47,00.
Observado: Dinheiro/PIX deu 40.89 e Crédito 1x deu 47.00, como previsto.
Correção/reteste ou pendência: o Débito (43,24) não está no verificar.py atual; foi conferido direto pelo botão Conferir pagamento na janela.

T07 — Comparação de eventos não duplica o modelo nem exige migração.
Previsão: no PySimpleGUI o evento "Adicionar" chama o mesmo pedido.adicionar; o Pedido não é reescrito.
Observado: pelo código, o evento "Adicionar" chama pedido.adicionar(pizza, valores["qtd"]) e o Pedido continua o mesmo de modelos.py, sem cópia nem mudança.
Correção/reteste ou pendência: Aprimorar mais, pois está apenas com uma função.

T08 — Demonstração opcional informa ausência da biblioteca sem instalar nada.
Previsão: se não tiver PySimpleGUI, mostra a mensagem "não está instalado" e termina.
Observado: igual. Apareceu "PySimpleGUI não está instalado: comparação não executada." e o programa terminou.
Correção/reteste ou pendência: nenhuma.

## Explicação individual
Uma decisão que consigo justificar:
Pizza e Bebida usam um Produto dentro delas (composição). Assim o Item continua igual e só a pizza ganha o tamanho.

Uma dificuldade, apoio e próxima tentativa:
Minha dificuldade maior foi mais entender o principais pontos de mudança nos codigo que foi "Copiados" das outras aulas.

## Arquivos
Versão executada e arquivos baixados:
modelos.py, pagamento.py, verificar.py, main.py, comparar_pysimplegui.py
Caminho de dados fictícios usado (se houver):
nenhum, o catálogo fica fixo no main.py.
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo separar o que mudou do que foi reutilizado.
Minha explicação:  mudaram as classes Pizza, Bebida e o catálogo. Item, Pedido e pagamento.py foram reaproveitados.

Consigo explicar composição apontando a referência entre objetos.
Minha explicação: em Pizza, self.produto = Produto(...) guarda um Produto dentro da pizza.

Consigo mostrar como código/tamanho/preço chegam ao pedido.
Minha explicação: A pizza tem codigo, nome e preco_centavos (vindos do Produto) e o tamanho. O Item usa o preço e a quantidade para o subtotal.

Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre transferência Produto/Pizza/Bebida, composição e contrato do pedido:
Eu fiz Pizza e Bebida criarem um Produto dentro delas. O Produto guarda código, nome e preço.
Assim o Item não precisa saber se o produto é pizza ou bebida, ele só usa o preço e a quantidade.
Por isso não precisei mexer no cálculo do total nem no Pedido.
O tamanho só existe na Pizza e é validado, só aceita Média ou Grande.
Se eu criar uma pizza com outro tamanho, dá erro e o pedido não muda.
Minha explicação / anexo:


## Checklist da interface
Controles e rótulos que conferi:
Produto (lista), Quantidade (campo), tabela com Código, Produto, Qtd e Subtotal, Forma de pagamento (lista), botões Adicionar, Atualizar, Remover e Conferir pagamento, e o texto de aviso no fim da janela.
Percurso por Tab/Shift+Tab e acionamento:
Pela ordem em que criei os controles, o Tab deve ir Produto > Quantidade > Tabela > Forma de pagamento > Adicionar > Atualizar > Remover > Conferir pagamento. Os botões acionam com a barra de espaço.
Mensagem após erro e possibilidade de corrigir:
O erro aparece no texto de aviso e o pedido não muda. O campo de quantidade só é limpo quando dá certo, então o texto digitado continua lá para eu corrigir e clicar de novo.
Redimensionamento e comportamento que observei:
Só a tabela cresce quando a janela aumenta; os outros controles ficam do mesmo tamanho.

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
