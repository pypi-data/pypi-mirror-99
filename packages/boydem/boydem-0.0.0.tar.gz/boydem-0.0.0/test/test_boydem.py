import os
from pathlib import Path
import sys
import importlib

import pytest

from boydem import boydem, _db_manager


@pytest.fixture(autouse=True)
def run_around_tests():
    _db_manager.file_name = (
        Path(os.path.expanduser("~")) / ".boydem" / "boydem.test.pickle"
    )
    boydem.clear()
    yield
    boydem.clear()


class K:
    def __init__(self):
        self.x = 3

    def f(self):
        self.x += 1
        return self.x

    def __repr__(self):
        return f"K equals {self.x}"


def test_boydem():
    boydem.a = 3
    boydem["b"] = [1, 2, 3]
    boydem[7] = "💥"
    boydem.k = K()
    boydem.k.f()


def test_string_key():
    boydem["a"] = "b"
    assert hasattr(boydem, "a")
    assert "a" in boydem
    assert "no" not in boydem
    assert boydem["a"] == "b"
    assert boydem.a == "b"
    assert boydem.__getattr__("a") == "b"
    del boydem["a"]
    with pytest.raises(KeyError):
        hasattr(boydem, "a")


def test_int_key():
    boydem[123] = 456
    assert 123 in boydem
    assert boydem[123] == 456
    assert boydem.__getattr__(123) == 456
    del boydem[123]
    assert 123 not in boydem


def test_keys():
    boydem["a"] = 1
    boydem["b"] = 2
    boydem["c"] = 3
    assert len(boydem.keys()) == 3
    for key in boydem.keys():
        assert key in ("a", "b", "c")


def test_values():
    boydem["a"] = 1
    boydem["b"] = 2
    boydem["c"] = 3
    assert len(boydem.values()) == 3
    for value in boydem.values():
        assert value in (1, 2, 3)


def test_items():
    boydem["a"] = 1
    boydem["b"] = 2
    boydem["c"] = 3
    assert len(boydem.items()) == 3
    for key, value in boydem.items():
        assert key in ("a", "b", "c")
        assert value in (1, 2, 3)


def test_iter():
    boydem["a"] = 1
    boydem["b"] = 2
    boydem["c"] = 3
    assert len(boydem) == 3
    for key, value in boydem:
        assert key in ("a", "b", "c")
        assert value in (1, 2, 3)


def test_len():
    boydem.clear()
    boydem["a"] = "a"
    assert len(boydem) == 1
    boydem["a"] = "a"
    assert len(boydem) == 1
    boydem["b"] = "b"
    assert len(boydem) == 2
    del boydem.a
    assert len(boydem) == 1


def test_print(capsys):
    print(boydem)
    captured = capsys.readouterr()
    assert captured.out == "Nothing here 😳\n"
    boydem.dog = "Jaime"
    boydem["list"] = [1, 2, 3]
    boydem[3] = "three"
    boydem.k = K()
    boydem.k.f()
    print(boydem)
    captured = capsys.readouterr()
    assert captured.out == "dog: Jaime\nlist: [1, 2, 3]\n3: three\nk: K equals 4\n"
    assert captured.out != "dog: Jaime\nlist: [1, 2, 3]\n3: three\nk: K equals 3\n"
