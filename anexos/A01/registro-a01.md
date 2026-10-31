# A01 — minha tentativa e meus testes

Use código de estudante na entrega. Não inclua dados pessoais de terceiros.
Python observado: Python 3.10.11
Tcl/Tk observado: Tcl/Tk version 8.6
Interpretador selecionado no VS Code: 

## Diagnóstico sem consulta
1. O que distingue texto de número? Se possui int antes da entrada da chamada
2. Como uma função recebe uma entrada e produz uma saída? No python a função é chamda pela variavel String ou int.. e na saída é pelo return ou print.
3. O que uma condição decide? Se tal dado que esta sendo utilizado vai ser aprovado ou não antes de concluir a chamada
Minha resposta inicial:
Não entedi?

## Matriz de testes (preencha antes e depois da execução)
| Nome fictício | Idade digitada | Resultado esperado | Resultado observado | Ajuste |
|---|---|---|---|---|
| Lia | 18 | 18 | Nome: Lia Idade: 18 anos | Não necessario |
| vazio | 18 | O nome não pode ficar vazio!	 | O nome não pode ficar vazio!	 | Não Necessario |
| somente espaços | 18 | O nome não pode ficar vazio | O nome não pode ficar vazio | preencher com nome |
| Lia | vazio | Não aceita texto na idade | Coloque a idade com número inteiro | preencher corretamente a idade |
| Lia | abc | Coloque a idade como número inteiro! | Coloque a idade como número inteiro! | X |
| Lia | 0 | A idade tem que ser maior que 0! | A idade tem que ser maior que 0! | X |
| Lia | -2 | A idade tem que ser maior que 0! | A idade tem que ser maior que 0! | X |
| Lia | 2.5 | Coloque a idade como número inteiro! | Coloque a idade como número inteiro! | X |
| Ana Maria | 21 | Conferencia do cadastro. Nome: Ana Maria, Idade: 21 anos | Nome: Ana Maria, Idade: 21 anos  | X |

## Interface
Testei botão, Tab e Shift+Tab:
Comparei o resultado do terminal com o da janela:
Fechei e reabri; o que aconteceu com o resultado?

## Fechamento (sem consulta)
Explique entrada → validação → resposta com suas palavras: O usuário digita nas caixas, o programa lê guardando o resultado da chama que o usuario respondeu e faz a validação com a condição.
Uma dificuldade, a correção que tentei e meu próximo passo: Pensar como utilizar o mesmo formato no que foi feito no terminal para o Tkinter. Procurar os comandos na propria aula e no site do "tkinter", próximo passo agora é treinar mais para ficar mais facil de enteder e compreender oq fazer.
Arquivos anexados separadamente: terminal.py e cadastro.py.
