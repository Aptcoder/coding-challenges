from .token import TokenTypes
from .lexer import Lexer
import pytest


test_cases = [
    ("{}", [("{", TokenTypes.LEFT_BRACE), ("}", TokenTypes.RIGTH_BRACE), ("", TokenTypes.EOF)], 1),
    ("[]", [("[", TokenTypes.LEFT_BRACKET), ("]", TokenTypes.RIGHT_BRACKET), ("", TokenTypes.EOF)], 1),
    ("true false", [("true", TokenTypes.BOOLEAN_TRUE), ("false", TokenTypes.BOOLEAN_FALSE)], 1),
    ('''{"name": 
     "value"}''', [("{", TokenTypes.LEFT_BRACE), ("name", TokenTypes.STRING), (":", TokenTypes.COLON), ("value", TokenTypes.STRING), ("}", TokenTypes.RIGTH_BRACE), ("", TokenTypes.EOF)], 2),
     ('''{"name": "value"}''', [("{", TokenTypes.LEFT_BRACE), ("name", TokenTypes.STRING), (":", TokenTypes.COLON), ("value", TokenTypes.STRING), ("}", TokenTypes.RIGTH_BRACE), ("", TokenTypes.EOF)], 1),
     ('''{"name": "value", }''', [("{", TokenTypes.LEFT_BRACE), ("name", TokenTypes.STRING), (":", TokenTypes.COLON), ("value", TokenTypes.STRING), (",", TokenTypes.COMMA), ("}", TokenTypes.RIGTH_BRACE), ("", TokenTypes.EOF)], 1),
     ('''{"name": 101, }''', [("{", TokenTypes.LEFT_BRACE), ("name", TokenTypes.STRING), (":", TokenTypes.COLON), ("101", TokenTypes.NUMERIC), (",", TokenTypes.COMMA), ("}", TokenTypes.RIGTH_BRACE), ("", TokenTypes.EOF)], 1),
     ('''{"name": [101], }''', [("{", TokenTypes.LEFT_BRACE), ("name", TokenTypes.STRING), (":", TokenTypes.COLON), ("[", TokenTypes.LEFT_BRACKET),  ("101", TokenTypes.NUMERIC), ("]", TokenTypes.RIGHT_BRACKET), (",", TokenTypes.COMMA), ("}", TokenTypes.RIGTH_BRACE), ("", TokenTypes.EOF)], 1)
]
@pytest.mark.parametrize("input, tests, lines", test_cases)
def test_next_token(input, tests, lines):
    lexer = Lexer(input)

    for expectedLiteral, expectedType in tests:
        token = lexer.nextToken()
        assert token.literal == expectedLiteral
        assert token.type == expectedType

    assert lexer.line_number == lines

'''
Should fail for invalid values
'''
@pytest.mark.parametrize("input, expectation", [
    ("()", pytest.raises(Exception)),
    ("{)", pytest.raises(Exception)),
    ('''{ "name": $ }''', pytest.raises(Exception)),
])
def test_next_token_fails(input, expectation):
    with expectation:
        lexer = Lexer(input)
        while lexer.nextToken().type != TokenTypes.EOF:
            continue