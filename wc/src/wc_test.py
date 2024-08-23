from . import wc as wc
from pathlib import Path

test_file_path = Path(__file__).parent.absolute().joinpath('test.txt')

def test_get_number_of_bytes():
    with open(test_file_path) as fd:
        result = wc.get_number_of_bytes(fd)
        assert result == 342190

def test_get_number_of_lines_and_words():
    with open(test_file_path) as fd:
        nl, nw = wc.get_number_of_lines_and_words(fd)
        assert nl == 7145
        assert nw == 58164

def test_get_number_of_characters():
    '''
    Open with newline="" so that new line characters are recognized but not translated
    '''
    with open(test_file_path, 'r', newline="") as fd:
        count = wc.get_number_of_characters(fd)
        assert count == 339292