"""Generate simple passphrases from word lists."""

import argparse
import math
import random
import re
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

# Regular expression that defines what words are admissible; this one
# is horribly English-centric.
word_re: re.Pattern[str] = re.compile(r"[a-z]*$")


def load_words(wordlists: Iterable[str]) -> set[str]:
    """Return a set of admissible words found in *wordlists*."""
    words: set[str] = set()
    for wordlist in wordlists:
        with Path(wordlist).open() as f:
            for line in f:
                for word in line.split():
                    w = word.strip().lower()
                    if word_re.match(w):
                        words.add(w)
    return words


class PassphraseInfo(NamedTuple):
    """Details about a generated passphrase."""

    count: int  # number of words we selected from
    bpw: float  # bits per word
    words: list[str]  # the passphrase


def generate(bits: int, wordlists: Iterable[str], rnd: random.Random) -> PassphraseInfo:
    """Generate a passphrase from *wordlists* with at least *bits* bits."""
    words = load_words(wordlists)
    bpw = math.log(len(words), 2)
    n = math.ceil(bits / bpw)
    chosen = rnd.sample(sorted(words), n)
    return PassphraseInfo(len(words), bpw, chosen)


def parse_args(argv: list[str]) -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "bits",
        type=int,
        help="the passphrase will have at least this many bits of entropy",
    )
    parser.add_argument(
        "wordlists",
        nargs="+",
        metavar="WORDLIST",
        help="path(s) to text files containing candidate words",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> None:
    """Run the program with command line *argv*."""
    args = parse_args(argv)
    bits = args.bits
    wordlists = args.wordlists
    info = generate(bits, wordlists, random.SystemRandom())
    print(f"{info.count} unique words in {len(wordlists)} files ({info.bpw:.1f} bits per word)")
    n = len(info.words)
    print(f"Requested {bits} bits; these {n} word(s) have {n * info.bpw:.1f} bits:")
    print(" ".join(info.words))


if __name__ == "__main__":
    main(sys.argv[1:])
