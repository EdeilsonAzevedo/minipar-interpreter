"""
Ponto de entrada do interpretador MiniPar

Este script permite interpretar um programa escrito na linguagem Minipar
por meio de três modos:
1. Tokenização (-tok)
2. Geração e exibição da Árvore Sintática Abstrata (-ast)
3. Execução do programa (modo padrão)
"""

import argparse
import pprint

from minipar.executor import Executor
from minipar.lexer import Lexer
from minipar.parser import Parser
from minipar.semantic import SemanticAnalyzer


def main():
    # Configuração da interface de linha de comando
    parser = argparse.ArgumentParser(
        prog="minipar",
        description="Interpretador da linguagem Minipar"
    )

    # Argumento para tokenização do código-fonte
    parser.add_argument(
        "-tok",
        action="store_true",
        help="Realiza a tokenização do código fonte e exibe os tokens gerados"
    )

    # Argumento para geração e exibição da AST
    parser.add_argument(
        "-ast",
        action="store_true",
        help="Gera e exibe a Árvore Sintática Abstrata (AST)"
    )

    # Caminho do arquivo contendo o programa-fonte
    parser.add_argument(
        "name",
        type=str,
        help="Arquivo contendo o código fonte a ser interpretado"
    )

    # Processamento dos argumentos
    args = parser.parse_args()

    # Leitura do conteúdo do arquivo-fonte
    with open(args.name, "r") as f:
        data = f.read()

    # Instancia o analisador léxico
    lexer = Lexer(data)

    # Modo: Tokenização
    if args.tok:
        for token in lexer.scan():
            print(f"{token} | linha: {lexer.line}")

    # Modo: Geração e exibição da AST
    elif args.ast:
        parser = Parser(lexer)
        semantic = SemanticAnalyzer()
        ast = parser.start()
        semantic.visit(ast)
        pprint.pprint(ast)

    # Modo padrão: análise completa e execução
    else:
        parser = Parser(lexer)
        semantic = SemanticAnalyzer()
        ast = parser.start()
        semantic.visit(ast)

        executor = Executor()
        executor.run(ast)


# Execução do programa, caso seja executado diretamente
if __name__ == "__main__":
    main()
