from minipar.symtable import SymTable, Symbol

def test_symtable_insert_and_find():
    """Testa a inserção e busca na tabela de símbolos."""
    symtable = SymTable()
    symbol = Symbol(var="x", type="NUMBER")
    assert symtable.insert("x", symbol) is True
    assert symtable.find("x") == symbol
    assert symtable.find("y") is None