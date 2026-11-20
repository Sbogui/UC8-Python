# Meu registro A17 — Sorveteria integrada e comparação visual

Nome/código individual, turma e data: Lucas Miranda Fernandez 14268 - 19/11/26

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Na A16, quais valores devem chegar ao controller em vez dos widgets? Os valores já lidos da tela: o nome, o preço digitado, o ID escolhido e se a pessoa confirmou. Não os campos (Entry) nem a tabela (Treeview).
- Como o mesmo fluxo da A16 pode usar memória e SQLite? O controller usa um repositório com os mesmos métodos. Dá para trocar o RepositorioMemoria pelo RepositorioSqlite sem mudar o fluxo.
- Por que o CSV da A13 usa um retrato da finalização? Para o relatório mostrar o que foi confirmado e não mudar se o pedido mudar depois.
- A escolha de perfil na simulação da A13 comprova identidade? Não. Ela só guarda o nome e o perfil que eu escolhi. Não prova quem eu sou.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- repositorio.py: acesso ao SQLite (produtos, clientes, vendas e itens da venda). O iniciar_vendas também cria as tabelas de produtos e clientes. Não usa Tkinter.
- controller.py: CadastroController (listar, salvar, excluir) e VendaController (confirmar). A janela chama o controller e o controller chama o repositório.
- memoria.py: o mesmo contrato do repositório, só que na memória.
- modelos.py, pagamento.py, relatorios.py, perfis.py e arquivos.py: os módulos de antes.
- verificar.py: testes com assert, sem janela. Usa um banco numa pasta temporária.
- main.py: a janela com as abas Pedido, Produtos, Clientes, Perfil e Exercício JSON.
- comparar_ctk.py: comparação opcional com CustomTkinter.
O catálogo, os clientes e as vendas ficam no banco e continuam depois de fechar. O pedido em montagem fica só na memória.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Catálogo/clientes vêm do banco por ID, inclusive após reabrir.
Previsão: um RepositorioSqlite novo, com o mesmo caminho, lista os produtos (1, "Sorvete", 650) e (2, "Picolé", 500) e o cliente (1, "Maria D'Ávila").
Observado:
Correção/reteste ou pendência:

T02 — Cadastro novo aparece após atualização explícita.
Previsão: um produto cadastrado depois de a lista ser consultada não aparece sozinho na lista que já estava na tela (2 produtos). Depois de consultar de novo, aparecem 3.
Observado:
Correção/reteste ou pendência:

T03 — Preço mudou ou produto sumiu: recusar confirmação sem venda parcial.
Previsão: se o preço mudar (650 para 700), se o nome mudar ou se o produto for excluído, confirmar dá erro ("mudou" ou "não existe mais"). Nenhuma venda é gravada e a montagem continua com os itens.
Observado:
Correção/reteste ou pendência:

T04 — Cliente inexistente ou não selecionado: orientar.
Previsão: sem cliente selecionado aparece "Selecione um cliente antes de confirmar.". Com o cliente 99 aparece "Cliente ID 99 não foi encontrado.". Nos dois casos nenhuma venda é gravada e o pedido continua em montagem.
Observado:
Correção/reteste ou pendência:

T05 — Venda de duas unidades a 6,50 no PIX: 13,00 →11,31.
Previsão: subtotal 1300, desconto 169 e total 1131 centavos (R$ 11,31).
Observado:
Correção/reteste ou pendência:

T06 — Falha na segunda inserção desfaz venda e itens.
Previsão: gravar a venda com o mesmo produto duas vezes falha na segunda inserção. Dá o erro "Nada foi salvo" e ficam 0 vendas e 0 itens.
Observado:
Correção/reteste ou pendência:

T07 — Sucesso grava uma venda e bloqueia nova finalização.
Previsão: a venda com 2 sorvetes grava 1 venda e 1 item, e o pedido vira "finalizado". Confirmar de novo é recusado e continua 1 venda.
Observado:
Correção/reteste ou pendência:

