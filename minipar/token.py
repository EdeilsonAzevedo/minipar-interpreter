"""
Módulo de Tokens

Este módulo define a classe Token e as constantes necessárias para
a análise léxica da linguagem Minipar. Ele inclui os padrões de
tokens, declarações e mapeamentos utilizados durante o processo.
"""

from dataclasses import dataclass

# Padrões de correspondência para os tokens
TOKEN_PATTERNS = [
    ("NAME", r"[A-Za-z_][A-Za-z0-9_]*"),  # Identificadores e palavras reservadas
    ("NUMBER", r"\b\d+\.\d+|\.\d+|\d+\b"),  # Números inteiros e decimais
    ("RARROW", r"->"),  # Operador de seta
    ("STRING", r'"([^"]*)"'),  # Literais de string
    ("SCOMMENT", r"#.*"),  # Comentários de uma linha
    ("MCOMMENT", r"/\*[\s\S]*?\*/"),  # Comentários multilinha
    ("OR", r"\|\|"),  # Operador lógico OR
    ("AND", r"&&"),  # Operador lógico AND
    ("EQ", r"=="),  # Operador de igualdade
    ("NEQ", r"!="),  # Operador de diferença
    ("LTE", r"<="),  # Operador menor ou igual
    ("GTE", r">="),  # Operador maior ou igual
    ("NEWLINE", r"\n"),  # Quebras de linha
    ("WHITESPACE", r"\s+"),  # Espaços em branco
    ("OTHER", r"."),  # Qualquer outro caractere
]

# Conjunto de tokens que representam declarações na linguagem
STATEMENT_TOKENS = {
    "ID",
    "FUNC",
    "IF",
    "ELSE",
    "WHILE",
    "RETURN",
    "BREAK",
    "CONTINUE",
    "SEQ",
    "PAR",
    "C_CHANNEL",
    "S_CHANNEL",
}

# Mapeamento de tipos de retorno para funções padrão da linguagem
DEFAULT_FUNCTION_NAMES = {
    "print": "VOID",
    "input": "STRING",
    "sleep": "VOID",
    "to_number": "NUMBER",
    "to_string": "STRING",
    "to_bool": "BOOL",
    "send": "STRING",
    "close": "VOID",
    "len": "NUMBER",
    "isalpha": "BOOL",
    "isnum": "BOOL",
}

# Expressão regular combinada para análise léxica
TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_PATTERNS)


@dataclass
class Token:
    """
    Representa um token gerado durante a análise léxica.

    Attributes:
        tag (str): Identifica o tipo do token.
        value (str): Armazena o valor associado ao token.
    """

    tag: str
    value: str

    def __repr__(self):
        """
        Retorna uma representação legível do token, exibindo seu valor e tipo.
        """
        return f"{{{self.value}, {self.tag}}}"