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
    count: int  # number of words we selected from
    bpw: float  # bits per word
    words: list[str]  # the passphrase


def generate(bits, wordlists, rnd):
    """Generate a passphrase from *wordlists* with at least *bits* bits."""
    words = load_words(wordlists)
    bpw = math.log(len(words), 2)
    n = math.ceil(bits / bpw)
    chosen = rnd.sample(sorted(words), n)
    return PassphraseInfo(len(words), bpw, chosen)


def main(argv):
    bits = int(argv[0])
    wordlists = argv[1:]
    info = generate(bits, wordlists, random.SystemRandom())
    print(f"{info.count} unique words in {len(wordlists)} files ({info.bpw:.1f} bits per word)")
    n = len(info.words)
    print(f"Requested {bits} bits; these {n} word(s) have {n * info.bpw:.1f} bits:")
    print(" ".join(info.words))


if __name__ == "__main__":
    main(sys.argv[1:])