T08 — Excluir cadastro vinculado é bloqueado.
Previsão: excluir o cliente 1 ou o produto 1, que já estão ligados a uma venda, dá erro "ligado a vendas". O cliente e a venda continuam no banco.
Observado:
Correção/reteste ou pendência:

T09 — CSV usa o comprovante confirmado e mantém totais.
Previsão: o CSV tem id 1, quantidade 2, subtotal 1300 e total 11,31. Isso continua assim mesmo depois de começar um novo pedido com outro produto.
Observado:
Correção/reteste ou pendência:

T10 — Comparação ttk/CTk documenta teclado/foco; ausência da dependência não bloqueia núcleo.
Previsão: sem o CustomTkinter instalado, o comparar_ctk.py mostra "CustomTkinter não está instalado: comparação não executada." e termina. O main.py continua funcionando.
Observado:
Correção/reteste ou pendência:

## Explicação individual
Uma decisão que consigo justificar: no registrar_venda, a conferência do catálogo, a venda e todos os itens ficam dentro do mesmo "with con:". Assim, se qualquer item falhar, o banco desfaz tudo e não fica uma venda pela metade.
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados: modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, memoria.py, controller.py, verificar.py, main.py, comparar_ctk.py e este registro.
Caminho de dados fictícios usado (se houver): o banco de teste do verificar.py fica numa pasta temporária. Na janela, o arquivo sorveteria_a17.db, na mesma pasta do main.py.
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo explicar por que venda e itens precisam da mesma transação.
Minha explicação: porque a venda e os itens formam um conjunto. Se gravasse a venda e um item falhasse, ficaria uma venda sem itens ou com itens faltando. Na mesma transação, ou grava tudo ou não grava nada.

Consigo prever banco e montagem após uma falha no item.
Minha explicação: o banco continua sem a venda (0 vendas e 0 itens) e a montagem continua com os itens, porque o pedido só é finalizado depois que a gravação terminou com sucesso. A tela não mostra sucesso.

Consigo distinguir o núcleo integrado da comparação visual opcional.
Minha explicação: o núcleo é a janela ttk com o banco, o pedido, a venda e o CSV, e ele precisa funcionar sozinho. O CustomTkinter é só uma comparação opcional depois. Se ele não estiver instalado, o núcleo não é bloqueado.

Ligação entre o ensaio e meus arquivos da atividade: no ensaio, as duas inclusões ficam no mesmo "with con:" e a segunda repete o ID. Isso dá erro e a contagem fica 0. No meu repositorio.py, a venda e os itens ficam no mesmo "with con:", e repetir o mesmo produto quebra a regra UNIQUE (venda_id, produto_id), então tudo é desfeito.

Minha previsão antes da alteração guiada e o resultado observado:
Previsão: se eu trocar o segundo ID para 2, não dá erro. As duas linhas são gravadas, a contagem é 2 e não aparece "Grupo desfeito".
Observado: 

## Continuação em casa
Arquivos/versão executados: modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, memoria.py, controller.py, verificar.py e main.py da pasta A17.
Pasta e comando usados: pasta A17, com os comandos `python verificar.py` e `python main.py`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre transação venda/itens, rollback, IDs vinculados e coerência com o catálogo:
Eu gravo a venda e todos os itens dentro do mesmo "with con:", então uma falha desfaz o conjunto (rollback) e não sobra venda pela metade.
O pedido só é finalizado depois que o banco gravou com sucesso, e por isso a montagem não se perde se der erro.
Antes de gravar, eu comparo o nome e o preço de cada item com o cadastro atual. Se algo mudou ou o produto sumiu, peço para revisar.
Os vínculos usam IDs (cliente_id e produto_id), e o banco confere isso porque eu ligo o foreign_keys em cada conexão.
Por isso não dá para excluir um cliente ou produto que já tem venda.
Esse código está no repositorio.py (registrar_venda) e no controller.py (VendaController).
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
