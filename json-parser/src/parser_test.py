from .parser import Parser
import pytest
from contextlib import nullcontext as does_not_raise
from pathlib import Path


test_cases = [
    ("{}", does_not_raise()),
    ('{"key": "value"}', does_not_raise()),
    ('{"key"}', pytest.raises(Exception)),
    ("[]", pytest.raises(Exception, match='character at position 0 not recognised')),
    ("{]", pytest.raises(Exception, match='character at position 1 not recognised')),
    ("{{}", pytest.raises(Exception, match='Invalid token')),
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
    ("/step2/valid2.json", does_not_raise())
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