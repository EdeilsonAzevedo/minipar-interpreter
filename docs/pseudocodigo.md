# LEXER
    função scan():
        compila regex a partir de TOKEN_PATTERNS

        para cada match (correspondência) no texto fonte:
            tipo_token ← tipo da correspondência
            valor_token ← valor extraído da correspondência

            se tipo_token é "WHITESPACE" ou "SCOMMENT":
                ignora (são irrelevantes para a gramática)
            
            se tipo_token é "MCOMMENT":
                conta quantas quebras de linha existem no comentário
                incrementa contador de linha
                continua

            se tipo_token é "NEWLINE":
                incrementa contador de linha
                continua

            se tipo_token é "NAME":
                se valor_token está na tabela de palavras-chave:
                    tipo_token ← token_table[valor_token]
                senão:
                    tipo_token ← "ID"

            se tipo_token é "STRING":
                remove aspas duplas do valor_token

            se tipo_token é "OTHER":
                trata o caractere como um símbolo literal (ex: +, -, =, etc)
                tipo_token ← valor_token

            cria um novo Token(tipo_token, valor_token)
            yield (Token, linha_atual)

# SINTATICO
    classe Parser:
        método __init__(lexer):
            lexer ← lexer.scan()
            lookahead, lineno ← próximo(lexer)
            symtable ← nova SymTable()
            para cada função padrão:
                symtable.insert(nome, Symbol(nome, "FUNC"))

        método match(tag):
            se tag == lookahead.tag:
                lookahead, lineno ← próximo(lexer) ou EOF
                retorna True
            retorna False

        método start():
            retorna program()

        método program():
            retorna Module(stmts())

        método stmts():
            body ← []
            enquanto lookahead.tag ∈ TOKENS_DE_INSTRUÇÃO:
                body.append(stmt())
            se lookahead.tag ∉ {"}", "EOF"}:
                lança SyntaxError
            retorna body

        método stmt():
            escolha lookahead.tag:
                caso "ID":
                    left ← local()
                    se left é Call:
                        retorna left
                    se não match("="):
                        erro "esperado '='"
                    right ← disjunction()
                    retorna Assign(left, right)

                caso "FUNC":
                    match("FUNC")
                    name ← var("FUNC")
                    params ← params()
                    se não match("RARROW"):
                        erro
                    tipo ← lookahead.value
                    match("TYPE")
                    body ← block(params)
                    retorna FuncDef(name, tipo, params, body)

                caso "RETURN":
                    match("RETURN")
                    expr ← disjunction()
                    retorna Return(expr)

                caso "BREAK":
                    match("BREAK")
                    retorna Break()

                caso "CONTINUE":
                    match("CONTINUE")
                    retorna Continue()

                caso "IF":
                    match("IF")
                    match("(")
                    cond ← disjunction()
                    match(")")
                    body ← block()
                    se lookahead.tag == "ELSE":
                        match("ELSE")
                        else_body ← block()
                    retorna If(cond, body, else_body)

                caso "WHILE":
                    match("WHILE")
                    match("(")
                    cond ← disjunction()
                    match(")")
                    body ← block()
                    retorna While(cond, body)

                caso "SEQ":
                    match("SEQ")
                    retorna Seq(block())

                caso "PAR":
                    match("PAR")
                    retorna Par(block())

                caso "C_CHANNEL":
                    match("C_CHANNEL")
                    name ← var("C_CHANNEL")
                    match("{")
                    host ← ari()
                    match(",")
                    port ← ari()
                    match("}")
                    retorna CChannel(name, host, port)

                caso "S_CHANNEL":
                    match("S_CHANNEL")
                    name ← var("S_CHANNEL")
                    match("{")
                    func ← var("REF")
                    match(",")
                    descr ← ari()
                    match(",")
                    host ← ari()
                    match(",")
                    port ← ari()
                    match("}")
                    retorna SChannel(name, host, port, func, descr)

                caso default:
                    erro "token inválido"

        método block(params = None):
            match("{")
            salva symtable atual
            symtable ← novo escopo com `prev`
            se params:
                para cada (nome, tipo) em params:
                    symtable.insert(nome, Symbol(nome, tipo))
            body ← stmts()
            match("}")
            restaura symtable
            retorna body

        método params():
            match("(")
            params ← {}
            se lookahead ≠ ")":
                adiciona param()
                enquanto match(","):
                    adiciona param()
            match(")")
            retorna params

        método param():
            nome ← lookahead.value
            match("ID"), match(":"), tipo ← lookahead.value
            match("TYPE")
            se match("="):
                default ← disjunction()
            senão:
                default ← None
            retorna nome, (tipo, default)

        método args():
            args ← []
            se lookahead ≠ ")":
                args.append(disjunction())
                enquanto match(","):
                    args.append(disjunction())
            retorna args

        método disjunction():
            left ← conjunction()
            enquanto match("OR"):
                right ← conjunction()
                left ← Logical("BOOL", "||", left, right)
            retorna left

        método conjunction():
            left ← equality()
            enquanto match("AND"):
                right ← equality()
                left ← Logical("BOOL", "&&", left, right)
            retorna left

        método equality():
            left ← comparison()
            enquanto match("EQ") ou match("NEQ"):
                op ← lookahead.tag
                right ← comparison()
                left ← Relational("BOOL", op, left, right)
            retorna left

        método comparison():
            left ← ari()
            enquanto lookahead.tag ∈ {">", "<", "GTE", "LTE"}:
                op ← lookahead.tag
                match(op)
                right ← ari()
                left ← Relational("BOOL", op, left, right)
            retorna left

        método ari():
            left ← term()
            enquanto lookahead.tag ∈ {"+", "-"}:
                op ← lookahead.tag
                match(op)
                right ← term()
                left ← Arithmetic(left.type, op, left, right)
            retorna left

        método term():
            left ← unary()
            enquanto lookahead.tag ∈ {"*", "/", "%"}:
                op ← lookahead.tag
                match(op)
                right ← unary()
                left ← Arithmetic(left.type, op, left, right)
            retorna left

        método unary():
            se lookahead.tag ∈ {"!", "-"}:
                op ← lookahead.tag
                match(op)
                expr ← unary()
                retorna Unary("BOOL", op, expr)
            senão:
                retorna primary()

        método local():
            token ← lookahead.value
            match("ID")
            se match(":"):
                tipo ← lookahead.value
                match("TYPE")
                symtable.insert(token, Symbol(token, tipo))
                retorna ID(tipo, token, decl=True)

            símbolo ← symtable.find(token)
            se símbolo não existe: erro
            expr ← ID(símbolo.type, token)

            enquanto True:
                se match("["):
                    index ← ari()
                    match("]")
                    expr ← Access(expr.type, token, expr, index)
                se match("."):
                    nome ← lookahead.value
                    match("ID")
                se match("("):
                    args ← args()
                    match(")")
                    expr ← Call("FUNC", token, expr, args)
                senão:
                    break
            retorna expr

        método primary():
            se match("("):
                expr ← disjunction()
                match(")")
                retorna expr
            se lookahead.tag == "ID":
                retorna local()
            se lookahead.tag == "NUMBER":
                valor ← lookahead.value
                match("NUMBER")
                retorna Constant("NUMBER", valor)
            se lookahead.tag == "STRING":
                valor ← lookahead.value
                match("STRING")
                retorna Constant("STRING", valor)
            se lookahead.tag ∈ {"TRUE", "FALSE"}:
                valor ← lookahead.value
                match(lookahead.tag)
                retorna Constant("BOOL", valor)
            erro

        método var(tipo):
            token ← lookahead.value
            match("ID")
            símbolo ← symtable.find(token)
            se tipo == "REF":
                se símbolo não existe: erro
            se tipo ∈ {"FUNC", "C_CHANNEL", "S_CHANNEL"}:
                se símbolo existe: erro
            symtable.insert(token, Symbol(token, tipo))
            retorna token

