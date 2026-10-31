# A05 — organização e consultas do sistema escolar

Código do estudante: 
Arquivos e interpretador executados: escolar_grupos.py e escolar_janelas.py; versão: Python 3.10.11
## Retomada sem consulta
Quais dados devem ficar juntos no último registro válido?
Nome, turma, a lista das cinco notas numéricas e a média, todos da mesma tentativa confirmada.

Por que uma quinta nota inválida não pode alterar o nome confirmado?
Porque o registro só é atualizado depois de validar tudo. Se o nome novo entrasse antes da nota falhar, o registro mostraria um nome de uma tentativa e notas de outra.

O que o botão recebe em command e quando essa função é executada?
Minhas respostas iniciais: 
Recebe a própria função, sem parênteses. Ela só é executada quando o usuário clica. Com parênteses, a função rodaria na hora em que o botão é criado e o botão receberia o resultado dela.

## Antes de programar
Desenho dos pais: Tk → Frame base → grupos → campos e botões:
Tk → base (Frame) → Identificação (LabelFrame) → rótulos e Entry de nome e turma, base → Notas (LabelFrame) → rótulos e as cinco Entry, base → Ações (Frame) → os três botões, base → rótulos de aviso e resultado. O primeiro argumento de cada widget é o seu grupo.

Onde cada grid organiza seus filhos?
A base organiza os grupos em linhas (título, Identificação, Notas, Ações, aviso, resultado). Cada grupo tem a sua própria grade: nome e turma nas linhas 0 e 1 da Identificação, as notas nas linhas 0 a 4 de Notas; os botões nas linhas 0 e 1 de Ações. A coluna de entrada de cada grupo recebe weight=1 para crescer.

Diferença entre edição, registro confirmado e retrato da consulta:
Edição são os textos nas Entry, que podem ser qualquer coisa. O registro confirmado é o último conjunto válido. O retrato é uma cópia dos textos do confirmado criada no instante em que a consulta abre, não acompanha mudanças posteriores.

## Preveja e depois execute
Dados sempre fictícios. C1/C2 identificam janelas de consulta diferentes.
Observações feitas por simulação de cliques com um display virtual (sem janela real). Tab/Shift+Tab e aparência: [conferir no seu computador].
| Caso | Sequência/verificação | Previsão | Observação | Ajuste |
|---|---|---|---|---|
| T01 | Confirmar que nome/turma, cinco notas e ações possuem os grupos/pais planejados | Entradas de nome/turma e de notas em LabelFrames diferentes; botões num Frame | Grupos "Identificação" e "Notas (0 a 10)"; nome/turma e notas em LabelFrames distintos; botões no Frame de ações | Nenhum |
| T02 | Lia / T1 / 6,7,8,9,10; calcular e conferir média 8.0 | "Registro confirmado." e média 8.0 | Igual à previsão | Nenhum |
| T03 | Antes do primeiro válido, usar Consultar | Orienta a calcular e não abre janela | "Calcule uma média válida antes de consultar." e 0 janelas abertas | Nenhum |
| T04 | Confirmar T02 e abrir consulta C1 | C1 mostra Lia / T1 / notas / média 8.0 | C1 abriu com Lia, T1, 6.0 a 10.0 e média 8.0 | Nenhum |
| T05 | Editar Rui / T2 / cinco notas 5, sem calcular; observar C1 | C1 continua com Lia | C1 não mudou | Nenhum |
| T06 | Após T02, tentar outra identificação com quinta nota abc; consultar novamente | Erro na nota 5; a nova consulta ainda mostra Lia | "Nota 5: informe um número." e a nova consulta mostrou Lia | Nenhum |
| T07 | Corrigir e confirmar Rui / T2 / cinco notas 5; observar C1 e abrir C2 | C1 mantém Lia; C2 mostra Rui com média 5.0 | C1 manteve Lia; a nova consulta mostrou Rui, 5.0 | Nenhum |
| T08 | Limpar as sete entradas; observar o registro principal e as consultas | Sete entradas vazias; registro e consultas intactos | Entradas vazias; C1 continuou aberta e o painel manteve o último registro | Nenhum |
| T09 | Fechar C1 pelo botão; continuar usando a principal e C2 | Só C1 some | Restou 1 consulta e a principal continuou funcionando | Nenhum |
| T10 | Abrir outra consulta e fechá-la por Escape | Só essa consulta fecha | Fechou; a outra consulta e a principal seguiram abertas | Nenhum |
| T11 | Abrir outra consulta e fechá-la pelo X da própria janela | Só essa consulta fecha | Fechou pelo protocolo do X (WM_DELETE_WINDOW); principal intacta | Nenhum (conferir o X real na sua janela) |
| T12 | Repetir 0/10, fora de faixa, vazios, vírgula/ponto e identificação da A04 | Mesmas respostas da A04 | A lógica é a da A04 (testada em medias.py): mesmas mensagens | Nenhum (repetir na janela) |
| T13 | Percorrer grupos e botões por Tab/Shift+Tab; ampliar a janela e observar campos | Ordem nome, turma, notas, botões; entradas crescem | Ao ampliar a janela, as entradas ficaram mais largas. |  |
| T14 | Executar sem marca-a05.png; observar o cabeçalho textual | Texto "Sistema escolar fictício — A05" | Texto mantido, sem imagem | Nenhum |
| T15 | Se usar PNG próprio, conferir imagem e testar arquivo inválido/ausente com fallback | Imagem aparece com PNG válido; inválido/ausente mantém o texto | Com um PNG de teste válido, a imagem apareceu junto do texto; com arquivo inválido e ausente, ficou só o texto | Nenhum |
| T16 | Executar o script a partir de outra pasta; conferir busca ao lado do script | A imagem é achada ao lado do script | Executado de outra pasta, a imagem foi achada | Nenhum |
| T17 | Fechar a principal com consultas abertas; reabrir e tentar Consultar | Consultas fecham junto; ao reabrir não há registro | Reaberta, a janela voltou sem registro e Consultar orientou, sem abrir janela | Nenhum |

## Imagem local (opcional)
O programa funcionou sem imagem: sim; o texto do cabeçalho permaneceu.
Se criei PNG próprio, nome/origem do arquivo e teste realizado:
Qual objeto conserva a referência da imagem:

## Fechamento sem consulta
Por que criar outra Tk/mainloop não é o contrato desta aula?
Uma aplicação Tkinter tem uma Tk e um mainloop. A consulta é uma Toplevel ligada à principal: compartilha o mesmo laço de eventos e fecha junto com ela. Outra Tk seria uma segunda aplicação, com outro laço, sem relação com a principal.

Por que C1 pode manter o registro antigo depois de um novo válido?
Porque C1 é um retrato: os textos foram criados no instante em que ela abriu e não consultam mais o registro. Só uma nova consulta (C2) lê o confirmado mais recente.

Qual janela cada fechamento destrói?
Botão, X e Escape destroem somente a Toplevel da consulta. Fechar a principal encerra a aplicação e, junto, as consultas.
Minha dificuldade, correção e próxima tentativa: 

Entregas: escolar_grupos.py, escolar_janelas.py e este registro.
Não há imagem obrigatória no pacote; use apenas arquivo próprio autorizado se optar por esse teste.

## Teoria e transferência
Consigo identificar o pai e a grade de um campo.
Minha explicação:
Consigo explicar sticky e peso de coluna no redimensionamento.
Minha explicação:
Consigo distinguir edição, confirmado e retrato da consulta.
Minha explicação:
Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre hierarquia de pais, expansão dos grupos, retratos e fechamento das Toplevel:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
