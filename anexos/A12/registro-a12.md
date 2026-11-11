# Meu registro A12 — Mercado: navegação e catálogo em JSON

Nome/código individual, turma e data:
Lucas Miranda Fernandez, 14268 - 10/11/2026

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Na A11, fechar a prévia pelo X finaliza o pedido? Não. Pois o X só fecha a janela. Só o botão Confirmar finaliza!
- O que deve ocorrer se o pedido mudar depois de abrir uma prévia na A11? A versão do pedido muda, então a confirmação é recusada e eu preciso abrir a prévia de novo.
- Na A08, por que o fator do desconto foi criado a partir de texto? Porque Decimal("0.87") é exato. Com o número 0.87 (float) o valor já nasce com uma pequena aproximação.
- Qual resultado esperado da A08 ajuda a detectar desconto aplicado duas vezes? R$ 100,00 no PIX dá R$ 87,00. Se desse R$ 75,69, o desconto foi aplicado duas vezes.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
arquivos.py: validar_catalogo, ler_catalogo e salvar_catalogo. Não usa Tkinter e não importa o modelos.py.
modelos.py e pagamento.py: iguais aos da A11, sem mudança.
verificar.py: testes com assert, sem janela. Usa uma pasta temporária para os arquivos de teste.
main.py: a janela com as abas Pedido e Exercício JSON, o menu "Ir para" e os seletores de arquivo. Importa modelos, pagamento e arquivos.
O Pedido existe só enquanto a janela está aberta e é criado uma vez só. O catálogo JSON só vira arquivo quando eu clico em Salvar JSON. Até lá ele é só o texto do editor.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Ausente retorna coleção vazia sem criar arquivo silenciosamente.
Previsão: ler_catalogo de um caminho que não existe devolve [] e o arquivo continua não existindo.
Observado: igual. Devolveu [] e o arquivo não foi criado (verificar.py passou).
Correção/reteste ou pendência: nenhuma.

T02 — UTF-8 conserva Picolé/limão.
Previsão: depois de salvar e ler de volta, "Picolé de limão" continua igual. No arquivo, os acentos aparecem normais (UTF-8), não como \u00e9.
Observado: igual. A lista lida ficou igual à salva. O arquivo tem "Picolé" em UTF-8 e não tem \u00e9.
Correção/reteste ou pendência: nenhuma.

T03 — JSON malformado e conteúdo com encoding inválido não são sobrescritos.
Previsão: um JSON sem vírgula dá erro. Um arquivo em latin-1 (com "Picolé") dá erro de UTF-8. Nos dois casos os bytes do arquivo ficam iguais antes e depois.
Observado: igual. O JSON sem vírgula deu "O arquivo tem erro de JSON...". O arquivo latin-1 deu "O arquivo não está em UTF-8...". Nos dois casos os bytes ficaram iguais.
Correção/reteste ou pendência: nenhuma.

T04 — Estrutura incorreta, IDs repetidos e preço inválido são rejeitados.
Previsão: dão ValueError: JSON que não é lista, produto sem campo, id repetido, id 0 ou em texto, nome vazio, preço em texto ou zero.
Observado: igual. Os 9 casos ruins deram ValueError.
Correção/reteste ou pendência: nenhuma.

T05 — Falha de escrita mantém o destino anterior e não anuncia sucesso.
Previsão: salvar dados inválidos não muda o arquivo. Quando a troca do arquivo falha (o destino é uma pasta), dá erro "Não foi possível salvar", não sobra arquivo .tmp e o arquivo anterior continua igual.
Observado: igual. Dados inválidos deram erro de preço e o arquivo não mudou. Com o destino sendo uma pasta, deu "Não foi possível salvar. O arquivo anterior foi mantido.", não sobrou .tmp e o arquivo anterior ficou igual.
Correção/reteste ou pendência: nenhuma.

T06 — Cancelar seletor não altera tela nem arquivo.
Previsão: se eu cancelar o Carregar ou o Salvar, o texto do editor continua igual, não aparece mensagem de sucesso e nenhum arquivo é criado.
Observado: Igual. O texto não foi alterado e não foi evidenciado nenhuma mensagem.
Correção/reteste ou pendência: nenhuma.

T07 — Navegar entre abas conserva pedido e estado.
Previsão: monto um pedido, vou para a aba Exercício JSON e volto. Os itens, o total e o estado "montagem" continuam iguais.
Observado: Igual. Apos montar o pedido, sair e voltar para a aba pedido, os itens e o estado continuou.
Correção/reteste ou pendência: nenhuma.

T08 — Exercício JSON não modifica automaticamente o catálogo em memória.
Previsão: carregar um JSON na aba Exercício JSON não muda o pedido nem a lista de produtos da aba Pedido.
Observado: Igual. não foi alterado o pedido após carregar o JSON.
Correção/reteste ou pendência: nenhuma.

