# APS LogComp - BarScript

# Curiosidade:
O nome "BarScript" foi inspirado em expressões informais de conversa de bar, e a linguagem foi projetada com comandos que remetem à fala cotidiana (ex: 'papo_que', 'fala_comigo', 'sai_fora'), tornando o aprendizado mais divertido.

# Palavras-chave:
- declaração de variável → `papo_que`
- condicional if → `cpa`
- condicional else → `caducou`
- loop while → `boh`
- print → `manda_ae`
- input → `fala_comigo`
- booleano true → `fatos`
- booleano false → `migue`
- sair do loop (break) → `sai_fora`
- pular para próxima repetição (continue) → `continua`

# Resumo

- **Tipos**
  - Não existe declaração explícita de tipo. A variável é criada com `papo_que` e seu valor define implicitamente o tipo.
  - Exemplos de valores: números, strings (entre aspas), booleanos (`fatos` ou `migue`).

- **Declaração**
  - Variáveis são declaradas usando:
    ```
    papo_que nome_da_variavel = valor
    ```
  - Exemplo:
    ```
    papo_que idade = 18
    papo_que nome = "Zé"
    papo_que ta_bebado = fatos
    ```

- **Booleanos**
  - `fatos` representa o valor verdadeiro (true).
  - `migue` representa o valor falso (false).

- **Interação com Usuário**
  - Para imprimir no console: 
    ```
    manda_ae(expr)
    ```
  - Para ler uma entrada do usuário (como string ou número):
    ```
    papo_que entrada = fala_comigo()
    ```

- **Controle de Fluxo**
  - Condicional IF:
    ```
    cpa (condicao) {
        // comandos
    }
    ```
  - Condicional ELSE:
    ```
    caducou {
        // comandos
    }
    ```
  - Loop WHILE:
    ```
    boh (condicao) {
        // comandos
    }
    ```
  - `sai_fora` encerra o loop atual.
  - `continua` pula para a próxima repetição do loop.

- **Operadores**
  - **Aritméticos**: `+`, `-`, `*`, `/`, `%`
  - **Relacionais**: `==`, `!=`, `>`, `<`, `>=`, `<=`
  - **Lógicos**: `&&`, `||`

- **Comentários**
  - Comentários de linha única começam com `//`.

---

# EBNF Formal

```ebnf
<programa> ::= "{" <lista_de_comandos> "}"

<lista_de_comandos> ::= { <comando_ou_comentario> }

<comando_ou_comentario> ::= <comando> | <comentario>

<comando> ::= <declaracao_variavel>
            | <atribuicao>
            | <condicional>
            | <loop>
            | <impressao>
            | <leitura>
            | <sai_fora>
            | <continua>

<comentario> ::= "//" { <caractere> } "\n"

<declaracao_variavel> ::= "papo_que" <identificador> "=" <expressao>

<atribuicao> ::= <identificador> "=" <expressao>

<condicional> ::= "cpa" "(" <expressao_condicao> ")" <bloco> [ "caducou" <bloco> ]

<loop> ::= "boh" "(" <expressao_condicao> ")" <bloco>

<impressao> ::= "manda_ae" "(" <expressao> ")"

<leitura> ::= "fala_comigo" "(" ")" 

<sai_fora> ::= "sai_fora"
<continua> ::= "continua"

<bloco> ::= "{" <lista_de_comandos> "}"

<expressao_condicao> ::= <expressao> 
                       | <expressao> <operador_relacional> <expressao>
                       | <expressao> <operador_logico> <expressao>

<operador_relacional> ::= "==" | "!=" | ">" | "<" | ">=" | "<="

<operador_logico> ::= "&&" | "||"

<expressao> ::= <termo> { ("+" | "-") <termo> }

<termo> ::= <fator> { ("*" | "/") <fator> }

<fator> ::= <numero> 
          | <texto> 
          | <booleano> 
          | <identificador> 
          | "(" <expressao> ")"
          | "fala_comigo" "(" ")"

<booleano> ::= "fatos" | "migue"

<identificador> ::= <letra> { <letra> | <digito> | "_" }

<numero> ::= { <digito> }

<texto> ::= '"' { <caractere> } '"'
```

---

# Exemplo de Programa em BarScript

```barscript
{
    papo_que idade = 26
    papo_que nome = "Raul"
    papo_que ta_bebado = migue

    manda_ae(idade)
    manda_ae(nome)

    cpa (idade >= 18) {
        manda_ae("Pode beber, meu chapa!")
    }
    caducou {
        manda_ae("Vai tomar coca-cola!")
    }

    boh (idade < 30) {
        cpa (idade == 28) {
            sai_fora
        }
        cpa (idade % 2 == 0) {
            continua
        }
        manda_ae(idade)
        idade = idade + 1
    }
}
```
