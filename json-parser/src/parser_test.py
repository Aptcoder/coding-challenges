from .parser import Parser
import pytest
from contextlib import nullcontext as does_not_raise
from pathlib import Path


test_cases = [
    ("{}", does_not_raise()),
    ('{"key": "value"}', does_not_raise()),
    ('{"key": 101 }', does_not_raise()),
    ('{"key": true }', does_not_raise()),
    ('''{"key": true,
        "name": "value"
      }''', does_not_raise()),
    ('{"key": false }', does_not_raise()),
    ('{"key": null }', does_not_raise()),
    ('{"key"}', pytest.raises(Exception)),
    ("()", pytest.raises(Exception, match='character at position 0 not recognised')),
    ("{)", pytest.raises(Exception, match='character at position 1 not recognised')),
    ("{{}", pytest.raises(Exception, match='Invalid token')),
    ('''{"name": [101,] }''', pytest.raises(Exception, match='Unrecognised array element')),
    ('''{"name": [101, 20, 40, 30] }''', does_not_raise()),
    ('''{"name": [] }''', does_not_raise()),
    ('''{"name": {} }''', does_not_raise()),
    ('''{"name": ['10 list'] }''', pytest.raises(Exception)),
    ('''{"name": {
        "key": "random"
    } }''', does_not_raise()),
    ]

@pytest.mark.parametrize("input, expectation", test_cases)
def test_parse_program(input, expectation):
    parser = Parser(input)

    with expectation:
        parser.parseProgram()



'''
Some file based tests
'''
test_cases = [
    ("/step1/invalid.json", pytest.raises(Exception, match="Invalid token")),
    ("/step2/invalid.json", pytest.raises(Exception, match="Invalid token")),
    ("/step2/invalid2.json", pytest.raises(Exception, match="not recognised")),
    ("/step1/valid.json", does_not_raise()),
    ("/step2/valid.json", does_not_raise()),
    ("/step2/valid2.json", does_not_raise()),
    ("/step3/valid.json", does_not_raise()),
    ("/step3/invalid.json", pytest.raises(Exception, match="not recognised")),
    ("/step4/invalid.json", pytest.raises(Exception, match="not recognised")),
    ("/step4/valid.json", does_not_raise()),
    ("/step4/valid2.json", does_not_raise()),
]
@pytest.mark.parametrize("relative_path, expectation", test_cases)
def test_parse_program_with_files(relative_path, expectation):
    file_path = Path(__file__).parent.absolute().joinpath(f'tests_files/{relative_path}')
    file = None
    with open(file_path) as fd:
        file = fd.read()

    parser = Parser(file)
    with expectation:
        parser.parseProgram()