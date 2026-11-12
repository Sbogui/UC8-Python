# Meu registro A13 — CSV de vendas e simulação de perfis

Nome/código individual, turma e data:
Lucas Miranda Fernandez, 14268 - 12/11/2026

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Na A12, arquivo ausente e arquivo JSON inválido representam a mesma situação? 
Não. Por que quando ausente quer dizer que o catálogo ainda não foi criado, e a leitura devolve lista vazia. Inválido quer dizer que o arquivo existe mas tem erro.. vai mostrar a mensagem e o arquivo fica como estava.
- Por que um JSON que decodifica ainda precisa de validação de estrutura? Porque ele pode estar escrito certo e ter id repetido, nome vazio ou preço em texto.
- Na A09, como remover o último item do carrinho sem criar erro de seleção? Remove pelo código da linha selecionada. Se a tabela ficar vazia, não existe linha selecionada e o programa só mostra o aviso "Selecione uma linha".
- Qual informação da A09 permanece estável quando a ordem visual muda? O código (ID) do produto.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
- modelos.py, pagamento.py e arquivos.py: iguais aos da A12.
- relatorios.py: exportar_csv. Recebe o comprovante e o caminho. Não usa Tkinter e não lê a janela.
- perfis.py: SessaoDemo (entrar, pode_configurar, sair). Só simula, não autentica.
- verificar.py: testes com assert, sem janela. Usa pasta temporária para os CSV de teste.
- main.py: a janela com as abas Pedido, Perfil (simulação) e Exercício JSON, o botão Exportar CSV e o menu. Importa todos os módulos.
O pedido e a sessão existem só enquanto a janela está aberta. O CSV só vira arquivo quando eu clico em Exportar CSV e escolho onde salvar.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Sem comprovante não exporta venda fictícia.
Previsão: exportar_csv com comprovante None dá ValueError "Finalize o pedido antes de exportar o relatório." e o arquivo não é criado. Na janela só aparece o aviso e o seletor nem abre.
Observado: igual no módulo. Deu a mensagem "Finalize o pedido antes de exportar o relatório." e o arquivo não foi criado.
Correção/reteste ou pendência: Nenhuma.

T02 — CSV conserva acentos e nome com separador/aspas ao ler de volta.
Previsão: o nome Picolé; edição "verão" volta igual na leitura com DictReader. O arquivo começa com o BOM do UTF-8.
Observado: igual. O arquivo começa com o BOM. 
Correção/reteste ou pendência: nenhuma.

T03 — Quantidade, centavos e total seguem o cabeçalho documentado.
Previsão: o cabeçalho é id;nome;quantidade;preco_centavos;subtotal_centavos;forma;total_pedido_reais. Para 2 picolés de 500 e 1 pizza de 3500: quantidade 2, preço 500, subtotal 1000 e 3500. O total do pedido é 39,15 em PIX, nas duas linhas.
Observado: igual. O cabeçalho saiu como previsto. A primeira linha deu BB09, 2, 500, 1000, PIX, 39,15 e a segunda deu PZ01, 1, 3500, 3500, PIX, 39,15.
Correção/reteste ou pendência: nenhuma.

T04 — Relatório vem do retrato confirmado, não de Entry atuais.
Previsão: depois de começar um novo pedido com 3 sucos, exportar o comprovante antigo gera o mesmo CSV de antes, sem o suco.
Observado: igual. Depois do novo pedido com 3 sucos, o CSV do comprovante antigo ficou idêntico ao anterior (mesmos bytes) e não tem "Suco".
Correção/reteste ou pendência: nenhuma.

T05 — Cancelar seletor preserva pedido e arquivo.
Previsão: se eu cancelar o seletor do Exportar CSV, o pedido e o comprovante ficam iguais, nenhum arquivo é criado e não aparece mensagem de sucesso.
Observado: não executado. 
Correção/reteste ou pendência: Nenhuma.

T06 — Falha de escrita não anuncia sucesso nem substitui o destino anterior.
Previsão: comprovante sem itens, pasta inexistente e destino que é uma pasta dão ValueError. O relatório anterior continua com os mesmos bytes e não sobra arquivo .tmp.
Observado: igual. Comprovante sem itens deu "O comprovante não tem itens para exportar.". Pasta inexistente e destino que é uma pasta deram "Não foi possível exportar. O relatório anterior foi mantido.". O relatório anterior ficou com os mesmos bytes e não sobrou arquivo .tmp.
Correção/reteste ou pendência: Nenhuma.

T07 — Simulação Caixa não permite configuração no contrato de demonstração.
Previsão: sem sessão e com Caixa, pode_configurar dá False. Com Administração dá True. Na janela, a aba Exercício JSON fica desativada para Caixa, e Carregar e Salvar também recusam.
Observado: no módulo, igual: sem sessão deu False, Caixa deu False e Administração deu True.
Correção/reteste ou pendência: Nenhuma.

T08 — Sair limpa sessão fictícia; não é exclusão de vendas.
Previsão: depois de sair, nome e perfil ficam vazios e pode_configurar dá False. O comprovante continua guardado, com total 3915 centavos.
Observado: igual. Depois de sair, nome e perfil ficaram vazios (None), pode_configurar deu False e o comprovante continuou com total 3915.
Correção/reteste ou pendência: Nenhuma.

