# Meu registro A19 — Academia e demonstrações individuais

Nome/código individual, turma e data: Lucas Miranda Fernandez 14268 - 18/11/26

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Na A18, que instrução permite ao colega iniciar sem uma explicação oral? O README: os requisitos, os arquivos, o comando python main.py, onde fica o banco e como rodar o verificar.py.
- O que deve acompanhar uma correção feita na A18? Um caso vizinho testado e a nova execução, com a previsão, o observado e o que foi corrigido registrados.
- Na A15, como selecionar o alvo depois de ordenar a listagem? Pelo ID da linha, e não pela posição na tabela.
- Que evidência da A15 mostra que cancelar exclusão preservou o cadastro? A lista continua igual depois de excluir sem confirmar (no verificar.py) e, na janela, aparece "Exclusão cancelada. Nada foi apagado." com a linha ainda na tabela.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- backup_sqlite.py: criar_backup(origem, destino). Usa a API backup do sqlite3 pela conexão. Não usa Tkinter e não importa os outros módulos.
- verificar.py: testes com assert, sem janela. Usa o RepositorioSqlite para criar um banco fictício de origem numa pasta temporária.
- Os módulos modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, memoria.py, controller.py e main.py são os da A18, sem mudança.
- roteiro-demo.md: o roteiro da minha demonstração, com o fluxo válido, o erro, a persistência e o limite.
Duração dos dados: a origem e a cópia de teste ficam numa pasta temporária e somem no fim do verificar.py. A cópia é um retrato do momento do backup. Dados novos na origem não aparecem nela.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Minha demonstração apresenta uma execução e uma explicação próprias.
Previsão: eu consigo apresentar o fluxo do roteiro-demo.md (cadastrar, montar, confirmar, ver o resultado) e explicar com as minhas palavras onde está a regra e qual ID liga os registros.
Observado:
Correção/reteste ou pendência:

T02 — Demo inclui fluxo válido, falha/cancelamento e persistência/relatório.
Previsão: a demonstração mostra a venda confirmada (R$ 11,31), um cancelamento e uma recusa por preço alterado sem gravar nada, e depois fechar e abrir o programa e abrir o CSV.
Observado:
Correção/reteste ou pendência:

T03 — Pergunta técnica tem explicação individual, além da tela pronta.
Previsão: eu respondo por que a venda e os itens ficam no mesmo "with con:", apontando o repositorio.py e o caso do verificar.py (0 vendas e 0 itens depois da falha).
Observado:
Correção/reteste ou pendência:

T04 — Mapa da academia distingue entidade, responsabilidade e armazenamento observado.
Previsão: (preencher depois de ler o academia_amostra.py)
Observado:
Correção/reteste ou pendência:

T05 — Backup usa destino novo e não sobrescreve cópia anterior.
Previsão: se o destino já existe, o criar_backup dá "não será sobrescrito" e o conteúdo do destino continua igual. Isso vale também para uma cópia criada antes.
Observado:
Correção/reteste ou pendência:

T06 — Origem ausente não cria silenciosamente banco vazio.
Previsão: com a origem inexistente, dá "Origem não encontrada", o arquivo da origem não é criado e nenhuma cópia é criada.
Observado:
Correção/reteste ou pendência:

T07 — Cópia abre e contém registros conhecidos; integridade conferida.
Previsão: a cópia, aberta por outra conexão, tem os produtos Sorvete (650) e Picolé d'água (500), o cliente Maria D'Ávila e a venda ID 1 com total 1131. O PRAGMA integrity_check dá "ok". A origem continua com os mesmos bytes.
Observado:
Correção/reteste ou pendência:

T08 — Entrega exclui ambientes/caches/dados reais e documenta limites.
Previsão: eu entrego só os arquivos .py, o roteiro e o registro (e o README, se for pedido), sem .venv, sem a pasta __pycache__, sem arquivos .db com dados e sem credenciais. Os limites ficam escritos.
Observado:
Correção/reteste ou pendência:

T09 — Feedback indica evidência por indicador e teste de recuperação.
Previsão: quem me observa registra uma evidência que viu e uma pergunta. Eu anoto a pergunta e o próximo teste de recuperação (backup e consulta da cópia) a repetir.
Observado:
Correção/reteste ou pendência:

## Explicação individual
Uma decisão que consigo justificar: o criar_backup só aceita um destino novo, abre a origem só para leitura e remove uma cópia incompleta se algo falhar. Assim, o backup nunca sobrescreve dados e nunca estraga a origem.
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados: backup_sqlite.py, verificar.py, roteiro-demo.md, modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, memoria.py, controller.py, main.py e este registro.
Caminho de dados fictícios usado (se houver): origem-ficticia.db e copia-nova.db, numa pasta de ensaio. Na janela, o arquivo sorveteria_a18.db, na mesma pasta do main.py.
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo explicar uma decisão apontando código e execução.
Minha explicação: eu falo a decisão, mostro o arquivo e a linha onde ela está e mostro um caso executado. Por exemplo: o registrar_venda usa um único "with con:", e o verificar.py mostra que uma falha deixa 0 vendas e 0 itens.

Consigo distinguir existência da cópia de recuperação conferida.
Minha explicação: o arquivo da cópia existir não prova nada. Eu preciso abrir a cópia por outra conexão, conferir a integridade e consultar dados conhecidos. Só então posso dizer que a cópia serve para recuperar.

Consigo identificar origem, destino novo e consulta usada para verificar o backup.
Minha explicação: a origem é o banco fictício (origem-ficticia.db). O destino é um caminho novo (copia-nova.db) que ainda não existe. A consulta é a listagem de produtos, clientes e vendas na cópia, mais o PRAGMA integrity_check.

Ligação entre o ensaio e meus arquivos da atividade: no ensaio, origem.backup(copia) copia pela conexão e depois consulto a cópia. No meu backup_sqlite.py, o con_origem.backup(con_destino) faz o mesmo, e no verificar.py eu abro a cópia por outro repositório para consultar.

Minha previsão antes da alteração guiada e o resultado observado:
Previsão: se eu acrescentar outra linha na origem antes do backup, a cópia terá 2 linhas. Se eu acrescentar a linha depois do backup, a cópia continua com 1 linha, porque ela é um retrato do momento da cópia.
Observado:

## Continuação em casa
Arquivos/versão executados: backup_sqlite.py, verificar.py, modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, memoria.py, controller.py e main.py da pasta A19.
Pasta e comando usados: pasta A19, com os comandos `python verificar.py`, `python backup_sqlite.py origem-ficticia.db copia-nova.db` (numa pasta de ensaio) e `python main.py`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre demonstração sustentada por evidências, comparação de responsabilidades e backup conferido:
No backup_sqlite.py, eu só crio a cópia se a origem existir e se o destino ainda não existir.
A cópia é feita pela API backup, com a origem aberta só para leitura, e não copiando o arquivo "na mão".
Depois da cópia, o programa abre o destino de novo e confere o integrity_check. Se falhar, apaga a cópia incompleta.
No verificar.py, eu consulto dados conhecidos na cópia, e não confio só no arquivo existir.
Na demonstração, eu falo de cada parte do fluxo com uma evidência e digo o que ainda não conferi.
Esse código está no backup_sqlite.py e no verificar.py.
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
