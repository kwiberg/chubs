"""Unit tests for the :mod:`chubs` module."""

import math
import sys
from pathlib import Path

import pytest

# Add project root to sys.path so the tests can import the chubs module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chubs


def test_load_words(tmp_path: Path) -> None:
    """Return lowercased words that match the regex."""
    words_file = tmp_path / "words.txt"
    words_file.write_text("Hello world\nBanana BANANA apple123 pineapple")
    result = chubs.load_words([words_file])
    assert result == {"hello", "world", "banana", "pineapple"}


class DummyRandom:
    """Deterministic :class:`random.Random` replacement for tests."""

    def sample(self, seq: list[str], n: int) -> list[str]:
        """Return the first *n* items to keep sampling deterministic."""
        return list(seq)[:n]


def test_generate_calculates_n_and_sample(tmp_path: Path) -> None:
    """`generate` samples enough words for the requested bits."""
    words_file = tmp_path / "words.txt"
    words = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
    words_file.write_text(" ".join(words))
    info = chubs.generate(10, [words_file], DummyRandom())
    assert info.count == 8
    assert math.isclose(info.bpw, 3.0)
    assert info.words == sorted(set(words))[:4]


def test_main_prints_expected(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`main` writes passphrase information to stdout."""

    def fake_generate(_bits: int, _wordlists: list[str], _rnd: DummyRandom) -> chubs.PassphraseInfo:
        return chubs.PassphraseInfo(10, 3.0, ["a", "b", "c", "d"])

    monkeypatch.setattr(chubs, "generate", fake_generate)
    chubs.main(["-b", "10", "-w", "dummy.txt"])
    captured = capsys.readouterr()
    expected = (
        "10 unique words in 1 files (3.0 bits per word)\n"
        "Requested 10 bits; these 4 word(s) have 12.0 bits:\n"
        "a b c d\n"
    )
    assert captured.out == expected


def test_parse_args_returns_namespace() -> None:
    """`parse_args` returns populated :class:`argparse.Namespace`."""
    args = chubs.parse_args(["-b", "20", "-w", "one.txt", "-w", "two.txt"])
    assert args.entropy_bits == 20
    assert args.wordlists == ["one.txt", "two.txt"]


def test_parse_args_defaults_entropy_bits() -> None:
    """`parse_args` defaults entropy_bits to 64 when not specified."""
    args = chubs.parse_args(["-w", "one.txt"])
    assert args.entropy_bits == 64
    assert args.wordlists == ["one.txt"]


def test_main_with_default_entropy(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """`main` uses default 64 bits when not specified."""

    def fake_generate(_bits: int, _wordlists: list[str], _rnd: DummyRandom) -> chubs.PassphraseInfo:
        words = ["w1", "w2", "w3", "w4", "w5", "w6", "w7", "w8", "w9", "w10"]
        return chubs.PassphraseInfo(100, 6.64, words)

    monkeypatch.setattr(chubs, "generate", fake_generate)
    chubs.main(["-w", "dummy.txt"])
    captured = capsys.readouterr()
    expected = (
        "100 unique words in 1 files (6.6 bits per word)\n"
        "Requested 64 bits; these 10 word(s) have 66.4 bits:\n"
        "w1 w2 w3 w4 w5 w6 w7 w8 w9 w10\n"
    )
    assert captured.out == expected
