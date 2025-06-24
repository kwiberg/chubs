"""Generate simple passphrases from word lists."""

import argparse
import math
import random
import re
import sys
import tempfile
import urllib.request
from collections.abc import Iterable
from pathlib import Path
from typing import NamedTuple

# Regular expression that defines what words are admissible; this one
# is horribly English-centric.
word_re: re.Pattern[str] = re.compile(r"[a-z]*$")


def download_default_wordlist() -> str:
    """Download Pride and Prejudice from Project Gutenberg to temp directory.

    Returns path to the downloaded file. Avoids re-downloading if already exists.
    """
    temp_dir = Path(tempfile.gettempdir())
    wordlist_path = temp_dir / "pride_and_prejudice.txt"

    if not wordlist_path.exists():
        url = "https://www.gutenberg.org/files/1342/1342-0.txt"
        urllib.request.urlretrieve(url, wordlist_path)  # noqa: S310

    return str(wordlist_path)


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
        "-b",
        "--entropy-bits",
        type=int,
        default=64,
        help="the passphrase will have at least this many bits of entropy (default: 64)",
    )
    parser.add_argument(
        "-w",
        "--wordlist",
        action="append",
        required=False,
        metavar="WORDLIST",
        dest="wordlists",
        help="path to a text file containing candidate words (can be used multiple times; "
        "defaults to Jane Austen's Pride and Prejudice from Project Gutenberg)",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> None:
    """Run the program with command line *argv*."""
    args = parse_args(argv)
    bits = args.entropy_bits
    wordlists = args.wordlists or [download_default_wordlist()]
    info = generate(bits, wordlists, random.SystemRandom())
    print(f"{info.count} unique words in {len(wordlists)} files ({info.bpw:.1f} bits per word)")
    n = len(info.words)
    print(f"Requested {bits} bits; these {n} word(s) have {n * info.bpw:.1f} bits:")
    print(" ".join(info.words))


if __name__ == "__main__":
    main(sys.argv[1:])
