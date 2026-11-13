# Meu registro A16 — Controllers e contratos: concluir clientes

Nome/código individual, turma e data:
Lucas Miranda Fernandez, 14268 - 13/11/2026

## Retomada sem consulta
Minha hipótese inicial para cada item:


## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Controller executa sem importar Tkinter.
Previsão: importar o controller, o repositório e a memória não carrega o tkinter.
Observado: 
Correção/reteste ou pendência:

T02 — Mesmo contrato com memória/SQLite inclui, lista e edita por ID.
Previsão: o mesmo cenário dá o mesmo resultado nas duas: IDs 1 e 2, depois editar o ID 1 e a lista fica [(1, "Sorvete de creme", 1500), (2, "Picolé", 500)].
Observado: 
Correção/reteste ou pendência:

T03 — Memória começa vazia numa nova instância; SQLite reabre com dados.
Previsão: um RepositorioMemoria novo lista tudo vazio. Um RepositorioSqlite novo, com o mesmo caminho, lista os dados que foram gravados.
Observado:
Correção/reteste ou pendência:

T04 — Editar/excluir clientes mantém alvo por ID.
Previsão: editar o cliente de ID 2 muda só esse nome ("João Pedro"). Excluir o ID 1 apaga só ele e sobra o ID 2.
Observado:
Correção/reteste ou pendência:

T05 — Cancelar exclusão de cliente não altera banco nem lista.
Previsão: excluir sem confirmar dá o erro "Confirme a exclusão para apagar o cliente." e a lista continua igual. Na janela, responder "Não" mostra "Exclusão cancelada. Nada foi apagado."
Observado:
Correção/reteste ou pendência:

T06 — Tipo de cadastro desconhecido é rejeitado.
Previsão: tipos como "fornecedor", vazio, None ou um texto com SQL dão ValueError em listar, salvar e excluir.
Observado:
Correção/reteste ou pendência:

T07 — Falha do repositório é comunicada e conserva formulário.
Previsão: com um repositório que falha, o controller deixa o ValueError subir (não devolve lista vazia nem sucesso). Na janela aparece a mensagem de erro e os campos continuam preenchidos.
Observado:
Correção/reteste ou pendência:

T08 — Cópia retornada pela memória não permite alterar o armazenamento por fora.
Previsão: se eu acrescentar um item ou limpar a lista que listar_produtos devolveu, o armazenamento continua com os mesmos produtos.
Observado:
Correção/reteste ou pendência:

T09 — Componentes mantêm campos/seleções independentes.
Previsão: selecionar um produto preenche só os campos da aba Produtos. A aba Clientes continua com os seus campos e a sua seleção. O cliente não tem campo de preço.
Observado:
Correção/reteste ou pendência:

## Explicação individual
Uma decisão que consigo justificar:
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados:
Caminho de dados fictícios usado (se houver):
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo seguir uma chamada da interface ao controller e ao repositório.
Minha explicação:
Consigo descrever o contrato e o que fica igual nas duas implementações.
Minha explicação:
Consigo distinguir a duração dos dados em memória e SQLite.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre controller, contrato de repositório, componentes e conclusão do CRUD de clientes:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
