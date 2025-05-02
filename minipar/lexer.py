"""
Módulo de Análise Léxica

Este módulo contém classes responsáveis por realizar a análise léxica
do código-fonte escrito na linguagem Minipar, transformando-o em um
conjunto de tokens que podem ser processados posteriormente.
"""

import re
from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass, field

from minipar.token import TOKEN_REGEX, Token

type NextToken = Generator[tuple[Token, int], None, None]


@dataclass
class Lexer():
    """
    Implementação concreta da análise léxica para a linguagem Minipar.

    Attributes:
        data (str): Código-fonte de entrada.
        line (int): Número da linha atual durante a análise.
        token_table (dict): Mapeamento de palavras reservadas e tipos.
    """

    data: str
    line: int = 1
    token_table: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        """
        Inicializa a tabela de palavras reservadas e tipos da linguagem.
        """
        self.token_table.update({
            "number": "TYPE",
            "bool": "TYPE",
            "string": "TYPE",
            "void": "TYPE",
            "true": "TRUE",
            "false": "FALSE",
        })

        # Palavras reservadas
        self.token_table.update({
            "func": "FUNC",
            "while": "WHILE",
            "if": "IF",
            "else": "ELSE",
            "return": "RETURN",
            "break": "BREAK",
            "continue": "CONTINUE",
            "par": "PAR",
            "seq": "SEQ",
            "c_channel": "C_CHANNEL",
            "s_channel": "S_CHANNEL",
        })

    def scan(self):
        """
        Realiza a análise léxica do código-fonte, gerando tokens.

        Yields:
            tuple[Token, int]: Um token e o número da linha correspondente.
        """
        # Compila as expressões regulares para correspondência de padrões
        compiled_regex = re.compile(TOKEN_REGEX)

        # Itera sobre as correspondências encontradas no código-fonte
        for match in compiled_regex.finditer(self.data):
            # Obtém o tipo e o valor do padrão correspondente
            token_type = match.lastgroup
            token_value = match.group()

            # Ignora espaços em branco e comentários
            if token_type in {"WHITESPACE", "SCOMMENT"}:
                continue
            elif token_type == "MCOMMENT":
                # Atualiza o número de linhas para comentários multilinha
                self.line += token_value.count("\n")
                continue
            elif token_type == "NEWLINE":
                # Incrementa o contador de linhas para quebras de linha
                self.line += 1
                continue
            elif token_type == "NAME":
                # Verifica se o nome corresponde a uma palavra reservada ou tipo
                token_type = self.token_table.get(token_value, "ID")
            elif token_type == "STRING":
                # Remove aspas duplas do valor da string
                token_value = token_value.replace('"', "")
            elif token_type == "OTHER":
                # Define o tipo como o próprio valor para padrões desconhecidos
                token_type = token_value

            # Gera o token e o número da linha correspondente
            yield Token(token_type, token_value), self.line  # type: ignore