T09 — Núcleo da pizzaria mantém ID, cancelamento, totais e confirmação.
Previsão: pizza de 3500 mais 2 refrigerantes de 600 dá 4700. Finalizar no PIX dá total 4089 e o estado vira "finalizado". Cancelar a prévia continua só fechando a janela.
Observado: o total deu 4700, finalizar no PIX deu 4089 e o estado ficou "finalizado".
Correção/reteste ou pendência: Nenhuma.

## Explicação individual
Uma decisão que consigo justificar: o exportar_csv usa só o comprovante confirmado e deixa o módulo csv cuidar das aspas. Assim, um nome com ponto e vírgula não quebra as colunas e o relatório não mistura outra montagem.
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados: modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, verificar.py, main.py e este registro.
Caminho de dados fictícios usado (se houver): os CSV de teste do verificar.py ficam numa pasta temporária. Na janela, o CSV fictício que eu escolher salvar.
Entrega pelo fluxo combinado conferida por mim:

## Teoria e transferência
Consigo explicar a origem dos dados exportados.
Minha explicação: os dados vêm do comprovante confirmado do pedido, e não dos campos que estão na janela naquele momento.

Consigo conferir CSV lendo nomes e valores de volta.
Minha explicação: eu leio o arquivo com csv.DictReader, com o mesmo separador (;) e a mesma codificação da escrita, e comparo o nome, a quantidade e os valores com o comprovante.

Consigo distinguir identificação, autenticação e autorização e os limites da simulação.
Minha explicação: identificação é dizer o nome. Autenticação é provar que a pessoa é quem diz. Autorização é decidir o que ela pode fazer. A simulação só guarda o nome e o perfil que eu escolho, não prova nada e não protege de verdade. Esconder a aba ou o botão não basta, por isso o Carregar e o Salvar JSON também conferem a permissão.

Ligação entre o ensaio e meus arquivos da atividade: o ensaio escreve com csv.writer e delimiter=";" e lê com DictReader. No meu relatorios.py eu escrevo com csv.writer e delimiter=";", e no verificar.py eu leio de volta com DictReader.

Minha previsão antes da alteração guiada e o resultado observado:
Previsão: se eu acrescentar aspas ao nome do ensaio, a leitura vai devolver o nome completo, com as aspas. O csv escreve as aspas duplicadas e tira de volta ao ler.
Observado: (preencher depois de rodar o ensaio.py)

## Continuação em casa
Arquivos/versão executados: modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, verificar.py e main.py da pasta A13.
Pasta e comando usados: pasta A13, com os comandos `python verificar.py` e `python main.py`.
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre CSV do comprovante, leitura de volta, codificação e distinção entre identificação/autenticação/autorização:
O exportar_csv recebe o comprovante confirmado e usa o módulo csv, em vez de juntar texto com ponto e vírgula.
Isso evita que um nome como Picolé; edição "verão" quebre as colunas.
Eu gravo em UTF-8 com BOM, para os acentos aparecerem certos em ferramentas como o Excel.
O verificar.py lê o arquivo de volta com DictReader e compara nome, quantidade e total.
Se a escrita falhar, o relatório anterior continua, porque só troco o arquivo no final.
No perfis.py, a SessaoDemo só guarda nome e perfil escolhidos: é identificação simulada, não autenticação.
Esse código está no relatorios.py e no perfis.py.
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi: abas "Pedido", "Perfil (simulação)" e "Exercício JSON" (desativada até entrar como Administração), e o menu "Ir para". Na aba Pedido: Produto (lista), Quantidade (campo), tabela com Código, Produto, Qtd e Subtotal, Estado, Forma de pagamento (lista) e os botões Adicionar, Atualizar, Remover, Finalizar pedido, Novo pedido e Exportar CSV. Na aba Perfil: Nome fictício (campo), Perfil (lista), a situação da sessão e os botões Entrar e Sair. Conferi pelo código; falta ver na janela aberta.
Percurso por Tab/Shift+Tab e acionamento: pela ordem em que criei os controles, na aba Pedido o Tab deve ir Produto → Quantidade → Tabela → Forma de pagamento → Adicionar → Atualizar → Remover → Finalizar pedido → Novo pedido → Exportar CSV, e o Shift+Tab volta. Na aba Perfil deve ir Nome → Perfil → Entrar → Sair. Os botões devem acionar com a barra de espaço. Pendente: confirmar na janela.
Mensagem após erro e possibilidade de corrigir: o erro aparece no texto de aviso da aba. Se a exportação falhar, o pedido e o comprovante continuam e dá para tentar de novo. Se o perfil ou o nome for recusado, a sessão anterior não muda. Pendente: confirmar na janela.
Redimensionamento e comportamento que observei: pelo código, ao aumentar a janela as abas crescem e a tabela da aba Pedido e o editor da aba Exercício JSON também. Os outros controles ficam do mesmo tamanho. Pendente: confirmar na janela.

## Pendências
O que não executei e por quê, incluindo falta de ambiente: não abri a janela do main.py, então faltam o T05, a parte da janela dos T01, T07, T08 e T09, o seletor de arquivo do Exportar CSV, o Tab/Shift+Tab e o redimensionamento. O verificar.py foi executado e cobre os módulos.
Caso para nova tentativa em sala: abrir o CSV no Excel e conferir os acentos e as colunas.
