# Meu registro A11 — Pizzaria: estados, confirmação e cancelamento

Nome/código individual, turma e data:
Lucas Miranda Fernandez, 14268 , 08/11/26

## Retomada sem consulta
Minha hipótese inicial para cada item:
- O que permite pizza e bebida no mesmo pedido?
O item não pergunta se o produto é pizza ou bebida, Ele apenas usa produto.preco_centavos e a quantidade para calcular o subtotal. Como PIzza e Bebida têm codigo, nome e preco_centavos, o item aceita os dois do mesmo jeito. Isso é o “contrato” da A10, que quem oferece esses três dados pode entrar no pedido. Por isso o Pedido não precisou mudar quando a pizza apareceu.
- Como a quantidade inválida da A07 afeta um pedido já válido?
Não afeta, e a razão está na ordem do código. No adicionar, a quantidade é validada primeiro (por quantidade(...) ou ao criar o Item), e a mudança no pedido só acontece depois.
- Por que o subtotal não vem da posição da linha?
A posição na tabela muda. Se você remover a primeira linha, a segunda vira a primeira. Se usasse a posição para achar o item, poderia calcular ou alterar o item errado. O código do produto (PZ01, BB01) não muda, então o Pedido guarda os itens em um dicionário com o código como chave (self.itens[codigo]). O subtotal vem do Item achado por esse código: quantidade * preço.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- modelos.py: Produto, Pizza, Bebida, Item e Pedido. O Pedido agora tem estado, versão e comprovante. Não usa Tkinter. Importa o pagamento.py.
- pagamento.py: igual ao da A08/A10, sem mudança.
- verificar.py: testes com assert, sem janela.
- main.py: a janela principal e a janela de confirmação.
Os dados ficam só enquanto a janela está aberta. Nenhum arquivo é gravado.
- estado: "montagem" ou "finalizado".
- versão: um número que sobe quando adiciono, atualizo ou removo um item.
- comprovante: guardado quando finaliza, com itens, forma, subtotal, desconto e total.


## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Vazio não finaliza.
Previsão: finalizar com o pedido vazio dá erro "Adicione ao menos um item antes de finalizar." e o estado continua "montagem". Na janela, só aparece o aviso e a prévia não abre.
Observado: Resultado ocorreu como o esperado.
Correção/reteste ou pendência: Nenhum.

T02 — Forma ausente não finaliza.
Previsão: com itens mas sem forma de pagamento, dá erro "Escolha a forma de pagamento." Os itens e o estado continuam iguais.
Observado: Resultado ocorreu como o esperado.
Correção/reteste ou pendência: Nenhum.

T03 — Cancelar, X e Escape preservam montagem e itens.
Previsão: os três só fecham a prévia. Os itens, o total (4700) e o estado "montagem" ficam iguais, e o pedido não é finalizado.
Observado: Resultado ocorreu como o esperado.
Correção/reteste ou pendência: Nenhum.

T04 — Prévia alterada depois da abertura exige nova conferência.
Previsão: abro a prévia, adiciono um suco na janela principal e confirmo. É recusado com a mensagem "A prévia ficou antiga", e o pedido continua em "montagem".
Observado: Não rodou mensagem "A prévia ficou antiga".
Correção/reteste ou pendência: 

T05 — Confirmar gera retrato com subtotal, desconto e total coerentes.
Previsão: PIX com R$ 47,00: subtotal 4700, desconto 611, total 4089. O subtotal é igual ao desconto mais o total. O estado vira "finalizado".
Observado: Resultado ocorreu como o esperado.
Correção/reteste ou pendência: Nenhum.

T06 — Pedido finalizado bloqueia mutações e segunda finalização.
Previsão: adicionar, atualizar, remover e finalizar de novo dão erro "Pedido finalizado: inicie um novo pedido." O total continua 4700.
Observado: Resultado ocorreu como o esperado.
Correção/reteste ou pendência: Nenhum.

T07 — Alterar o recibo retornado não altera o comprovante guardado.
Previsão: se eu adicionar "lixo" nos itens e zerar o total do recibo devolvido, o comprovante guardado continua com 2 itens e total 4089.
Observado: igual. Depois de mexer no recibo devolvido, o comprovante guardado continuou com 2 itens e total 4089.
Correção/reteste ou pendência: nenhuma.

T08 — Novo pedido limpa a montagem; cancelamento de descarte preserva-a.
Previsão: "Novo pedido" com itens pergunta se pode descartar. Responder "Não" mantém os itens; responder "Sim" deixa o pedido vazio, em "montagem". O comprovante antigo continua guardado.
Observado: no verificar.py, depois de novo() o pedido ficou vazio, em "montagem", e o comprovante antigo continuou com total 4089.
Correção/reteste ou pendência: pendente, testar na janela do main.py o botão Novo pedido respondendo "Não" (itens preservados) e depois "Sim" (pedido vazio).

