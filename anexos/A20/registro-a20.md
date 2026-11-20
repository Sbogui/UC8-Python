# Meu registro A20 — Vínculos, recuperação e entrega final

Nome/código individual, turma e data: Lucas Miranda Fernandez 14268 - 19/11/26

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Na A19, criar um arquivo de backup basta para demonstrar recuperação? Não. Recuperar é tentar o requisito de novo, com outra entrada ou outra sequência, e explicar com as minhas palavras. O backup sozinho não mostra que eu entendi.
- Qual foi o papel da pergunta técnica individual na A19? Mostrar que eu entendo o que fiz: a resposta aponta uma regra, um arquivo e um caso que eu observei.
- Na A16, um contrato de repositório depende obrigatoriamente de herança? Não. O contrato é o conjunto de métodos e comportamentos que o repositório promete. Não precisa de uma classe-mãe.
- Por que a exclusão de clientes da A16 precisa manter identidade e confirmação separadas? O ID diz qual cliente será afetado, e a confirmação é a escolha explícita da pessoa. Se juntar os dois, uma seleção errada ou um clique sem querer pode apagar o cadastro errado.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- vinculos.py: validar_vinculos e pode_excluir_aluno. Trabalha com listas de dicionários em memória e não usa Tkinter nem banco.
- relacoes_sqlite.py: demonstrar(). Usa bancos temporários na memória, com chave estrangeira e ON DELETE RESTRICT.
- verificar.py: testes com assert, sem janela. Importa o vinculos.py e o relacoes_sqlite.py.
- entrega-final.md: o documento da entrega, com inventário, evidências, recuperação e limites.
Os dados da A20 são fictícios e só existem durante a execução. Os bancos da demonstração ficam na memória e somem quando o programa termina.
Os IDs que ligam as coisas: a matrícula guarda aluno_id (que aponta para o id do aluno) e plano_id (que aponta para o id do plano).

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Vínculos válidos não apontam para IDs inexistentes.
Previsão: com aluno 41, plano 7 e uma matrícula ligando os dois, validar_vinculos devolve uma lista vazia. Mudar só o nome do aluno para "Lia Silva" continua devolvendo lista vazia.
Observado:
Correção/reteste ou pendência:

T02 — Aluno/plano ausente é identificado sem alterar dados.
Previsão: uma matrícula com aluno_id 92 e plano_id 99 gera 2 problemas ("o aluno 92 não existe" e "o plano 99 não existe"). As listas de alunos, planos e matrículas ficam iguais antes e depois.
Observado:
Correção/reteste ou pendência:

T03 — IDs duplicados/booleanos/negativos são recusados.
Previsão: ID repetido, True, -3, 0 e "5" (texto) geram problemas. Uma matrícula com aluno_id True ou plano_id -7 também.
Observado:
Correção/reteste ou pendência:

T04 — Aluno com matrícula não pode ser excluído pelo contrato.
Previsão: pode_excluir_aluno(41, matriculas) dá False. Um aluno sem matrícula (55) dá True. Código True ou -1 dá False.
Observado:
Correção/reteste ou pendência:

T05 — SQLite bloqueia exclusão vinculada com foreign_keys habilitado.
Previsão: com PRAGMA foreign_keys = ON, excluir o aluno 1 que tem matrícula dá IntegrityError, e inserir matrícula com aluno 99 também. Sem ligar o foreign_keys, o banco aceita a referência órfã.
Observado:
Correção/reteste ou pendência:

T06 — Erro de integridade não apaga aluno/matrícula.
Previsão: depois dos erros, o aluno 1 e a matrícula 1 continuam lá (1 aluno e 1 matrícula). Depois da correção (apagar a matrícula primeiro), a exclusão do aluno funciona.
Observado:
Correção/reteste ou pendência:

T07 — Recuperação liga dificuldade, apoio, nova tentativa e evidência individual.
Previsão: eu descrevo a dificuldade (o relatorios.py com conteúdo de outro arquivo e o erro de import circular), o apoio recebido, uma nova tentativa feita por mim (refazer o arquivo certo e rodar `python verificar.py`) e o resultado que eu vi.
Observado:
Correção/reteste ou pendência:

