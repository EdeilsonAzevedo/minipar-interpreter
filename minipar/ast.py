"""
AST - Representação Estrutural do Código Fonte

Este módulo define os nós que compõem a Árvore Sintática Abstrata (AST) da linguagem.
Os nós representam instruções (statements) e expressões (expressions), descrevendo
suas relações e tipos de forma estruturada.
"""

from dataclasses import dataclass
from typing import Optional, Union, List, Dict, Tuple
from minipar.token import Token


class Node:
    """
    Representa um nó genérico na Árvore Sintática Abstrata (AST).
    """
    pass


@dataclass
class Statement(Node):
    """
    Representa uma instrução na AST.
    """
    pass


@dataclass
class Expression(Node):
    """
    Representa uma expressão na AST.

    Attributes:
        type (str): Tipo de retorno da expressão.
        token (Token): Token associado à expressão.
    """
    type: str
    token: Token

    @property
    def name(self) -> Optional[str]:
        """
        Retorna o valor do token associado à expressão, se disponível.
        """
        return self.token.value if self.token else None

    def to_dict(self) -> Dict[str, Union[str, Token]]:
        """
        Converte a expressão em um dicionário contendo seus atributos principais.
        """
        return {"type": self.type, "token": self.token}


#### TYPES #####

Body = List[Union[Statement, Expression]]  # Corpo de instruções ou expressões.
Arguments = List[Expression]  # Lista de argumentos de uma chamada.
Parameters = Dict[str, Tuple[str, Optional[Expression]]]  # Parâmetros de funções.


##### EXPRESSIONS #####


@dataclass
class Constant(Expression):
    """
    Representa uma constante na AST.
    """
    pass


@dataclass
class ID(Expression):
    """
    Representa um identificador na AST.

    Attributes:
        decl (bool): Indica se o identificador é uma declaração.
    """
    decl: bool = False


@dataclass
class Access(Expression):
    """
    Representa o acesso a um membro ou atributo.

    Attributes:
        id (ID): Identificador do membro.
        expr (Expression): Expressão associada ao acesso.
    """
    id: ID
    expr: Expression


@dataclass
class Logical(Expression):
    """
    Representa uma operação lógica.

    Attributes:
        left (Expression): Operando esquerdo.
        right (Expression): Operando direito.
    """
    left: Expression
    right: Expression


@dataclass
class Relational(Expression):
    """
    Representa uma operação relacional.

    Attributes:
        left (Expression): Operando esquerdo.
        right (Expression): Operando direito.
    """
    left: Expression
    right: Expression


@dataclass
class Arithmetic(Expression):
    """
    Representa uma operação aritmética.

    Attributes:
        left (Expression): Operando esquerdo.
        right (Expression): Operando direito.
    """
    left: Expression
    right: Expression


@dataclass
class Unary(Expression):
    """
    Representa uma operação unária.

    Attributes:
        expr (Expression): Operando da operação.
    """
    expr: Expression


@dataclass
class Call(Expression):
    """
    Representa uma chamada de função.

    Attributes:
        id (Optional[ID]): Identificador da função chamada.
        args (Arguments): Lista de argumentos da chamada.
        oper (Optional[str]): Operador associado à chamada, se aplicável.
    """
    id: Optional[ID]
    args: Arguments
    oper: Optional[str]


@dataclass
class Cast(Expression):
    """
    Representa uma conversão de tipo.

    Attributes:
        expr (Expression): Expressão a ser convertida.
        target_type (str): Tipo alvo da conversão.
    """
    expr: Expression
    target_type: str


##### STATEMENTS #####


@dataclass
class Module(Statement):
    """
    Representa um módulo contendo uma lista de instruções.

    Attributes:
        stmts (Optional[Body]): Lista de instruções do módulo.
    """
    stmts: Optional[Body]


@dataclass
class Assign(Statement):
    """
    Representa uma atribuição.

    Attributes:
        left (Expression): Lado esquerdo da atribuição.
        right (Expression): Lado direito da atribuição.
    """
    left: Expression
    right: Expression


@dataclass
class Return(Statement):
    """
    Representa uma instrução de retorno.

    Attributes:
        expr (Expression): Expressão a ser retornada.
    """
    expr: Expression


@dataclass
class Break(Statement):
    """
    Representa uma instrução de interrupção de laço.
    """
    pass


@dataclass
class Continue(Statement):
    """
    Representa uma instrução de continuação de laço.
    """
    pass


@dataclass
class FuncDef(Statement):
    """
    Representa a definição de uma função.

    Attributes:
        name (str): Nome da função.
        return_type (str): Tipo de retorno da função.
        params (Parameters): Parâmetros da função.
        body (Body): Corpo da função.
    """
    name: str
    return_type: str
    params: Parameters
    body: Body


@dataclass
class If(Statement):
    """
    Representa uma instrução condicional.

    Attributes:
        condition (Expression): Condição do bloco.
        body (Body): Corpo do bloco condicional.
        else_stmt (Optional[Body]): Corpo do bloco else, se aplicável.
    """
    condition: Expression
    body: Body
    else_stmt: Optional[Body]


@dataclass
class While(Statement):
    """
    Representa um laço de repetição.

    Attributes:
        condition (Expression): Condição do laço.
        body (Body): Corpo do laço.
    """
    condition: Expression
    body: Body


@dataclass
class Par(Statement):
    """
    Representa um bloco paralelo.

    Attributes:
        body (Body): Corpo do bloco paralelo.
    """
    body: Body


@dataclass
class Seq(Statement):
    """
    Representa um bloco sequencial.

    Attributes:
        body (Body): Corpo do bloco sequencial.
    """
    body: Body


@dataclass
class Channel(Statement):
    """
    Representa um canal de comunicação.

    Attributes:
        name (str): Nome do canal.
        _localhost (Expression): Expressão representando o localhost.
        _port (Expression): Expressão representando a porta.
    """
    name: str
    _localhost: Expression
    _port: Expression

    @property
    def localhost(self) -> str:
        """
        Retorna o valor do localhost.
        """
        return self._localhost.token.value

    @property
    def localhost_node(self) -> Expression:
        """
        Retorna o nó associado ao localhost.
        """
        return self._localhost

    @property
    def port(self) -> str:
        """
        Retorna o valor da porta.
        """
        return self._port.token.value

    @property
    def port_node(self) -> Expression:
        """
        Retorna o nó associado à porta.
        """
        return self._port


@dataclass
class SChannel(Channel):
    """
    Representa um canal de comunicação do tipo servidor.

    Attributes:
        func_name (str): Nome da função associada ao canal.
        description (Expression): Descrição do canal.
    """
    func_name: str
    description: Expression


@dataclass
class CChannel(Channel):
    """
    Representa um canal de comunicação do tipo cliente.
    """
    pass


@dataclass
class NoOp(Statement):
    """
    Representa uma instrução vazia.
    """
    pass


@dataclass
class Assert(Statement):
    """
    Representa uma instrução de asserção.

    Attributes:
        condition (Expression): Condição a ser avaliada.
        message (Optional[Expression]): Mensagem opcional associada à asserção.
    """
    condition: Expression
    message: Optional[Expression]
