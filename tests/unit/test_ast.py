import pytest
from minipar.ast import (
    Constant,
    ID,
    Access,
    Logical,
    Relational,
    Arithmetic,
    Unary,
    Call,
    Cast,
    Assert,
    NoOp,
    Token,
)

def test_constant_to_dict():
    """Testa a conversão de uma constante para dicionário."""
    token = Token(tag="NUMBER", value="42")
    constant = Constant(type="NUMBER", token=token)
    result = constant.to_dict()
    assert result == {"type": "NUMBER", "token": token}


def test_id_name_property():
    """Testa a propriedade 'name' de um identificador."""
    token = Token(tag="ID", value="x")
    identifier = ID(type="ID", token=token)
    assert identifier.name == "x"


def test_access_initialization():
    """Testa a inicialização de um nó de acesso."""
    id_token = Token(tag="ID", value="obj")
    expr_token = Token(tag="NUMBER", value="0")
    id_node = ID(type="ID", token=id_token)
    expr_node = Constant(type="NUMBER", token=expr_token)
    access = Access(
        id=id_node,
        expr=expr_node,
        type="ACCESS",
        token=Token(tag="ACCESS", value="access")
    )
    assert access.id == id_node
    assert access.expr == expr_node


def test_logical_operation():
    """Testa a criação de um nó de operação lógica."""
    left = Constant(type="BOOL", token=Token(tag="TRUE", value="true"))
    right = Constant(type="BOOL", token=Token(tag="FALSE", value="false"))
    logical = Logical(left=left, right=right, type="BOOL", token=Token(tag="AND", value="&&"))
    assert logical.left == left
    assert logical.right == right


def test_cast_initialization():
    """Testa a inicialização de um nó de conversão de tipo."""
    expr = Constant(type="NUMBER", token=Token(tag="NUMBER", value="42"))
    cast = Cast(expr=expr, target_type="STRING", type="STRING", token=Token(tag="CAST", value="cast"))
    assert cast.expr == expr
    assert cast.target_type == "STRING"


def test_assert_statement():
    """Testa a criação de uma instrução de asserção."""
    condition = Constant(type="BOOL", token=Token(tag="TRUE", value="true"))
    message = Constant(type="STRING", token=Token(tag="STRING", value="Erro!"))
    assertion = Assert(condition=condition, message=message)
    assert assertion.condition == condition
    assert assertion.message == message


def test_noop_statement():
    """Testa a criação de uma instrução vazia."""
    noop = NoOp()
    assert isinstance(noop, NoOp)