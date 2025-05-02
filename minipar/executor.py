import socket
import threading
from abc import ABC, abstractmethod
from copy import deepcopy
from dataclasses import dataclass, field
from enum import Enum
from time import sleep

from minipar import ast
from minipar import error as err
from minipar.symtable import VarTable
from minipar.token import Token


class commands(Enum):
    """
    Enumeração que define comandos especiais utilizados durante a execução.
    """
    BREAK = "BREAK"
    CONTINUE = "CONTINUE"
    RETURN = "RETURN"

@dataclass
class Executor():
    """
    Implementação concreta do executor de nós da AST.
    Gerencia tabelas de variáveis, funções e conexões durante a execução.
    """
    var_table: VarTable = field(default_factory=VarTable)
    function_table: dict[str, ast.FuncDef] = field(default_factory=dict)
    connection_table: dict[str, socket.socket] = field(default_factory=dict)

    def __post_init__(self):
        """
        Inicializa funções padrão disponíveis durante a execução.
        """
        self.default_functions = {
            "print": print,
            "input": input,
            "to_number": self.number,
            "to_string": str,
            "to_bool": bool,
            "sleep": sleep,
            "send": self.send,
            "close": self.close,
            "len": len,
            "isalpha": self.isalpha,
            "isnum": self.isnum,
        }

    def run(self, node: ast.Module):
        """
        Executa o nó principal do programa, iterando sobre suas instruções.
        """
        if node.stmts:
            for stmt in node.stmts:
                self.execute(stmt)

    def execute(self, node: ast.Node):
        """
        Identifica e executa o método correspondente ao tipo do nó.
        """
        meth_name: str = f"exec_{type(node).__name__}"
        method = getattr(self, meth_name, None)

        if method:
            return method(node)

    def enter_scope(self):
        """
        Cria um novo escopo, vinculando uma nova tabela de variáveis ao escopo atual.
        """
        self.var_table = VarTable(prev=self.var_table)

    def exit_scope(self):
        """
        Retorna ao escopo anterior, descartando a tabela de variáveis atual.
        """
        if self.var_table.prev:
            self.var_table = self.var_table.prev

    ###### EXECUÇÃO DE INSTRUÇÕES #####
    
    def exec_Assign(self, node: ast.Assign):
        """
        Executa uma instrução de atribuição, armazenando o valor na tabela de variáveis.
        """
        value = self.execute(node.right)
        var_name = node.left.token.value
        is_declared = getattr(node.left, "decl", False)
        var_scope = self.var_table.find(var_name)

        if is_declared or not var_scope:
            self.var_table.table[var_name] = value
        else:
            var_scope.table[var_name] = value

        return var_name

    def exec_Return(self, node: ast.Return):
        """
        Executa uma instrução de retorno, avaliando e retornando a expressão associada.
        """
        return self.execute(node.expr)

    def exec_Break(self, _: ast.Break):
        """
        Executa uma instrução de interrupção de laço.
        """
        return commands.BREAK

    def exec_Continue(self, _: ast.Continue):
        """
        Executa uma instrução de continuação de laço.
        """
        return commands.CONTINUE

    def exec_FuncDef(self, node: ast.FuncDef):
        """
        Registra uma definição de função na tabela de funções.
        """
        if node.name not in self.function_table:
            self.function_table[node.name] = node

    def exec_block(self, block: ast.Body):
        """
        Executa um bloco de instruções, retornando o resultado da execução.
        """
        result = None
        for stmt in block:
            if isinstance(stmt, ast.Assign):
                self.exec_Assign(stmt)
            elif isinstance(stmt, ast.Return):
                return self.execute(stmt)
            else:
                result = self.execute(stmt)
            if result is not None or result in (commands.BREAK, commands.CONTINUE):
                return result

        return None

    def exec_If(self, node: ast.If):
        """
        Executa uma instrução condicional, avaliando a condição e executando o bloco correspondente.
        """
        condition = self.execute(node.condition)
        result = None
        self.enter_scope()
        if condition:
            result = self.exec_block(node.body)
        elif node.else_stmt:
            result = self.exec_block(node.else_stmt)
        self.exit_scope()
        return result

    def exec_While(self, node: ast.While):
        """
        Executa um laço de repetição enquanto a condição for verdadeira.
        """
        condition = self.execute(node.condition)
        self.enter_scope()
        while condition:
            result = self.exec_block(node.body)
            condition = self.execute(node.condition)
            if result == commands.BREAK:
                break
            elif result == commands.CONTINUE:
                continue
            else:
                if result:
                    return result
        self.exit_scope()

    def exec_Par(self, node: ast.Par):
        """
        Executa um bloco de instruções em paralelo, utilizando threads.
        """
        threads = []
        for stmt in node.body:
            thread_executor = Executor(
                deepcopy(self.var_table), deepcopy(self.function_table)
            )
            thread = threading.Thread(target=thread_executor.execute, args=(stmt,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def exec_Seq(self, _: ast.Seq):
        """
        Representa um bloco sequencial vazio. Não realiza nenhuma operação.
        """
        pass

    def exec_CChannel(self, node: ast.CChannel):
        """
        Estabelece uma conexão cliente com um canal de comunicação.
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((node.localhost, int(node.port)))
        print(client.recv(2040).decode())
        self.connection_table[node.name] = client

    def exec_SChannel(self, node: ast.SChannel):
        """
        Estabelece um canal de comunicação do tipo servidor.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((node.localhost, int(node.port)))
        server.listen(10)
        conn, _ = server.accept()
        description = self.execute(node.description)
        if description:
            conn.send(description.encode("utf-8"))

        function = self.function_table[node.func_name]
        while True:
            data = conn.recv(2048).decode()
            print(f"received: {data}")
            if not data:
                conn.close()
                break

            call = ast.Call(
                type=function.return_type,
                token=Token("ID", function.name),
                args=[ast.Constant(type="STRING", token=Token("STRING", data))],
                id=None,
                oper=None,
            )

            ret = self.exec_Call(call)

            conn.send(str(ret).encode("utf-8"))

    ###### FUNÇÕES PERSONALIZADAS ######
    def number(self, value):
        """
        Converte um valor para número inteiro ou ponto flutuante.
        """
        try:
            return int(value)
        except ValueError:
            return float(value)

    def isalpha(self, value):
        """
        Verifica se o valor contém apenas caracteres alfabéticos.
        """
        return str(value).isalpha()

    def isnum(self, value):
        """
        Verifica se o valor contém apenas caracteres numéricos.
        """
        return str(value).isnumeric()

    def send(self, conn_name: str, data: str):
        """
        Envia dados para um canal de comunicação cliente.
        """
        client = self.connection_table[conn_name]
        client.send(data.encode("utf-8"))

        return client.recv(2048).decode("utf-8")

    def close(self, conn_name: str):
        """
        Fecha a conexão com um canal de comunicação.
        """
        client = self.connection_table[conn_name]
        client.close()

    ###### EXECUÇÃO DE EXPRESSÕES #####

    def exec_Constant(self, node: ast.Constant):
        """
        Avalia uma constante, retornando seu valor.
        """
        match node.type:
            case "STRING":
                return node.token.value
            case "NUMBER":
                return eval(node.token.value)
            case "BOOL":
                return bool(node.token.value)
            case _:
                return node.token.value

    def exec_ID(self, node: ast.ID):
        """
        Avalia um identificador, retornando o valor associado na tabela de variáveis.
        """
        var_name = node.token.value
        var_scope = self.var_table.find(var_name)
        if var_scope:
            return var_scope.table[var_name]
        else:
            raise err.RunTimeError(f"variável {var_name} não definida")

    def exec_Access(self, node: ast.Access):
        """
        Avalia o acesso a um membro ou índice de uma variável.
        """
        index = self.execute(node.expr)
        var_name = node.id.token.value
        var_scope = self.var_table.find(var_name)
        if var_scope:
            return var_scope.table[var_name][index]
        else:
            raise err.RunTimeError(f"variável {var_name} não definida")

    def exec_Logical(self, node: ast.Logical):
        """
        Avalia uma operação lógica, retornando o resultado.
        """
        left = self.execute(node.left)
        match node.token.value:
            case "&&":
                if left:
                    return self.execute(node.right)
                return left
            case "||":
                right = self.execute(node.right)
                return left or right
            case _:
                return

    def exec_Relational(self, node: ast.Relational):
        """
        Avalia uma operação relacional, retornando o resultado.
        """
        left = self.execute(node.left)
        right = self.execute(node.right)

        if left is None or right is None:
            return

        match node.token.value:
            case "==":
                return left == right
            case "!=":
                return left != right
            case ">":
                return left > right
            case "<":
                return left < right
            case ">=":
                return left >= right
            case "<=":
                return left <= right
            case _:
                return

    def exec_Arithmetic(self, node: ast.Arithmetic):
        """
        Avalia uma operação aritmética, retornando o resultado.
        """
        left = self.execute(node.left)
        right = self.execute(node.right)

        if left is None or right is None:
            return

        match node.token.value:
            case "+":
                return left + right
            case "-":
                return left - right
            case "*":
                return left * right
            case "/":
                return left / right
            case "%":
                return left % right
            case _:
                return

    def exec_Unary(self, node: ast.Unary):
        """
        Avalia uma operação unária, retornando o resultado.
        """
        expr = self.execute(node.expr)

        if expr is None:
            return

        match node.token.value:
            case "!":
                return not expr
            case "-":
                return expr * (-1)
            case _:
                return

    def exec_Call(self, node: ast.Call):
        """
        Executa uma chamada de função, avaliando os argumentos e retornando o resultado.
        """
        func_name = node.oper if node.oper else node.token.value

        if func_name not in {"close", "send"}:
            if self.default_functions.get(func_name):
                args = [self.execute(arg) for arg in node.args]
                return self.default_functions[func_name](*args)
        else:
            conn_name = node.token.value
            if func_name == "send":
                args = [self.execute(arg) for arg in node.args]
                return self.default_functions[func_name](conn_name, *args)
            else:
                return self.default_functions[func_name](conn_name)

        function: ast.FuncDef | None = self.function_table.get(str(func_name))

        if not function:
            return

        self.enter_scope()

        for param in function.params.items():
            name, (_, default) = param
            if default:
                self.var_table.table[name] = self.execute(default)
        for param, arg in zip(function.params.items(), node.args):
            name, _ = param
            value = self.execute(arg)
            self.var_table.table[name] = value

        ret = self.exec_block(function.body)
        self.exit_scope()
        return ret
