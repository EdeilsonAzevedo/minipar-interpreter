from minipar.token import Token

def test_token_initialization():
    """Testa a inicialização de um token."""
    token = Token(tag="NUMBER", value="42")
    assert token.tag == "NUMBER"
    assert token.value == "42"

def test_token_representation():
    """Testa a representação de um token."""
    token = Token(tag="ID", value="x")
    assert repr(token) == "{x, ID}"