T08 — Entrega executa em outra pasta por README.
Previsão: copiando a pasta A15 inteira para outro lugar, `python verificar.py` passa e `python main.py` cria o banco na pasta nova, porque o caminho vem da pasta do main.py e não de um caminho absoluto.
Observado:
Correção/reteste ou pendência:

T09 — Pendência não é registrada como sucesso nem gera nota inventada.
Previsão: o que eu não executei fica escrito como "pendente" no registro e no entrega-final.md, sem "ok" e sem nota.
Observado:
Correção/reteste ou pendência:

T10 — Arquivos executados/exportados conferidos e cópia local preservada.
Previsão: eu abro cada arquivo e confiro que o conteúdo bate com o nome (por exemplo, o relatorios.py sem código do repositorio.py), guardo uma cópia local e só depois envio ao OneDrive.
Observado:
Correção/reteste ou pendência:

## Explicação individual
Uma decisão que consigo justificar: o validar_vinculos só confere e devolve uma lista de problemas, sem mexer nos dados. No SQLite usei ON DELETE RESTRICT e não CASCADE, para o banco recusar a exclusão em vez de apagar as matrículas e esconder o problema.
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados: vinculos.py, relacoes_sqlite.py, verificar.py, entrega-final.md e este registro, da pasta A20. Também a pasta A15 da pizzaria.
Caminho de dados fictícios usado (se houver): os bancos da demonstração ficam na memória. O banco da pizzaria é o pizzaria_a15.db, na pasta do main.py.
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo explicar quais IDs ligam aluno, plano e matrícula.
Minha explicação: a matrícula guarda o aluno_id, que aponta para o id do aluno, e o plano_id, que aponta para o id do plano. Mudar o nome do aluno não muda o ID, então o vínculo continua.

Consigo prever o efeito de referência ausente e exclusão de cadastro vinculado.
Minha explicação: se a matrícula aponta para um aluno que não existe, ela é uma referência órfã e deve ser recusada. Se eu tento excluir um aluno que ainda tem matrícula, a exclusão é bloqueada e todos os registros continuam como estavam.

Consigo relacionar uma correção a evidência nova e a um limite da entrega.
Minha explicação: depois de corrigir, eu repito o caso com outra entrada ou sequência e anoto o que eu vi. O limite é o que eu ainda não consegui conferir, como outro computador ou a janela, e isso fica escrito como pendente.

Ligação entre o ensaio e meus arquivos da atividade: o ensaio tem a função vinculo_existe, que confere se o aluno_id e o plano_id estão nos IDs conhecidos. O meu validar_vinculos faz a mesma conferência para todas as matrículas e também recusa IDs repetidos, True, negativos e em texto.

Minha previsão antes da alteração guiada e o resultado observado:
Previsão: se eu mudar só o nome do aluno de "Lia" para "Lia Silva", o vínculo continua válido (Após nome: True), porque o vínculo usa o ID.
Observado: (preencher depois de rodar o ensaio.py)

## Continuação em casa
Arquivos/versão executados: vinculos.py, relacoes_sqlite.py e verificar.py da pasta A20.
Pasta e comando usados: pasta A20, com os comandos `python verificar.py`, `python vinculos.py` e `python relacoes_sqlite.py`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre vínculos por ID, referências órfãs, chave estrangeira/RESTRICT e revalidação da entrega:
Eu ligo as matrículas aos alunos e planos só pelo ID, e nunca pelo nome ou pela posição na lista.
O validar_vinculos recusa referência órfã e ID repetido, True, negativo ou em texto, e não altera nenhum dado.
O pode_excluir_aluno impede excluir quem ainda tem matrícula.
Isso fica no código que executa a operação, e não só no botão da tela.
No SQLite eu liguei o foreign_keys em cada conexão e usei ON DELETE RESTRICT, então o próprio banco recusa o que deixaria uma referência órfã.
Depois de corrigir, eu repito o caso com outra entrada e anoto só o que eu vi.
Esse código está no vinculos.py e no relacoes_sqlite.py.
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
