"""
Módulo de Tabelas de Símbolos e Variáveis

Este módulo define as classes responsáveis por gerenciar o acesso
a variáveis e símbolos, considerando os diferentes escopos durante
a análise sintática e a execução do programa.
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class Symbol:
    """
    Representa um símbolo na tabela de símbolos.

    Attributes:
        var (str): Nome da variável associada ao símbolo.
        type (str): Tipo da variável associada ao símbolo.
    """

    var: str
    type: str


@dataclass
class SymTable:
    """
    Representa a tabela de símbolos, que armazena informações
    sobre variáveis e seus tipos em um determinado escopo.

    Attributes:
        table (dict): Dicionário que mapeia nomes de variáveis para símbolos.
        prev (Optional[SymTable]): Referência à tabela de escopo superior.
    """

    table: dict[str, Symbol] = field(default_factory=dict)
    prev: Optional["SymTable"] = None

    def insert(self, string: str, symbol: Symbol) -> bool:
        """
        Insere um símbolo na tabela, caso ele ainda não exista.

        Args:
            string (str): Nome da variável.
            symbol (Symbol): Símbolo a ser inserido.

        Returns:
            bool: True se a inserção foi bem-sucedida, False caso contrário.
        """
        if string in self.table:
            return False
        self.table[string] = symbol
        return True

    def find(self, string: str) -> Optional[Symbol]:
        """
        Busca um símbolo na tabela pelo nome, considerando escopos superiores.

        Args:
            string (str): Nome da variável a ser buscada.

        Returns:
            Optional[Symbol]: O símbolo encontrado ou None se não existir.
        """
        current_scope = self
        while current_scope:
            symbol = current_scope.table.get(string)
            if symbol:
                return symbol
            current_scope = current_scope.prev
        return None


@dataclass
class VarTable:
    """
    Representa a tabela de variáveis, que armazena os valores
    associados às variáveis em um determinado escopo.

    Attributes:
        table (dict): Dicionário que mapeia nomes de variáveis para seus valores.
        prev (Optional[VarTable]): Referência à tabela de escopo superior.
    """

    table: dict[str, Any] = field(default_factory=dict)
    prev: Optional["VarTable"] = None

    def find(self, string: str) -> Optional["VarTable"]:
        """
        Busca uma variável na tabela pelo nome, considerando escopos superiores.

        Args:
            string (str): Nome da variável a ser buscada.

        Returns:
            Optional[VarTable]: A tabela onde a variável foi encontrada ou None.
        """
        current_scope = self
        while current_scope:
            value = current_scope.table.get(string)
            if value is None:
                current_scope = current_scope.prev
                continue
            return current_scope
