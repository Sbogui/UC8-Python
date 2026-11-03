# Meu registro A08 — Sorveteria: pagamentos e arredondamento

Nome/código individual, turma e data: Lucas Miranda Fernandez 14268 - 02/11/26

## Retomada sem consulta
Minha hipótese inicial para cada item:
- Preço unitário, quantidade e subtotal: preço é do Produto; quantidade é do Item; subtotal = quantidade × preço.
- Uma inclusão inválida apaga itens já aceitos? Não: valida antes de alterar.
- Na A04, por que validar as cinco notas antes de confirmar? Para o registro não misturar dados de tentativas diferentes.
- Por que o total é recalculado pela coleção? Porque o rótulo é só texto formatado; a fonte dos dados são os itens.

## Arquitetura antes do código
Desenho dos módulos, dependências e duração dos dados:
modelos.py da A07 reutilizado, pagamento.py funcões, sem Tkinter e sem importar o pedido. main.py importa modelos e pagamento. A interface entrega ao pagamento o subtotal em texto decimal e a forma, recebe (subtotal, desconto, total) novos.

## Matriz de execução
Para cada caso, registre previsão, observado, correção e nova execução.
Casos T01 a T08 vêm de "python verificar.py" (sem -O). Janela não executada, sem Tkinter. As previsões numéricas foram calculadas à mão/calculadora antes de executar.

T01 — R$100,00 → 87,00 dinheiro/PIX; 92,00 débito; 100,00 crédito1x.
Previsão: totais 87,00; 87,00; 92,00; 100,00 (descontos 13,00; 13,00; 8,00; 0,00).
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T02 — R$0,50 no PIX → R$0,44 com HALF_UP.
Previsão: 0,50 × 0,87 = 0,435 → total 0,44; desconto 0,06.
Observado: (0.50, 0.06, 0.44).
Correção/reteste ou pendência: nenhuma.

T03 — Duas chamadas iguais produzem resultados iguais e não alteram os itens.
Previsão: pedido de 32,50 no PIX: 28,275 → 28,28 nas duas chamadas; linhas e total do pedido iguais antes/depois.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T04 — Trocar PIX/crédito/PIX recalcula do subtotal original.
Previsão: 28,28; 32,50; 28,28.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T05 — Forma vazia ou desconhecida: erro orientado.
Previsão: "Escolha a forma de pagamento." (vazia ou só espaços); "Forma de pagamento desconhecida." (Cheque).
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T06 — Valor com letras, NaN/inf, negativo, milhares ou mais de duas casas: recusar.
Previsão: recusa abc, nan, inf, -1, +1, 1.000,00, 1,000, 1.234, 10,555, vazio, 1e3, "1 0"; aceita 7,5 = 7.50 e o limite 1.000.000,00; recusa 1.000.000,01; zero só quando permitido.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T07 — Subtotal = desconto +total após arredondamento.
Previsão: fecha para 6 subtotais × 4 formas; total sempre com duas casas.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

T08 — Validações de quantidade e catálogo da A07 preservadas.
Previsão: 999 + 1 recusado e linha mantida; sem produto e "1,5" recusados; formatar(3250) = "R$ 32,50"; preco_para_centavos("7,50") = 750.
Observado: igual.
Correção/reteste ou pendência: nenhuma.

## Explicação individual
Uma decisão que consigo justificar: calcular_pagamento sempre parte do subtotal original e devolve um resultado novo, então repetir o clique ou trocar a forma não acumula desconto.
Uma dificuldade, apoio e próxima tentativa:

## Arquivos
Versão executada e arquivos baixados: modelos.py , pagamento.py, verificar.py, main.py e este registro.
Caminho de dados fictícios usado (se houver): nenhum.
Entrega pelo fluxo combinado conferida por mim: 

## Teoria e transferência
Consigo distinguir subtotal, desconto e total.
Minha explicação: subtotal é o valor dos itens, total é o valor depois da forma de pagamento, desconto = subtotal − total arredondado.

Consigo explicar por que Decimal recebe texto e onde ocorre o arredondamento.
Minha explicação: Decimal("0.87") é exato, Decimal(0.87) já nasceria com a aproximação do float. O arredondamento acontece uma vez, ao quantificar o total.

Consigo prever o efeito de repetir uma conferência sem mudar os itens.
Minha explicação: o resultado é o mesmo, porque a base é sempre o subtotal original.

Ligação entre o ensaio e meus arquivos da atividade:
Minha previsão antes da alteração guiada e o resultado observado:

## Continuação em casa
Arquivos/versão executados:
Pasta e comando usados:
Justificativa de 5–8 linhas ou nome do áudio de cerca de 60 segundos:
Decisão do meu código sobre funções puras de pagamento, Decimal de texto, ROUND_HALF_UP e subtotal preservado:
Minha explicação / anexo:

## Checklist da interface
Controles e rótulos que conferi:
Percurso por Tab/Shift+Tab e acionamento:
Mensagem após erro e possibilidade de corrigir:
Redimensionamento e comportamento que observei:

## Pendências
O que não executei e por quê, incluindo falta de ambiente:
Caso para nova tentativa em sala:
