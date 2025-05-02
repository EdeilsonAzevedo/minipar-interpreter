"""
Módulo de Análise Semântica

Este módulo realiza a verificação semântica da AST gerada pela análise sintática,
identificando inconsistências e erros relacionados ao significado do código.
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from minipar import ast
from minipar import error as err
from minipar.token import DEFAULT_FUNCTION_NAMES


@dataclass
class SemanticAnalyzer:
    """
    Implementação concreta do analisador semântico.

    Attributes:
        context_stack (list[ast.Node]): Pilha de contexto para rastrear escopos.
        function_table (dict[str, ast.FuncDef]): Tabela de funções declaradas.
    """
    context_stack: list[ast.Node] = field(default_factory=list)
    function_table: dict[str, ast.FuncDef] = field(default_factory=dict)

    def __post_init__(self):
        """
        Inicializa a lista de funções padrão disponíveis na linguagem.
        """
        self.default_func_names = list(DEFAULT_FUNCTION_NAMES.keys())

    def visit(self, node: ast.Node):
        """
        Identifica e executa o método de visita correspondente ao tipo do nó.

        Args:
            node (ast.Node): Nó da AST a ser visitado.

        Returns:
            Qualquer valor retornado pelo método de visita.
        """
        meth_name: str = f"visit_{type(node).__name__}"
        visitor = getattr(self, meth_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node: ast.Node):
        """
        Visita um nó genérico da AST, percorrendo seus atributos.

        Args:
            node (ast.Node): Nó genérico da AST.
        """
        self.context_stack.append(node) # Entra no contexto do nó

        for attr in dir(node):
            value = getattr(node, attr)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.Node):
                        self.visit(item)
            elif isinstance(value, ast.Node):
                self.visit(node)

        self.context_stack.pop()  # Sai do contexto do nó

    ###### VISITA DECLARAÇÕES ######

    def visit_Assign(self, node: ast.Assign):
        """
        Verifica a atribuição de valores a variáveis.

        Args:
            node (ast.Assign): Nó de atribuição.
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if not isinstance(node.left, ast.ID):
            raise err.SemanticError("atribuição precisa ser feita para uma variável")
        
        var = node.left
        if left_type != right_type:
            raise err.SemanticError(
                f"(Erro de Tipo) variável {var.token.value} espera {left_type}"
            )

    def visit_Return(self, node: ast.Return):
        """
        Verifica a validade de uma instrução de retorno.

        Args:
            node (ast.Return): Nó de retorno.
        """
        if not any(isinstance(parent, ast.FuncDef) for parent in self.context_stack):
            raise err.SemanticError(
                "return encontrado fora de uma declaração de função"
            )

        function = next(
            (n for n in self.context_stack[::-1] if isinstance(n, ast.FuncDef))
        )
        expr_type = self.visit(node.expr)

        if expr_type != function.return_type:
            raise err.SemanticError(
                f"retorno em {function.name} tem tipo diferente do definido"
            )

    def visit_Break(self, _: ast.Break):
        """
        Verifica se a instrução 'break' está dentro de um loop.
        """
        if not any(isinstance(parent, ast.While) for parent in self.context_stack):
            raise err.SemanticError(
                "break encontrado fora de uma declaração de um loop"
            )

    def visit_Continue(self, _: ast.Continue):
        """
        Verifica se a instrução 'continue' está dentro de um loop.
        """
        if not any(isinstance(parent, ast.While) for parent in self.context_stack):
            raise err.SemanticError(
                "continue encontrado fora de uma declaração de um loop"
            )

    def visit_FuncDef(self, node: ast.FuncDef):
        """
        Verifica a declaração de uma função.

        Args:
            node (ast.FuncDef): Nó de definição de função.
        """
        if any(
            isinstance(parent, (ast.If, ast.While, ast.Par))
            for parent in self.context_stack
        ):
            raise err.SemanticError(
                "não é possível declarar funções dentro de escopos locais"
            )

        if node.name not in self.function_table:
            self.function_table[node.name] = node

        self.generic_visit(node)

    def visit_block(self, block: ast.Body):
        """
        Visita um bloco de instruções.

        Args:
            block (ast.Body): Bloco de instruções.
        """
        for node in block:
            self.visit(node)

    def visit_If(self, node: ast.If):
        """
        Verifica a validade de uma instrução condicional.

        Args:
            node (ast.If): Nó de instrução condicional.
        """
        cond_type = self.visit(node.condition)

        if cond_type != "BOOL":
            raise err.SemanticError(f"esperado BOOL, mas encontrado {cond_type}")

        self.context_stack.append(node)
        self.visit_block(node.body)
        if node.else_stmt:
            self.visit_block(node.else_stmt)
        self.context_stack.pop()

    def visit_While(self, node: ast.While):
        """
        Verifica a validade de um laço de repetição.

        Args:
            node (ast.While): Nó de laço de repetição.
        """
        cond_type = self.visit(node.condition)

        if cond_type != "BOOL":
            raise err.SemanticError(f"esperado BOOL, mas encontrado {cond_type}")

        self.context_stack.append(node)
        self.visit_block(node.body)
        self.context_stack.pop()

    def visit_Par(self, node: ast.Par):
        """
        Verifica a validade de um bloco de execução paralela.

        Args:
            node (ast.Par): Nó de execução paralela.
        """
        if any(not isinstance(inst, ast.Call) for inst in node.body):
            raise err.SemanticError(
                "esperado apenas funções em um bloco de execução paralela"
            )

    def visit_CChannel(self, node: ast.CChannel):
        """
        Verifica a validade de um canal de comunicação cliente.

        Args:
            node (ast.CChannel): Nó de canal cliente.
        """
        localhost_type = self.visit(node._localhost)

        if localhost_type != "STRING":
            raise err.SemanticError(f"localhost em {node.name} precisa ser STRING")

        port_type = self.visit(node._port)

        if port_type != "NUMBER":
            raise err.SemanticError(f"port em {node.name} precisa ser NUMBER")

    def visit_SChannel(self, node: ast.SChannel):
        """
        Verifica a validade de um canal de comunicação servidor.

        Args:
            node (ast.SChannel): Nó de canal servidor.
        """
        func = self.function_table[node.func_name]

        if func.return_type != "STRING":
            raise err.SemanticError(
                f"função base de {node.name} precisa ter retorno STRING"
            )

        if len(func.params) != 1 or list(func.params.values())[0][0] != "STRING":
            raise err.SemanticError(
                f"função base de {node.name} precisa ter exatamente 1 parâmetro STRING"
            )

        description_type = self.visit(node.description)

        if description_type != "STRING":
            raise err.SemanticError(f"localhost em {node.name} precisa ser STRING")

        localhost_type = self.visit(node._localhost)

        if localhost_type != "STRING":
            raise err.SemanticError(f"localhost em {node.name} precisa ser STRING")

        port_type = self.visit(node._port)

        if port_type != "NUMBER":
            raise err.SemanticError(f"port em {node.name} precisa ser NUMBER")

    ###### VISITA EXPREÇÕES #######

    def visit_Constant(self, node: ast.Constant):
        """
        Retorna o tipo de uma constante.

        Args:
            node (ast.Constant): Nó de constante.

        Returns:
            str: Tipo da constante.
        """
        return node.type

    def visit_ID(self, node: ast.ID):
        """
        Retorna o tipo de um identificador.

        Args:
            node (ast.ID): Nó de identificador.

        Returns:
            str: Tipo do identificador.
        """
        return node.type

    def visit_Access(self, node: ast.Access):
        """
        Verifica o acesso a índices de variáveis.

        Args:
            node (ast.Access): Nó de acesso.

        Returns:
            str: Tipo do acesso.

        Raises:
            err.SemanticError: Se o acesso não for válido.
        """
        if node.type != "STRING":
            raise err.SemanticError("Acesso por index é válido apenas em strings")
        return node.type

    def visit_Logical(self, node: ast.Logical):
        """
        Verifica a validade de uma operação lógica.

        Args:
            node (ast.Logical): Nó de operação lógica.

        Returns:
            str: Tipo da operação lógica.
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if left_type != "BOOL" or right_type != "BOOL":
            raise err.SemanticError(
                f"(Erro de Tipo) Esperado BOOL, mas encontrado {left_type} e {right_type} na operação {node.token.value}"
            )

        return "BOOL"

    def visit_Relational(self, node: ast.Relational):
        """
        Verifica a validade de uma operação relacional.

        Args:
            node (ast.Relational): Nó de operação relacional.

        Returns:
            str: Tipo da operação relacional.
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.token.value in {"==", "!="}:
            if left_type != right_type:
                raise err.SemanticError(
                    f"(Erro de Tipo) Esperado tipos iguais, mas encontrado {left_type} e {right_type} na operação {node.token.value}"
                )
        else:
            if left_type != "NUMBER" or right_type != "NUMBER":
                raise err.SemanticError(
                    f"(Erro de Tipo) Esperado NUMBER, mas encontrado {left_type} e {right_type} na operação {node.token.value}"
                )

        return "BOOL"

    def visit_Arithmetic(self, node: ast.Arithmetic):
        """
        Verifica a validade de uma operação aritmética.

        Args:
            node (ast.Arithmetic): Nó de operação aritmética.

        Returns:
            str: Tipo da operação aritmética.
        """
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if node.token.value == "+":
            if left_type != right_type:
                raise err.SemanticError(
                    f"(Erro de Tipo) Esperado tipos iguais, mas encontrado {left_type} e {right_type} na operação {node.token.value}"
                )
        else:
            if left_type != "NUMBER" or right_type != "NUMBER":
                raise err.SemanticError(
                    f"(Erro de Tipo) Esperado NUMBER, mas encontrado {left_type} e {right_type} na operação {node.token.value}"
                )

        return left_type

    def visit_Unary(self, node: ast.Unary):
        """
        Verifica a validade de uma operação unária.

        Args:
            node (ast.Unary): Nó de operação unária.

        Returns:
            str: Tipo da operação unária.
        """
        expr_type = self.visit(node.expr)

        if node.token.tag == "-":
            if expr_type != "NUMBER":
                raise err.SemanticError(
                    f"(Erro de Tipo) Esperado NUMBER, mas encontrado {expr_type} na operação {node.token.value}"
                )
        elif node.token.tag == "!":
            if expr_type != "BOOL":
                raise err.SemanticError(
                    f"(Erro de Tipo) Esperado BOOL, mas encontrado {expr_type} na operação {node.token.value}"
                )

        return expr_type

    def visit_Call(self, node: ast.Call):
        """
        Verifica a validade de uma chamada de função.

        Args:
            node (ast.Call): Nó de chamada de função.

        Returns:
            str: Tipo de retorno da função chamada.
        """
        func_name = node.oper if node.oper else node.token.value

        for arg in node.args:
            self.visit(arg)

        function: ast.FuncDef | None = self.function_table.get(str(func_name))

        if not function:
            if func_name not in self.default_func_names:
                raise err.SemanticError(f"função {func_name} não declarada")
            else:
                return DEFAULT_FUNCTION_NAMES[func_name]

        nondefault_params = sum(
            [value[1] is not None for value in function.params.values()]
        )
        call_args = len(node.args)

        if nondefault_params > call_args:
            raise err.SemanticError(
                f"Esperado {nondefault_params} argumentos, mas encontrado {call_args}"
            )

        return function.return_type
