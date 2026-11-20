# Minha entrega final — A20

Identificação individual e data: Lucas Miranda Fernandez 14268 - 19/11/26
Versão/pasta enviada e cópia local: pasta A18 (sorveteria com SQLite, controllers, vendas e README), mais a pasta A20 (vínculos). Cópia local: C:\\dev\\UC8-Python\\anexos\\A20.

## Inventário
Arquivos necessários, README e caminho do banco fictício:
- Pasta A18: main.py, modelos.py, pagamento.py, repositorio.py, memoria.py, controller.py, arquivos.py, relatorios.py, perfis.py e verificar.py.
- Pasta A20: vinculos.py, relacoes_sqlite.py, verificar.py e este documento.
- README: README-A18.md, com ambiente, comandos, primeiro uso e limites.
- Banco fictício: o main.py cria o sorveteria_a18.db na mesma pasta dele, quando a janela abre. Não precisa de caminho absoluto.
Relatórios e matriz que acompanham a entrega: o relatório CSV fictício gerado pelo botão Exportar CSV (se eu gerar um) e os registros (registro-a18.md e registro-a20.md).
Ambientes/caches/dados operacionais excluídos: não entram na entrega a pasta __pycache__ e o sorveteria_a18.db com os meus dados de teste (quem receber cria um banco vazio ao abrir a janela).

## Evidências individuais
I1 — ambiente e reprodução: caso: copiar a pasta A18 para outra pasta e seguir o README-A18.md (`python verificar.py` e depois `python main.py`). Resultado: os comandos de verificação da A20 foram executados e concluídos sem erros. Pendência:.
I2 — código e funcionalidades: caso: fazer uma venda de R$ 47,00 no PIX, confirmar, fechar e abrir o programa de novo, e conferir que a venda continua gravada. Resultado: A vendo continuou gravada no banco de dados. Pendência:.
I3 — interface, usabilidade e acessibilidade: caso: percorrer a aba Pedido com Tab e Shift+Tab e abrir a prévia com o foco em Cancelar. Resultado: Ocorreu como o esperado. Pendência:.
I4 — eventos e validações: caso: salvar um produto com preço 0 e depois corrigir para 7,50 na mesma sessão; e tentar excluir um cliente que já tem venda. Resultado: O codigo bloqueia valores igual ou menor que zero.. Pendência: .

## Recuperação
Dificuldade delimitada e apoio recebido: o relatorios.py ficou com o conteúdo de outro arquivo colado dentro dele, e o programa deu erro de import circular. O apoio foi a explicação da IA (Claude) apontando a linha com o problema.
Nova tentativa individual e evidência: após executar `python verificar.py`, apareceu `Casos executados: previsões e resultados conferem.`.
O que ainda não foi observado:

## Vínculos
IDs válidos, referência inexistente e exclusão vinculada: no projeto, a venda guarda cliente_id (aponta para clientes.id) e itens_venda guarda produto_id (aponta para produtos.id), e o repositorio.py liga o foreign_keys em cada conexão; excluir um cliente ou produto ligado a venda é recusado com a mensagem "ligado a vendas" (caso T04 do verificar.py da A18). No vinculos.py, uma matrícula com aluno 41 e plano 7 é válida. Com aluno 92, ele avisa que o aluno não existe. Excluir o aluno 41 enquanto ele tem matrícula não é permitido. Resultado observado por mim: `python vinculos.py` mostrou Inicial: True, Após nome: True, a referência ao aluno 92 foi identificada e a exclusão do aluno 41 foi bloqueada (False).
Diferença observada entre validação JSON e restrição SQLite: no código em memória, a conferência só acontece quando alguém chama validar_vinculos ou pode_excluir_aluno. No SQLite, com foreign_keys ligado em cada conexão e ON DELETE RESTRICT, o próprio banco recusa o vínculo inválido e a exclusão do que ainda está em uso. Sem ligar o foreign_keys, o banco aceita a referência órfã. Resultado observado por mim: todos os testes retornaram True: vínculo válido, ID inexistente bloqueado, exclusão vinculada bloqueada, dados preservados, correção revalidada e referência órfã aceita sem foreign_keys.

## Entrega
Downloads/arquivos executados conferidos: vinculos.py, relacoes_sqlite.py e verificar.py foram executados, e os resultados conferiram.
Recebimento no canal combinado conferido por mim: .
Autoavaliação e próximo estudo: consegui entender melhor como os IDs mantêm os vínculos, como referências inválidas são identificadas e como o SQLite protege os registros com chaves estrangeiras. Quero continuar praticando validações e testes.