## Explicação individual
Uma decisão que consigo justificar:
O ler_catalogo só le, nunca grava. Assim, se o JSON estiver quebrado, o arquivo continua como estava, em vez de ser trocado por uma lista vazia.
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados:
modelos.py, pagamento.py, arquivos.py, verificar.py, main.py e este registro, todos da pasta A12. O verificar.py foi executado e passou. O main.py foi executado e abriu as duas abas.
Caminho de dados fictícios usado (se houver):
os arquivos de teste do verificar.py ficam numa pasta temporária que some no final. Na janela, o JSON fictício que eu escolher salvar.
Entrega pelo fluxo combinado conferida por mim:
Enviei os arquivos para o github e conferi que eles aparecem lá.

## Teoria e transferência
Consigo distinguir caminho, texto, codificação e dados decodificados.
Minha explicação:
O caminho indica onde o arquivo está salvo. O texto é o que consigo ler. A codificação UTF-8 transforma os caracteres em bytes para serem armazenados. Os dados decodificados são as informações que o python consegue interpretar depois de ler o arquivo.
Consigo explicar por que validar JSON exige mais que aceitar a sintaxe.
Minha explicação:
Porque um JSON pode estar escrito corretamente, mas ter informações erradas. pois pode faltar o ID de um produto, ter um preço negativo ou IDs repetidos. Por isso, além de verificar se o JSON está correto, precisamos validar os dados e seus tipos.
Consigo prever pedido e edição depois de navegar, cancelar ou falhar na leitura.
Minha explicação:
O sistema tem que preservar os dados do pedido durante a navegação e permitir que o usuário continue editando quando cancelar uma operação. Se ocorrer um erro na leitura do arquivo, os dados anteriores não devem ser apagados ou substituídos por informações inválidas.
Ligação entre o ensaio e meus arquivos da atividade:
No arquivo modelos.py, a classe Pedido controla os itens, o estado e a versão do pedido. No arquivo arquivos.py, as funções ler_catalogo, salvar_catalogo e validar_catalogo cuidam da leitura, gravação e validação dos dados dos produtos.
Minha previsão antes da alteração guiada e o resultado observado:
Minha previsão era que o sistema conseguiria identificar arquivos inválidos e impedir que dados incorretos fossem carregados. Ao prever a implementação, vi que existem verificações de codificação UTF-8, sintaxe JSON, campos obrigatórios, tipos de dados e valores positivos.

## Continuação em casa
Arquivos/versão executados:
modelos.py (A11) e arquivos.py (A12).
Pasta e comando usados:
Pasta: UC8-Python\anexos\A12 / python main.py
Justificativa de 5-8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre leitura/escrita UTF-8, estrutura JSON, validação integral e navegação sem recriar o modelo:
O "sistema" lê e grava o catálogo sempre em UTF-8, para os acentos não se perderem.
O catálogo é uma lista de produtos com id, nome e preço em centavos.
O validar_catalogo confere a lista inteira antes de aceitar: ids únicos, nome com texto e preço inteiro positivo.
Ao salvar, o "sistema" salva num arquivo temporário na mesma pasta e só no fim troca o arquivo de destino.
Assim, uma falha não estraga o arquivo que já existia.
O Pedido é criado uma vez só em criar_janela, então trocar de aba não apaga o carrinho.
Minha explicação / anexo: Fiz a explicação acima.

## Checklist da interface
Controles e rótulos que conferi:
Abas "Pedido" e "Exercício JSON", e o menu "Ir para" com as opções Pedido e Exercício JSON. 
Na aba Pedido: Produto (lista), Quantidade (campo), tabela com Código, Produto, Qtd e Subtotal, Estado, Forma de pagamento (lista).
E os botões Adicionar, Atualizar, Remover, Finalizar pedido e Novo pedido. 
Na aba JSON: o editor de texto, a mensagem de aviso e os botões Carregar JSON e Salvar JSON. Conferi pelo código.

Percurso por Tab/Shift+Tab e acionamento:
Pela ordem em que criei os controles, na aba Pedido o Tab deve ir Produto > Quantidade > Tabela > Forma de pagamento > Adicionar > Atualizar > Remover > Finalizar pedido > Novo pedido, e o Shift+Tab volta. Na aba JSON deve ir do editor para Carregar JSON e Salvar JSON. Os botões devem acionar com a barra de espaço.

Mensagem após erro e possibilidade de corrigir:
O erro aparece no texto de aviso da aba. Na aba JSON, se o arquivo carregado for inválido ou o texto do editor não passar na validação, o editor continua com o mesmo texto e eu posso corrigir e tentar de novo. Pendente: confirmar na janela.

Redimensionamento e comportamento que observei:
Pelo código, ao aumentar a janela as abas crescem, a tabela da aba Pedido cresce e o editor da aba JSON também. Os outros controles ficam do mesmo tamanho. Pendente: confirmar na janela.

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Tudo foi executado.

Caso para nova tentativa em sala:
