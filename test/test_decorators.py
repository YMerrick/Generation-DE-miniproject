from io import StringIO

from src.decorators import get_num_input
from src import get_input


def test_get_num_input(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('1\n'))
    assert get_num_input('Input: ') == 1


def test_get_input(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO('Hello\n'))
    assert get_input('Input: ') == 'Hello'
