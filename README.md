# APS LogComp - BarScript

# Palavras-chave:
- declaração de variável → `papo_que`
- condicional if → `cpa`
- condicional else → `caducou`
- loop while → `boh`
- print → `manda_ae`
- input → `fala_comigo`
- booleano true → `fatos`
- booleano false → `migue`

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
  - Para ler uma entrada do usuário:
    ```
    fala_comigo(nome_da_variavel)
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

- **Operadores**
  - **Aritméticos**: `+`, `-`, `*`, `/`
  - **Relacionais**: `==`, `!=`, `>`, `<`, `>=`, `<=`
  - **Lógicos**: `&&`, `||`

- **Comentários**
  - Comentários de linha única começam com `//`.

---



# EBNF Formal

```

<programa> ::= "{" <lista_de_comandos> "}"

<lista_de_comandos> ::= { <comando_ou_comentario> }

<comando_ou_comentario> ::= <comando> | <comentario>

<comando> ::= <declaracao_variavel>
            | <atribuicao>
            | <condicional>
            | <loop>
            | <impressao>
            | <leitura>

<comentario> ::= "//" { <caractere> } "\n"

<declaracao_variavel> ::= "papo_que" <identificador> "=" <expressao>

<atribuicao> ::= <identificador> "=" <expressao>

<condicional> ::= "cpa" "(" <expressao_condicao> ")" <bloco> [ "caducou" <bloco> ]

<loop> ::= "boh" "(" <expressao_condicao> ")" <bloco>

<impressao> ::= "manda_ae" "(" <expressao> ")"

<leitura> ::= "fala_comigo" "(" <identificador> ")"

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

<booleano> ::= "fatos" | "migue"

<identificador> ::= <letra> { <letra> | <digito> | "_" }

<numero> ::= { <digito> }

<texto> ::= '"' { <caractere> } '"'
```




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

    boh (idade < 21) {
        idade = idade + 1
        manda_ae(idade)
    }
}
