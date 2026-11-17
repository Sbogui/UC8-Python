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

**Ensaio sem tocar no banco principal:** passe outro caminho.
```
python main.py ensaio.db
```
**Começar do zero:** feche a janela e apague `sorveteria_a18.db` (ou use outro nome, como acima).

### Primeiro uso (dados fictícios)
1. Aba **Cadastros** > clique em **Entrar (simulação)** com perfil *Administração* (sem isso os botões ficam desativados).
2. Cadastre um produto: nome `Taça Grande`, preço `35,00`, **Salvar**. Depois `Água`, `6,00`.
3. Cadastre um cliente: `Ana`.
4. Aba **Venda**: escolha cliente e produto, quantidade `1`, **Adicionar**. Repita com `Água` e quantidade `2`.
5. Total esperado: **R$ 47,00**. Com PIX, a confirmação mostra **R$ 40.89**; com Débito, **R$ 43.24**.
6. **Finalizar** > confirmar. A mensagem diz o número da venda. Depois **Exportar CSV**.

## Verificação
Rode **sem** `-O` (a opção `-O` desliga os `assert`; o script avisa e para):
```
python verificar.py
```
Resultado esperado: sete linhas `OK`, a linha de isolamento e, no fim, `Casos executados: previsões e resultados conferem.`
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