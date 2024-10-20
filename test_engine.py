import pytest
from backend.engine import create_rule, evaluate_rule, modify_operator, Node


def test_create_rule():
    rule_string = "age > 18"
    ast = create_rule(rule_string)
    
    assert ast.type == "operator"
    assert ast.value == ">"
    assert ast.left.type == "operand"
    assert ast.right.type == "operand"


def test_evaluate_rule():
    rule_string = "age > 18"
    ast = create_rule(rule_string)
    
    data = {"age": 20}
    result = evaluate_rule(ast, data)
    assert result is True

    data = {"age": 16}
    result = evaluate_rule(ast, data)
    assert result is False


def test_invalid_rule():
    with pytest.raises(ValueError):
        create_rule("invalid_rule_format")


def test_modify_operator():
    rule_string = "age > 18"
    ast = create_rule(rule_string)
    modify_operator(ast, "<")
    
    assert ast.value == "<"
