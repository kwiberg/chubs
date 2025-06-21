import math
import random
import re
import sys
from typing import NamedTuple

# Regular expression that defines what words are admissible; this one
# is horribly English-centric.
word_re = re.compile(r"[a-z]*$")


class PassphraseInfo(NamedTuple):
    count: int
    bpw: float
    n: int
    words: list[str]


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


def generate(bits, wordlists, rnd):
    """Generate a passphrase from *wordlists* with at least *bits* bits."""
    words = load_words(wordlists)
    bpw = math.log(len(words), 2)
    n = math.ceil(bits / bpw)
    # Python 3.11 requires sampling from a sequence, so sort the set first
    chosen = rnd.sample(sorted(words), n)
    return PassphraseInfo(len(words), bpw, n, chosen)


def main(argv):
    bits = int(argv[0])
    wordlists = argv[1:]
    info = generate(bits, wordlists, random.SystemRandom())
    print(
        "{} unique words in {} files ({:.1f} bits per word)".format(
            info.count, len(wordlists), info.bpw
        )
    )
    print(
        "Requested {} bits; these {} word(s) have {:.1f} bits:".format(
            bits, info.n, info.n * info.bpw
        )
    )
    print(" ".join(info.words))


if __name__ == "__main__":
    main(sys.argv[1:])
