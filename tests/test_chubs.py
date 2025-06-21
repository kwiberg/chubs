import math
import sys
from pathlib import Path

# Add project root to sys.path so the tests can import the chubs module
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import chubs


def test_load_words(tmp_path):
    words_file = tmp_path / "words.txt"
    words_file.write_text("Hello world\nBanana BANANA apple123 pineapple")
    result = chubs.load_words([words_file])
    assert result == {"hello", "world", "banana", "pineapple"}


class DummyRandom:
    def sample(self, seq, n):
        """Return the first *n* items to keep sampling deterministic."""
        return list(seq)[:n]


def test_generate_calculates_n_and_sample(tmp_path):
    words_file = tmp_path / "words.txt"
    words = [
        "alpha", "beta", "gamma", "delta",
        "epsilon", "zeta", "eta", "theta",
    ]
    words_file.write_text(" ".join(words))
    info = chubs.generate(10, [words_file], DummyRandom())
    assert info.count == 8
    assert math.isclose(info.bpw, 3.0)
    assert info.words == sorted(set(words))[:4]


def test_main_prints_expected(monkeypatch, capsys):
    def fake_generate(bits, wordlists, rnd):
        return chubs.PassphraseInfo(10, 3.0, ["a", "b", "c", "d"])

    monkeypatch.setattr(chubs, "generate", fake_generate)
    chubs.main(["10", "dummy.txt"])
    captured = capsys.readouterr()
    expected = (
        "10 unique words in 1 files (3.0 bits per word)\n"
        "Requested 10 bits; these 4 word(s) have 12.0 bits:\n"
        "a b c d\n"
    )
    assert captured.out == expected
