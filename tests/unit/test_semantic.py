from minipar.semantic import SemanticAnalyzer
from minipar.ast import Constant

def test_semantic_constant():
    """Testa a análise semântica de uma constante."""
    analyzer = SemanticAnalyzer()
    node = Constant(type="NUMBER", token=None)
    result = analyzer.visit_Constant(node)
    assert result == "NUMBER"