import math
import random
import re
import sys

# Regular expression that defines what words are admissible; this one
# is horribly English-centric.
word_re = re.compile(r"[a-z]*$")

# Parse command-line arguments. Crash if the user git it wrong.
(bits, *wordlists) = sys.argv[1:]
bits = int(bits)

# Extract the set of admissable words from the text in the files.
words = set()
for wordlist in wordlists:
    with open(wordlist) as f:
        for line in f:
            for word in line.split():
                w = word.strip().lower()
                if word_re.match(w):
                    words.add(w)

# Compute the number of words (n) required to get a pass-phrase with
# the required number of bits, and pick that many words at random.
bpw = math.log(len(words), 2)
n = math.ceil(bits / bpw)
print("{} unique words in {} files ({:.1f} bits per word)"
      .format(len(words), len(wordlists), bpw))
print("Requested {} bits; these {} word(s) have {:.1f} bits:"
      .format(bits, n, n * bpw))
print(" ".join(random.SystemRandom().sample(words, n)))