T09 — Principal continua utilizável após fechar confirmação.
Previsão: depois de fechar a prévia, consigo adicionar, atualizar e remover na janela principal e usar o Tab normalmente.
Observado: Resultado ocorreu como o esperado.
Correção/reteste ou pendência: Nenhum.

## Explicação individual
Uma decisão que consigo justificar: o comprovante guarda uma cópia dos itens e dos valores, e o finalizar devolve outra cópia. Assim, mexer no recibo ou começar um novo pedido não muda o comprovante.
Uma dificuldade, apoio e próxima tentativa: 

## Arquivos
Versão executada e arquivos baixados: modelos.py, pagamento.py, verificar.py, main.py e este registro.
Caminho de dados fictícios usado (se houver): nenhum, o catálogo fica fixo no main.py.
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo explicar estado e versão com papéis diferentes.
Minha explicação:
o estado diz em que fase o pedido está, "montagem" ou "finalizado", e decide se ele ainda pode mudar. A versão é um número que sobe cada vez que a montagem muda, e serve para saber se a prévia ficou antiga.

Consigo distinguir confirmação explícita de cancelamento.
Minha explicação:
só o botão Confirmar chama o finalizar com confirmado=True. Cancelar, X e Escape só fecham a janela, sem finalizar e sem mexer nos itens.

Consigo justificar por que o comprovante precisa de um retrato independente.
Minha explicação:
se o comprovante usasse a mesma lista do pedido, um novo pedido ou uma mudança poderia alterar o comprovante antigo. Com uma cópia dos itens e dos valores, ele fica como estava na confirmação.

Ligação entre o ensaio e meus arquivos da atividade:
No ensaio, versao_atual é a versão do pedido e versao_da_previa é a versão que eu guardei quando abri a prévia. No meu código, a versao_atual é o self.versao do modelos.py e a versao_da_previa é o previa["versao"] do main.py. O finalizar compara as duas, igual o ensaio faz com ==.

Minha previsão antes da alteração guiada e o resultado observado:
Previsão: se eu tirar a linha versao_atual += 1, vai aparecer True, porque as versões ficam iguais. A mensagem "Reabrir prévia" vai aparecer do mesmo jeito, porque o print dela não está dentro de um if.
Observado: Apareceu a mensagem "Reabrir prévia" como o esperado.

## Continuação em casa
Arquivos/versão executados: modelos.py, pagamento.py, verificar.py e main.py da pasta A11. O verificar.py foi executado e passou. O main.py foi executado e passou.
Pasta e comando usados: pasta A11, com os comandos `python verificar.py` e `python main.py`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre estados montagem/finalizado, versão da prévia e comprovante independente:
Eu coloquei um estado no Pedido: "montagem" ou "finalizado". Depois de finalizar, não dá mais para adicionar, remover ou atualizar.
Também coloquei uma versão, que sobe quando o pedido muda. Quando abro a prévia, o main.py guarda essa versão.
Na hora de confirmar, o finalizar compara a versão guardada com a atual. Se for diferente, recusa e o pedido não muda.
O comprovante guarda uma cópia dos itens e dos valores, então não muda quando começo um novo pedido.
Esse código está no modelos.py, no método finalizar.
Minha explicação / anexo: a explicação está acima.

## Checklist da interface
Controles e rótulos que conferi: Produto (lista), Quantidade (campo), tabela com Código, Produto, Qtd e Subtotal, Estado, Forma de pagamento (lista), botões Adicionar, Atualizar, Remover, Finalizar pedido e Novo pedido.
Percurso por Tab/Shift+Tab e acionamento: pela ordem em que criei os controles, o Tab deve ir Produto > Quantidade > Tabela > Forma de pagamento → Adicionar → Atualizar → Remover → Finalizar pedido → Novo pedido. Na prévia, o foco começa em Cancelar e o Tab vai para Confirmar. Os botões devem acionar com a barra de espaço.
Mensagem após erro e possibilidade de corrigir: o erro aparece no texto de aviso e o pedido não muda. Se a prévia ficar antiga, ela fecha e o aviso pede para abrir de novo, depois é só clicar em Finalizar pedido outra vez.
Redimensionamento e comportamento que observei: pelo código, só a tabela cresce quando a janela principal aumenta, os outros controles ficam do mesmo tamanho. A prévia tem tamanho fixo. 

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
