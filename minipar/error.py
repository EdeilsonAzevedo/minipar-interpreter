class SyntaxError(Exception):
    """
    Indica um erro de sintaxe identificado durante a análise sintática.

    Este erro ocorre quando o código fonte contém construções que
    violam as regras gramaticais definidas pela linguagem.
    """

    def __init__(self, line: int, msg: str):
        super().__init__(f"Erro de Sintaxe na linha {line}: {msg}")


class SemanticError(Exception):
    """
    Indica um erro semântico identificado durante a análise semântica.

    Este erro ocorre quando o código fonte está sintaticamente correto,
    mas apresenta inconsistências ou violações de regras semânticas,
    como uso de tipos incompatíveis ou variáveis não declaradas.
    """

    def __init__(self, msg: str):
        super().__init__(f"Erro Semântico: {msg}")


class RunTimeError(Exception):
    """
    Indica um erro ocorrido durante a execução do programa.

    Este erro é levantado quando ocorre uma falha em tempo de execução,
    como divisão por zero, acesso inválido à memória ou outros problemas
    relacionados à execução dinâmica do código.
    """

    def __init__(self, msg: str):
        super().__init__(f"Erro em Tempo de Execução: {msg}")
