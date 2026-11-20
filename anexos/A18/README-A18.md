# Minha sorveteria — candidata A18

## Objetivo e limites
Cadastro de produtos e clientes, montagem de pedido, pagamento com desconto, gravação da venda no SQLite e exportação do comprovante em CSV. A pasta também traz `verificar.py`, a suíte de regressão da A18.

O que **não** existe: login real (o perfil Caixa/Administração é só uma simulação), nota fiscal (o comprovante é didático), edição de vendas já gravadas.
O pedido em montagem fica só na memória: se a janela fechar antes de finalizar, ele se perde. Cadastros e vendas confirmadas ficam no banco.

## Ambiente
- Python 3.10 ou mais novo, com Tkinter/ttk. Confira com `python --version` e `python -m tkinter` (deve abrir uma janelinha de teste).
- Só biblioteca padrão. **Não é preciso instalar nada.**
- Linux: se o Tkinter faltar, instale o pacote `python3-tk`.

## Arquivos e execução
Todos na mesma pasta:

| Arquivo | Para que serve |
|---|---|
| `main.py` | abre a janela |
| `modelos.py` | Produto, Item, Pedido (quantidade, total, estado) |
| `pagamento.py` | valores em Decimal e desconto por forma de pagamento |
| `repositorio.py` | banco SQLite: produtos, clientes, vendas |
| `memoria.py` | mesmo contrato do repositório, sem banco |
| `controller.py` | liga a janela ao repositório |
| `arquivos.py` | catálogo em JSON |
| `relatorios.py` | CSV do comprovante |
| `perfis.py` | perfil fictício |
| `verificar.py` | testes |

**Abrir a janela** (a partir da pasta A18):
```
python main.py
```
**Banco:** `sorveteria_a18.db`, criado ao lado do `main.py` na primeira execução (começa vazio).

**Ensaio sem tocar no banco principal:** copie a pasta inteira para outro lugar e rode `python main.py` lá. Cada pasta cria o seu próprio `sorveteria_a18.db`, começando vazio.

**Começar do zero:** feche a janela e apague `sorveteria_a18.db`.

### Primeiro uso (dados fictícios)
1. Aba **Produtos**: nome `Taça Grande`, preço `35,00`, **Salvar produto**. Depois `Água`, `6,00`.
2. Aba **Clientes**: nome `Ana`, **Salvar cliente**.
3. Aba **Pedido**: clique em **Atualizar catálogo e clientes**, escolha o cliente e o produto, quantidade `1`, **Adicionar**. Repita com `Água` e quantidade `2`.
4. Total esperado: **R$ 47,00**. Escolha a forma de pagamento e clique em **Finalizar pedido**: com PIX a prévia mostra **R$ 40,89**; com Débito, **R$ 43,24**.
5. **Confirmar**. A mensagem diz o número da venda. Depois **Exportar CSV**.

A aba **Exercício JSON** só abre depois de **Entrar** na aba *Perfil (simulação)* com o perfil *Administração*. Os cadastros de produtos e clientes não precisam disso.

## Verificação
Rode **sem** `-O` (a opção `-O` desliga os `assert`; o script avisa e para):
```
python verificar.py
```
Resultado esperado: uma única linha, `Casos executados: previsões e resultados conferem.` Se algum `assert` falhar, o Python mostra o erro e a linha do arquivo.
Os testes usam pasta temporária e **não criam nem alteram** `sorveteria_a18.db`.

O que cada caso confere:
- **T01** regras: 3500 + 2 × 600 = 4700; erro depois de item válido; cancelar duas vezes; totais 47,00 / 40,89 (PIX) / 43,24 (Débito).
- **T02** o ID continua certo com a lista invertida.
- **T03** o banco reaberto conserva os dados; a memória nova começa vazia.
- **T04** falha no 2º item não deixa venda pela metade; o mesmo caso corrigido grava a venda 1; preço alterado é recusado; cliente com venda não é excluído.
- **T05** o CSV sai do comprovante e não muda quando o pedido muda.
- **T06** uma previsão errada de propósito (`== 4000`) falha; a correta (`== 4700`) passa.

Uma falha, a correção e o reteste: *(preencher com a correção real que você fez)*

Como conferir os relatórios: abra o CSV (separador `;`, UTF-8). Colunas: `produto_id;nome;quantidade;preco_centavos;subtotal_centavos;forma;total_pedido`. Para a venda do primeiro uso no PIX, o `total_pedido` é `40,89` e o subtotal da Água é `1200`.

## Limites conhecidos
- A janela (`main.py`) só teve a sintaxe conferida no ambiente de preparo, porque ali não havia Tkinter. Abrir e usar a janela precisa ser feito na sua máquina (registro T07 e T08).
- Preço alterado no catálogo com o pedido aberto: use **Atualizar catálogo**, remova a linha antiga e adicione de novo. Se tentar finalizar assim mesmo, a venda é recusada.

## Última conferência (preencha você)
- Data: _17_/_11_/_26_
- Versão do Python (`python --version`): ______
- `python -m tkinter` abriu a janela de teste: (x) sim ( ) não
- `python verificar.py` terminou com "Casos executados": (x) sim ( ) não
- `python main.py` abriu a janela e o primeiro uso funcionou: (x) sim ( ) não
- Executado em outra pasta, por (nome do colega): ______  Dúvida que ele teve: ______