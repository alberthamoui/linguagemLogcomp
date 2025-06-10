import sys
from abc import abstractmethod
from pprint import pprint
DEBUG = False


class SymbolTable:
    def __init__(self):
        self.symbols = {} # {nome: (tipo, valor)}

    def get(self, name):
        if name in self.symbols:
            return self.symbols[name][1] # retorna soh o valor
        else:
            raise ValueError(f"Identificador {name} não encontrado")

    def getType(self, name):
        if name in self.symbols:
            return self.symbols[name][0] # retorna soh o tipo
        else:
            raise ValueError(f"Identificador {name} não encontrado")

    def set(self, name, value, tipo=None):
        if tipo is not None:
            self.symbols[name] = (tipo, value)
        elif name in self.symbols:
            self.symbols[name] = (self.symbols[name][0], value)
        else:
            raise ValueError(f"Identificador {name} não definido")
        
    def has(self, name):  
        return name in self.symbols

class PrePro:
    def __init__(self):
        pass
    @staticmethod
    def filter(code):
        lines = code.splitlines()
        filtered = [line.split("//")[0] for line in lines]
        return "\n".join(filtered)

class Node:
    def __init__(self, value, children=None):
        if children is None:
            children = []
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, st):
        pass

class Block(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def evaluate(self, st):
        final = None
        for child in self.children:
            final = child.evaluate(st)
        return final

class Print(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def evaluate(self, st):
        final = self.children[0].evaluate(st)
        if isinstance(final, bool):
            final = str(final).lower()
        print(final)


        return final

class Assign(Node):
    def __init__(self, children):
        Node.__init__(self, None, children)

    def evaluate(self, st):
        vName = self.children[0].value
        v = self.children[1].evaluate(st)

        if not st.has(vName):
            raise ValueError(f"Variável '{vName}' não foi declarada")  

        tipo = st.getType(vName)

        if tipo == "INT" and type(v) != int:
            raise TypeError(f"Tipo inválido para '{vName}': esperado INT")  
        elif tipo == "STRING" and not isinstance(v, str):
            raise TypeError(f"Tipo inválido para '{vName}': esperado STRING")  
        elif tipo == "BOOL" and not isinstance(v, bool):
            raise TypeError(f"Tipo inválido para '{vName}': esperado BOOL")  

        print(f"[ASSIGN] {vName} = {v}") if DEBUG else None
        st.set(vName, v)
        return v

class If(Node):
    def __init__(self, children):
        # children = [condição, bloco_then, (opcional) bloco_else]
        super().__init__(None, children)

    def evaluate(self, st):
        cond = self.children[0].evaluate(st)
        if not isinstance(cond, bool):
            raise TypeError("Condição do if precisa ser booleana")
        if cond:
            return self.children[1].evaluate(st)
        # se tiver 3 filhos e cond=False, executa else
        if len(self.children) == 3 and self.children[2] is not None:
            return self.children[2].evaluate(st)
        # if sem else && cond=False → nada
        return None

class For(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def evaluate(self, st):
        iteration = 0
        if not self.children or len(self.children) < 2:
            raise ValueError("For mal formado: esperado condição e bloco.")

        while True:
            cond = self.children[0].evaluate(st)
            print(f"[FOR] Iteração {iteration}, condição: {cond}") if DEBUG else None
            if not cond:
                break
            self.children[1].evaluate(st)
            iteration += 1

class Scan(Node):
    def evaluate(self, st):
        raw = input()             # lê do stdin como texto
        try:
            return int(raw)      # tenta converter pra inteiro
        except ValueError:
            return raw           # se não der, retorna texto puro

class Iden(Node):
    def __init__(self, value):
        Node.__init__(self, value, None)

    def evaluate(self, st):
        return st.get(self.value)

class UnOp(Node):
    def evaluate(self, st):
        valor = self.children[0].evaluate(st)
        if self.value == '+':
            if type(valor) != int:
                raise TypeError(f"Operador unário '+' requer um inteiro")
            return +valor
        elif self.value == '-':
            if type(valor) != int:
                raise TypeError(f"Operador unário '-' requer um inteiro")
            return -valor
        elif self.value == '!':
            if not isinstance(valor, bool):
                raise TypeError(f"Operador unário '!' requer um booleano")
            return not valor
        else:
            raise ValueError(f"Operador inválido (UnOp): {self.value}")

class IntVal(Node):
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return self.value

class NoOp(Node):
    def evaluate(self, st):
        pass

class StrVal(Node):  
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return self.value

class BoolVal(Node):  
    def __init__(self, value):
        super().__init__(value)

    def evaluate(self, st):
        return self.value


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class BinOp(Node):
    def evaluate(self, st):
        if len(self.children) != 2:
            raise ValueError(f"Operação binária mal formada: {self.value} esperava dois operandos.")

        left = self.children[0].evaluate(st)
        right = self.children[1].evaluate(st)

        operador = self.value

        def precisaTipo(expected_type):
            if type(left) != expected_type or type(right) != expected_type:
                raise TypeError(f"Operação '{operador}' requer dois {expected_type.__name__}s")

        def precisaMesmoTipo():
            if type(left) != type(right):
                raise TypeError(f"Operação '{operador}' requer dois operandos do mesmo tipo")

        if operador == '+':
            if isinstance(left, str) or isinstance(right, str):
                left = str(left).lower() if isinstance(left, bool) else str(left)
                right = str(right).lower() if isinstance(right, bool) else str(right)
                return left + right
            precisaTipo(int)
            return left + right

        elif operador == '-':
            precisaTipo(int)
            return left - right

        elif operador == '*':
            precisaTipo(int)
            return left * right

        elif operador == '%':
            precisaTipo(int)
            return left % right

        elif operador == '/':
            precisaTipo(int)
            return left // right

        elif operador == '==':
            precisaMesmoTipo()
            return left == right

        elif operador in ['<', '>']:
            precisaMesmoTipo()
            return left < right if operador == '<' else left > right

        elif operador == '||':
            precisaTipo(bool)
            return left or right

        elif operador == '&&':
            precisaTipo(bool)
            return left and right

        elif operador == "!=":
            return left != right
        elif operador == ">=":
            return left >= right
        elif operador == "<=":
            return left <= right

        else:
            raise ValueError(f"Operador inválido (BinOp): {operador}")

class VarDec(Node):  
    def __init__(self, children):
        super().__init__(None, children)  # children = [nome, tipo, valor ou None]

    def evaluate(self, st):
        var_name = self.children[0].value
        init_val = self.children[1].evaluate(st)
        # inferir tipo
        if isinstance(init_val, int):
            var_type = "INT"
        elif isinstance(init_val, str):
            var_type = "STRING"
        elif isinstance(init_val, bool):
            var_type = "BOOL"
        else:
            raise TypeError(f"Tipo não suportado: {type(init_val)}")
        if st.has(var_name):
            raise ValueError(f"Variável '{var_name}' já declarada")
        st.set(var_name, init_val, var_type)
        return init_val

class Break(Node):
    def __init__(self):
        # value=None e children=[] são só placeholders,
        # não usados pelo Break em si
        super().__init__(None, [])
    def evaluate(self, st):
        return self

class Continue(Node):
    def __init__(self):
        super().__init__(None, [])
    def evaluate(self, st):
        return self

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.actual = None
        self.selectNext()

    def selectNext(self):
        # Se for espaço ou tab, pula
        while self.position < len(self.source) and self.source[self.position] in ' \t':
            self.position += 1

        if self.position >= len(self.source):
            self.actual = Token("EOF", None)
            return

        # Se for um operador 
        if self.source[self.position] in ['+', '-', '*', '/', '(', ')', '{', '}', '\n', '=', '|', '&', '!', '<', '>','%']:
            # Operador 2 char

            if self.source[self.position:self.position+2] == "!=":
                self.actual = Token("NE", "!=")
                self.position += 2
                return
            elif self.source[self.position:self.position+2] == ">=":
                self.actual = Token("GE", ">=")
                self.position += 2
                return
            elif self.source[self.position:self.position+2] == "<=":
                self.actual = Token("LE", "<=")
                self.position += 2
                return
            elif self.source[self.position:self.position+2] == '==':
                self.actual = Token("EQEQ", "==")
                self.position += 2
                return
            elif self.source[self.position:self.position+2] == '&&':
                self.actual = Token("AND", "&&")
                self.position += 2
                return
            elif self.source[self.position:self.position+2] == '||':
                self.actual = Token("OR", "||")
                self.position += 2
                return

            # Operador 1 char
            if self.source[self.position] == '+':
                self.actual = Token("PLUS", "+")
                self.position += 1
            elif self.source[self.position] == '-':
                self.actual = Token("MINUS", "-")
                self.position += 1
            elif self.source[self.position] == '*':
                self.actual = Token("MULT", "*")
                self.position += 1
            elif self.source[self.position] == '/':
                self.actual = Token("DIV", "/")
                self.position += 1
            elif self.source[self.position] == '%': # Minha linguagem
                self.actual = Token("MOD", "%")
                self.position += 1
            elif self.source[self.position] == '(':
                self.actual = Token("LP", "(")
                self.position += 1
            elif self.source[self.position] == ')':
                self.actual = Token("RP", ")")
                self.position += 1
            elif self.source[self.position] == '{':
                self.actual = Token("LB", "{")
                self.position += 1
            elif self.source[self.position] == '}':
                self.actual = Token("RB", "}")
                self.position += 1
            elif self.source[self.position] == '\n':
                self.actual = Token("NL", "\n")
                self.position += 1
            elif self.source[self.position] == '=':
                self.actual = Token("EQ", "=")
                self.position += 1
            elif self.source[self.position] == '!':
                self.actual = Token("NOT", "!")
                self.position += 1
            elif self.source[self.position] == '<':
                self.actual = Token("LT", "<")
                self.position += 1
            elif self.source[self.position] == '>':
                self.actual = Token("GT", ">")
                self.position += 1

        # Números 
        elif self.source[self.position].isdigit():
            number = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                number += self.source[self.position]
                self.position += 1
            self.actual = Token("INT", int(number))

        # Strings
        elif self.source[self.position] == '"':  
            self.position += 1
            stringVal = ""
            while self.position < len(self.source) and self.source[self.position] != '"':
                stringVal += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise ValueError("String não fechada com aspas")
            self.position += 1  # consome " final
            self.actual = Token("STRING", stringVal)  


        # Identificadores e outros
        elif self.source[self.position].isalpha() or self.source[self.position] == '_':
            identifier = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                identifier += self.source[self.position]
                self.position += 1
            if identifier == "manda_ae": # Minha linguagem
                self.actual = Token("PRINT", identifier)
            elif identifier == "fala_comigo": # Minha linguagem
                self.actual = Token("SCAN", identifier)
            elif identifier == "cpa": # Minha linguagem
                self.actual = Token("IF", identifier)
            elif identifier == "caducou": # Minha linguagem
                self.actual = Token("ELSE", identifier)
            elif identifier == "boh": # Minha linguagem
                self.actual = Token("FOR", identifier)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            elif identifier == "papo_que": # Minha linguagem
                self.actual = Token("VAR", identifier)  
            # elif identifier in ["int", "string", "bool"]:
            #     self.actual = Token("TYPE", identifier.upper())  
            elif identifier == "fatos": # Minha linguagem
                self.actual = Token("BOOL", True)  
            elif identifier == "migue": # Minha linguagem
                self.actual = Token("BOOL", False)

            # Minha linguagem
            elif identifier == "sai_fora":
                self.actual = Token("BREAK", identifier)
            elif identifier == "continua":
                self.actual = Token("CONTINUE", identifier)
            # Minha linguagem

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

            else:
                self.actual = Token("IDEN", identifier)

        else:
            raise ValueError(f"Caracter {self.source[self.position]} inválido")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Parser:

    @staticmethod
    def parseStatement(tokenizer):

        if tokenizer.actual.type == "BREAK":
            tokenizer.selectNext()
            return Break()
        elif tokenizer.actual.type == "CONTINUE":
            tokenizer.selectNext()
            return Continue()


        if tokenizer.actual.type == "NL":
            tokenizer.selectNext()
            return NoOp(None)

        elif tokenizer.actual.type == "VAR":         # 'papo_que'
            tokenizer.selectNext()                   # consumiu 'papo_que'

            if tokenizer.actual.type != "IDEN":
                raise ValueError("Esperado identificador após 'papo_que'")

            # monta o nó da variável
            var_name = Iden(tokenizer.actual.value)
            tokenizer.selectNext()                   # consumiu o nome

            # agora obrigatoriamente espera '='
            if tokenizer.actual.type != "EQ":
                raise ValueError(f"Erro de sintaxe: '=' esperado após variável, mas encontrado {tokenizer.actual.type}")
            tokenizer.selectNext()                   # consumiu '='

            # parseia a expressão de inicialização
            init_val = Parser.parseBExpression(tokenizer)
            return VarDec([var_name, init_val])

        elif tokenizer.actual.type == "IDEN":
            iden = tokenizer.actual.value
            tokenizer.selectNext()
            if tokenizer.actual.type != "EQ":
                raise ValueError(f"Erro de sintaxe: '=' esperado, mas encontrado {tokenizer.actual.value}.")
            tokenizer.selectNext()
            child = [Iden(iden) ,Parser.parseBExpression(tokenizer)]
            return Assign(child)

        elif tokenizer.actual.type == "PRINT":
            tokenizer.selectNext()
            if tokenizer.actual.type != "LP":
                raise ValueError(f"Erro de sintaxe: '(' esperado, mas encontrado {tokenizer.actual.value}.")
            else:
                tokenizer.selectNext()
                children = []
                
                while tokenizer.actual.type != "RP":
                    children.append(Parser.parseBExpression(tokenizer))

                if tokenizer.actual.type != "RP":
                    raise ValueError(f"Erro de sintaxe: ')' esperado, mas encontrado {tokenizer.actual.value}.")
                tokenizer.selectNext()
                return Print(children)

        elif tokenizer.actual.type == "FOR":
            tokenizer.selectNext()
            cond = Parser.parseBExpression(tokenizer)
            block = Parser.parseBlockNoEmpty(tokenizer)
            print("DEBUG Criando For com:", cond, block) if DEBUG else None
            return For([cond, block])

        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

        elif tokenizer.actual.type == "IF":           # ‘cpa’
            tokenizer.selectNext()                    # consumiu 'cpa'

            # 1) '(' condição ')'
            if tokenizer.actual.type != "LP":
                raise ValueError(f"Bloco de if mal formado: esperado '(', encontrado {tokenizer.actual.type}.")
            tokenizer.selectNext()
            cond = Parser.parseBExpression(tokenizer)
            if tokenizer.actual.type != "RP":
                raise ValueError(f"Bloco de if mal formado: esperado ')', encontrado {tokenizer.actual.type}.")
            tokenizer.selectNext()

            # 2) then-block
            if tokenizer.actual.type != "LB":
                raise ValueError(f"Bloco de if mal formado: esperado '{{', encontrado {tokenizer.actual.type}.")
            if_block = Parser.parseBlockNoEmpty(tokenizer)

            # 3) pular quebras de linha antes de 'caducou'
            while tokenizer.actual.type == "NL":
                tokenizer.selectNext()
            # 4) bloco else opcional
            if tokenizer.actual.type == "ELSE":
                tokenizer.selectNext()                # consumiu 'caducou'
                if tokenizer.actual.type != "LB":
                    raise ValueError(f"Bloco de else mal formado: esperado '{{', encontrado {tokenizer.actual.type}.")
                else_block = Parser.parseBlockNoEmpty(tokenizer)
                return If([cond, if_block, else_block])

            # sem else
            return If([cond, if_block])
        # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

    @staticmethod
    def parseExpression(tokenizer): 
        resultado = Parser.parseTerm(tokenizer)
        while tokenizer.actual.type in ["PLUS", "MINUS"]:
            operador = tokenizer.actual.value
            tokenizer.selectNext()
            right = Parser.parseTerm(tokenizer)
            resultado = BinOp(operador, [resultado, right])
        return resultado

    @staticmethod
    def parseTerm(tokenizer): 
        resultado = Parser.parseFactor(tokenizer)
        while tokenizer.actual.type in ["MULT", "DIV", "MOD"]:
            operador = tokenizer.actual.value
            tokenizer.selectNext()
            right = Parser.parseFactor(tokenizer)
            resultado = BinOp(operador, [resultado, right])
        return resultado 

    @staticmethod
    def parseFactor(tokenizer):
        unary_ops = []
        while tokenizer.actual.type in ["PLUS", "MINUS", "NOT"]:
            operador = tokenizer.actual.value
            unary_ops.append(operador)
            tokenizer.selectNext()

        if tokenizer.actual.type == "INT":
            resultado = IntVal(tokenizer.actual.value)
            tokenizer.selectNext()
        elif tokenizer.actual.type == "IDEN":
            value = tokenizer.actual.value
            tokenizer.selectNext()
            resultado = Iden(value)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        elif tokenizer.actual.type == "STRING":  
            resultado = StrVal(tokenizer.actual.value)
            tokenizer.selectNext()

        elif tokenizer.actual.type == "BOOL":  
            resultado = BoolVal(tokenizer.actual.value)
            tokenizer.selectNext()
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        elif tokenizer.actual.type == "LP":
            tokenizer.selectNext()
            resultado = Parser.parseBExpression(tokenizer)
            if tokenizer.actual.type != "RP":
                raise ValueError("Parênteses não fecharam")
            tokenizer.selectNext()
        elif tokenizer.actual.type == "SCAN":
            tokenizer.selectNext()
            if tokenizer.actual.type != "LP":
                raise ValueError(f"Erro de sintaxe: '(' esperado, mas encontrado {tokenizer.actual.value}.")
            tokenizer.selectNext()
            if tokenizer.actual.type != "RP":
                raise ValueError(f"Erro de sintaxe: ')' esperado, mas encontrado {tokenizer.actual.value}.")
            tokenizer.selectNext()
            resultado = Scan(None)
        else:
            print("TOKEN INVÁLIDO EM parseFactor:", tokenizer.actual.type, tokenizer.actual.value) if DEBUG else None
            raise ValueError("Sintaxe inválida")

        for op in reversed(unary_ops):
            resultado = UnOp(op, [resultado])

        return resultado

    @staticmethod
    def parseRelExpression(tokenizer):
        node = Parser.parseExpression(tokenizer)
        while tokenizer.actual.type in ["LT", "GT", "EQEQ", "NE", "GE", "LE"]:
            operador = tokenizer.actual.value
            tokenizer.selectNext()
            right = Parser.parseExpression(tokenizer)
            node = BinOp(operador, [node, right])
        return node

    @staticmethod
    def parseBTerm(tokenizer):
        node = Parser.parseRelExpression(tokenizer)
        while tokenizer.actual.type == 'AND':
            operador = tokenizer.actual.value
            tokenizer.selectNext()
            right = Parser.parseRelExpression(tokenizer)
            node = BinOp(operador, [node, right])
        return node
    
    @staticmethod
    def parseBExpression(tokenizer):
        node = Parser.parseBTerm(tokenizer)
        while tokenizer.actual.type == 'OR':
            operador = tokenizer.actual.value
            tokenizer.selectNext()
            right = Parser.parseBTerm(tokenizer)
            node = BinOp(operador, [node, right])
        return node
    
    @staticmethod
    def parseMainBlock(tokenizer):
        # pula quebras de linha iniciais, se houver
        while tokenizer.actual.type == "NL":
            tokenizer.selectNext()

        # 1. programa TEM de começar com '{'
        if tokenizer.actual.type != "LB":
            raise ValueError("Erro de sintaxe: esperado '{' no início do programa" + f", encontrado {tokenizer.actual.type}.")

        # 2. delega o parsing do bloco principal
        return Parser.parseBlockNoEmpty(tokenizer)

    @staticmethod
    def parseBlockNoEmpty(tokenizer):
        statements = []

        if tokenizer.actual.type != "LB":
            raise ValueError("Bloco com chaves '{' esperado" + f", encontrado {tokenizer.actual.type}.")

        tokenizer.selectNext()

        # pula quebra de linha inicial, se houver
        while tokenizer.actual.type == "NL":
            tokenizer.selectNext()

        # erro se o bloco já fecha logo de cara
        if tokenizer.actual.type == "RB":
            raise ValueError("Bloco não pode estar vazio")

        while tokenizer.actual.type != "RB":
            statement = Parser.parseStatement(tokenizer)
            if statement is not None:
                statements.append(statement)

            # consome quebras de linha intermediárias
            while tokenizer.actual.type == "NL":
                tokenizer.selectNext()

            if tokenizer.actual.type == "EOF":
                raise ValueError("Bloco não fechado com '}'")

        tokenizer.selectNext()  # consome RB
        return Block(statements)

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        tokenizer = Tokenizer(code)
        ast = Parser.parseMainBlock(tokenizer)

        if tokenizer.actual.type != "EOF":
            raise ValueError("Expressão inválida")
        return ast

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
    elif len(sys.argv) == 1:
        filename = "teste.txt"
    else:
        raise ValueError("Uso: python script.py [arquivo]")

    try:
        with open(filename, 'r') as file:
            code = file.read()
        
        ast = Parser.run(code)
        st = SymbolTable()
        # print("DEBUG AST Root Node:", ast)
        # print("DEBUG AST Root Children:", ast.children)
        # for c in ast.children:
        #     print("   ->", c, "| children:", getattr(c, "children", None))

        ast.evaluate(st)




    except FileNotFoundError:
        raise ValueError(f"Arquivo {filename} não encontrado")
    except Exception as e:
        raise ValueError(f"Erro ao processar o arquivo: {str(e)}")

if __name__ == "__main__":
    main()