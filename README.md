chubs---a simple Python script that generates XKCD-style passwords
==================================================================

First, read the [original XKCD comic][1].

This Python script will generate passwords (or rather, pass *phrases*)
such as the one in the comic. They need to be generated with a
computer; humans are hopelessly bad at coming up with a random
sequence of words.

Invoke it from the command line, like so:

    $ python3 chubs.py 64 some-long-text-file.txt
    5640 unique words in 1 files (12.5 bits per word)
    Requested 64 bits; these 6 word(s) have 74.8 bits:
    tall healthy disagreeable noble connect perplexity

The words will be randomly selected from the set of words in the text
file listed on the command line. Pick any text file you like (or
files---you can list as many as you like). This example uses [Jane
Austen's][2] [Pride and Prejudice][3] from [Project Gutenberg][4].

The numeric parameter you specify is the number of random bits used to
create the password. This is a measure of the password strength
relative to an attacker that knows how the password was generated,
including what word list was used. Any real-world attacker will have
to brute-force at least this many bits.



[1]: http://xkcd.com/936/
[2]: http://en.wikipedia.org/wiki/Jane_Austen
[3]: http://www.gutenberg.org/ebooks/1342
[4]: http://www.gutenberg.org/
