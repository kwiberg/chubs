import argparse
import math
import random
import re
import sys
from typing import NamedTuple

# Regular expression that defines what words are admissible; this one
# is horribly English-centric.
word_re = re.compile(r"[a-z]*$")

def load_words(wordlists):
    """Return a set of admissible words found in *wordlists*."""
    words = set()
    for wordlist in wordlists:
        with open(wordlist) as f:
            for line in f:
                for word in line.split():
                    w = word.strip().lower()
                    if word_re.match(w):
                        words.add(w)
    return words


class PassphraseInfo(NamedTuple):
    count: int        # number of words we selected from
    bpw: float        # bits per word
    words: list[str]  # the passphrase


def generate(bits, wordlists, rnd):
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
        "bits", type=int, help="number of random bits for the passphrase"
    )
    parser.add_argument(
        "wordlists",
        nargs="+",
        metavar="WORDLIST",
        help="path(s) to text files containing candidate words",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> None:
    args = parse_args(argv)
    bits = args.bits
    wordlists = args.wordlists
    info = generate(bits, wordlists, random.SystemRandom())
    print(
        "{} unique words in {} files ({:.1f} bits per word)".format(
            info.count, len(wordlists), info.bpw
        )
    )
    n = len(info.words)
    print(
        "Requested {} bits; these {} word(s) have {:.1f} bits:".format(
            bits, n, n * info.bpw
        )
    )
    print(" ".join(info.words))


if __name__ == "__main__":
    main(sys.argv[1:])