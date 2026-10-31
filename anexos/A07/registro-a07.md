# Meu registro A07 — Sorveteria: produtos, itens e pedido

Nome/código individual: Lucas Miranda Fernandez
Turma e data: 14268

## Retomada sem consulta
- Na A06, o que self identifica? O objeto que recebeu a chamada (em lia.atualizar(...), self é a lia).
- Por que o modelo da A06 é verificável sem janela? Porque aluno.py não importa Tkinter; só recebe textos e devolve mensagens.
- Na A03, de qual valor parte uma nova conversão? Do valor original, não do resultado anterior.
- Dois objetos da A06 podem compartilhar a mesma lista de notas? Não, __init__ cria uma lista nova por objeto.

## Arquitetura antes do código
modelos.py (quantidade, formatar, Produto, Item, Pedido; sem Tkinter) · verificar.py (assert sem janela) · main.py (janela). main.py importa modelos; modelos não importa ninguém. Os dados vivem só na sessão: o Pedido existe enquanto a janela existe; nenhum arquivo é gravado.
- Produto guarda código, nome e preço unitário em centavos.
- Item guarda uma referência ao Produto e a quantidade; calcula o subtotal.
- Pedido guarda self.itens = {código: Item} criado em __init__ e calcula o total.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.

T01 — Duas frutas a R$5,00 e três leites a R$7,50.
Previsão: subtotais 1000 e 2250; total 3250; "R$ 32,50".
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T02 — Pedido novo sem itens e sem compartilhar a coleção.
Previsão: linhas() == [], total 0 e `outro.itens is not pedido.itens`.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T03 — Mesmo código soma; nome igual com código distinto fica separado.
Previsão: fruta passa a 5 na mesma linha (2 linhas); Fruta P03 cria a 3ª; total 5×500 + 3×750 + 600 = 5350.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T04 — Sem seleção: orientar e preservar.
Previsão: "Selecione um produto antes de adicionar." e linhas/total idênticos.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T05 — Quantidade inválida: recusar sem alteração.
Previsão: recusa "", "   ", abc, 0, -1, 1,5, 1.5, 1000, +2 e "2 3"; aceita 1 e " 999 ".
Observado: igual; o pedido ficou idêntico depois de cada recusa.
Correção/reteste ou pendência: nenhuma.

T06 — Acumular acima de 999.
Previsão: 999 + 1 é recusado e a linha continua ("P02", "Leite", 999, 749250).
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T07 — Total recalculado depois de cada inclusão válida.
Previsão (primeira tentativa): 500, 2000 e 3500.
Observado: o terceiro assert falhou (AssertionError); o total real foi 3000.
Correção/reteste ou pendência: refiz a conta no papel — depois de fruta×1, leite×2 e fruta×2 há 3 frutas (1500) e 2 leites (1500) = 3000. O erro estava na previsão, não no modelo. Corrigi a previsão para 3000, executei de novo e passou.

T08 — Percurso por teclado, rótulos, expansão e execução sem imagem.
Previsão: Tab percorre produto → quantidade → botões; Enter na quantidade adiciona; a tabela cresce ao ampliar; sem imagem.
Observado: 
Correção/reteste ou pendência: 

## Explicação individual
Uma decisão que consigo justificar: Pedido guarda os itens em um dicionário criado em __init__, com o código como chave: assim reconheço um produto repetido pelo código (não pelo nome) e cada pedido tem a sua coleção.
Uma dificuldade, apoio e próxima tentativa: 

## Arquivos
Versão executada e arquivos baixados: modelos.py, verificar.py, main.py e este registro.
Caminho de dados fictícios usado (se houver): nenhum, catálogo fixo em main.py.
Entrega pelo fluxo combinado conferida por mim: 

## Teoria e transferência
- Classe e instância no ensaio das caixas: Caixa descreve o tipo; caixa_a e caixa_b são duas instâncias.
- __init__ e self: __init__ prepara os dados de cada objeto novo; self é o objeto que recebeu a chamada.
- Por que cada pedido precisa de sua coleção: para que incluir um item em um pedido não apareça em outro.
- Onde ficam preço, quantidade, subtotal e total: preço em Produto; quantidade e subtotal() em Item; total_centavos() em Pedido.
- Como localizo um produto pelo código: `produto.codigo in self.itens`.
- Dois nomes para o mesmo objeto: caixa_b = caixa_a não cria outra caixa; alterar por um nome muda o que se vê pelo outro.

## Continuação em casa
Arquivos e versão que realmente executei: verificar.py com modelos.py desta pasta.
Comando e pasta usados: `python verificar.py`, na pasta A07.
Justificativa de 5–8 linhas ou nome do áudio de aproximadamente 60 segundos:
Escolhi explicar independência, identificação por código ou validação antes da alteração:
Minha explicação / arquivo anexado:

## Checklist da interface
Seleção identificável — observação:
Mensagem compreensível após erro — observação:
Percurso por Tab/Shift+Tab e acionamento — observação:
Correção na mesma janela — observação:

## O que ainda não executei
Caso pendente e motivo, incluindo falta de ambiente quando houver:
Próxima tentativa que levarei para conferência:
