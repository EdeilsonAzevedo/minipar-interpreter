from minipar.lexer import Lexer
from minipar.token import Token

def test_lexer_scan():
    """Testa a análise léxica básica."""
    code = 'number x = 42;'
    lexer = Lexer(data=code)
    tokens = list(lexer.scan())
    assert tokens[0][0] == Token(tag="TYPE", value="number")
    assert tokens[1][0] == Token(tag="ID", value="x")
    assert tokens[2][0] == Token(tag="=", value="=")
    assert tokens[3][0] == Token(tag="NUMBER", value="42")