# SEMANTICO
    classe SemanticAnalyzer:
        context_stack ← []
        function_table ← {}

        método __post_init__():
            default_func_names ← nomes das funções padrão

        método visit(node):
            chama o método correspondente ao tipo do nó:
                ex: visit_Assign(node), visit_If(node), etc.
            se não existir, chama generic_visit(node)

        método generic_visit(node):
            context_stack.push(node)
            para cada atributo em node:
                se for lista de nós:
                    para cada subnó:
                        se é um nó, aplica visit(subnó)
                se for um nó:
                    aplica visit(subnó)
            context_stack.pop()

        método visit_Assign(node):
            left_type ← visit(node.left)
            right_type ← visit(node.right)
            se node.left não é ID:
                erro semântico: "atribuição inválida"
            se left_type ≠ right_type:
                erro semântico: "tipos incompatíveis na atribuição"

        método visit_Return(node):
            se nenhum elemento em context_stack é FuncDef:
                erro semântico: "return fora de função"
            função ← último FuncDef na pilha (mais recente)
            expr_type ← visit(node.expr)
            se expr_type ≠ função.return_type:
                erro semântico: "tipo de retorno inválido"

        método visit_Break(_):
            se nenhum elemento em context_stack é While:
                erro semântico: "break fora de loop"

        método visit_Continue(_):
            se nenhum elemento em context_stack é While:
                erro semântico: "continue fora de loop"

        método visit_FuncDef(node):
            se existe If, While ou Par na pilha:
                erro semântico: "função em escopo inválido"
            se node.name não em function_table:
                function_table[node.name] ← node
            generic_visit(node)

        método visit_If(node):
            cond_type ← visit(node.condition)
            se cond_type ≠ "BOOL":
                erro semântico: "condição de if não booleana"
            context_stack.push(node)
            visita node.body
            se node.else_stmt:
                visita node.else_stmt
            context_stack.pop()

        método visit_While(node):
            cond_type ← visit(node.condition)
            se cond_type ≠ "BOOL":
                erro semântico: "condição de while não booleana"
            context_stack.push(node)
            visita node.body
            context_stack.pop()

        método visit_Par(node):
            para cada inst em node.body:
                se não for Call:
                    erro semântico: "somente chamadas permitidas em blocos PAR"

        método visit_CChannel(node):
            host_type ← visit(node._localhost)
            port_type ← visit(node._port)
            se host_type ≠ "STRING":
                erro semântico
            se port_type ≠ "NUMBER":
                erro semântico

        método visit_SChannel(node):
            func ← function_table[node.func_name]
            se func.return_type ≠ "STRING":
                erro semântico
            se número de parâmetros ≠ 1 ou tipo ≠ "STRING":
                erro semântico
            verifica types de description, localhost e port:
                se incorretos, lança erro

        método visit_Constant(node):
            retorna node.type

        método visit_ID(node):
            retorna node.type

        método visit_Access(node):
            se node.type ≠ "STRING":
                erro semântico: "acesso por índice só permitido em strings"
            retorna node.type

        método visit_Logical(node):
            left_type ← visit(node.left)
            right_type ← visit(node.right)
            se algum ≠ "BOOL":
                erro semântico
            retorna "BOOL"

        método visit_Relational(node):
            left_type ← visit(node.left)
            right_type ← visit(node.right)
            se operador ∈ {"==", "!="}:
                se left_type ≠ right_type:
                    erro semântico
            senão:
                se algum ≠ "NUMBER":
                    erro semântico
            retorna "BOOL"

        método visit_Arithmetic(node):
            left_type ← visit(node.left)
            right_type ← visit(node.right)
            se operador == "+":
                se left_type ≠ right_type:
                    erro semântico
            senão:
                se algum ≠ "NUMBER":
                    erro semântico
            retorna left_type

        método visit_Unary(node):
            expr_type ← visit(node.expr)
            se operador == "-":
                se expr_type ≠ "NUMBER":
                    erro semântico
            se operador == "!":
                se expr_type ≠ "BOOL":
                    erro semântico
            retorna expr_type

        método visit_Call(node):
            func_name ← node.oper se existir, senão node.token.value
            para cada argumento em node.args:
                aplica visit(argumento)
            se func_name ∉ function_table e ∉ funções padrão:
                erro semântico: "função não declarada"
            se for função padrão:
                retorna tipo associado
            func ← function_table[func_name]
            se número de argumentos < número de parâmetros sem default:
                erro semântico
            retorna func.return_type
