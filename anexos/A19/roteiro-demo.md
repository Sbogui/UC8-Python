# Minha demonstração individual — A19

## Demonstração do fluxo
Problema e requisito escolhido: o programa registra vendas de uma sorveteria fictícia, com cliente, produtos, forma de pagamento e comprovante, e não perde os dados ao fechar. O requisito que vou demonstrar: a venda e os itens são gravados juntos no banco, e só depois de eu confirmar.
Arquivos/caminho e comando: pasta A19 (modelos.py, pagamento.py, arquivos.py, relatorios.py, perfis.py, repositorio.py, memoria.py, controller.py, main.py, backup_sqlite.py, verificar.py). Comando: `python main.py`. O banco fica no arquivo sorveteria_a18.db, na mesma pasta do main.py.
Fluxo válido com dados fictícios:
1. Aba Clientes: salvar "Maria Fictícia".
2. Aba Produtos: salvar "Sorvete" a 6,50 e "Picolé" a 5,00.
3. Aba Pedido: clicar em "Atualizar catálogo e clientes", escolher a cliente, o Sorvete e a quantidade 2, e clicar em Adicionar.
4. Escolher PIX, clicar em Finalizar pedido e depois em Confirmar.
O que deve aparecer: "Venda ID 1" no resumo, com subtotal R$ 13,00, desconto R$ 1,69 e total R$ 11,31. O estado do pedido vira "finalizado".
Caso de erro ou cancelamento:
- Cancelar: clicar em Finalizar pedido e depois em Cancelar (ou no X, ou no Escape). O que deve acontecer: os itens e o total continuam iguais e nenhuma venda é gravada.
- Erro: depois de montar o item, mudar o preço do Sorvete na aba Produtos e tentar confirmar. O que deve acontecer: aparece uma mensagem de que o produto mudou, a montagem continua e nenhuma venda é gravada.
Persistência e relatório:
- Fechar o programa e abrir de novo: os clientes e os produtos devem continuar na tela.
- Clicar em Exportar CSV e abrir o arquivo: deve ter 1 linha com o id do produto, a quantidade 2, o subtotal 1300 e o total 11,31.
- Rodar `python verificar.py`: deve imprimir "Casos executados: previsões e resultados conferem."
Limite e próximo teste: o pedido em montagem fica só na memória e se perde se eu fechar o programa antes de finalizar. O perfil (Caixa/Administração) é só simulação e não autentica. A janela ainda precisa ser conferida por mim: Tudo certo!. 

## Pergunta técnica individual
Decisão que consigo explicar com código/evidência: o registrar_venda (repositorio.py) grava a venda e todos os itens dentro do mesmo "with con:". Se um item falhar, a venda inteira é desfeita. Evidência: no verificar.py da A18 (T04), o mesmo produto duas vezes deixa 0 vendas e 0 itens no banco, e o mesmo caso corrigido grava a venda ID 1.

## Comparação com academia
Entidades e IDs observados: (preencher depois de abrir o academia_amostra.py: quais são as entidades, como ficam ligadas e qual ID liga os registros)
Camadas e armazenamento comprovados pela leitura: (preencher: quais classes ou funções cuidam de dados, regras e armazenamento, e onde isso aparece no código)
O que não pude afirmar somente pelo README:

## Backup em cópia
Origem e destino novo: origem `origem-ficticia.db` e destino `copia-nova.db`, numa pasta de ensaio (nunca o banco principal). Comando: `python backup_sqlite.py origem-ficticia.db copia-nova.db`.
Consulta de dados conhecidos na cópia: no verificar.py, abro a cópia por outra conexão e confiro os produtos [(1, "Sorvete", 650), (2, "Picolé d'água", 500)], o cliente "Maria D'Ávila", a venda ID 1 com total 1131 e o resultado "ok" do PRAGMA integrity_check.
Próxima ação após feedback: 
