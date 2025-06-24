`chubs`—a simple Python script that generates XKCD-style passwords
==================================================================

First, read the [original XKCD comic][1].

This Python script will generate passwords (or rather, pass *phrases*)
such as the one in the comic. They need to be generated with a
computer; humans are hopelessly bad at coming up with a random
sequence of words.

Invoke it from the command line using the built in help for details:

    $ python3 chubs.py -h

Basic usage with default wordlist (Pride and Prejudice, 64 bits of
entropy):

    $ python3 chubs.py
    5715 unique words in 1 files (12.5 bits per word)
    Requested 64 bits; these 6 word(s) have 74.9 bits:
    french schemes stand viewing henceforth aspect

Using a custom wordlist:

    $ curl -o wuthering-heights.txt https://www.gutenberg.org/files/768/768-0.txt
    $ python3 chubs.py -w wuthering-heights.txt
    7840 unique words in 1 files (12.9 bits per word)
    Requested 64 bits; these 5 word(s) have 64.7 bits:
    image luxury overflowing wad interview

Asking for a specific amount of entropy (using default wordlist):

    $ python3 chubs.py -b 128

Multiple word list files:

    $ python3 chubs.py -w file1.txt -w file2.txt

By default, the script uses [Jane Austen's][2] [Pride and
Prejudice][3] from [Project Gutenberg][4] as the wordlist, which is
automatically downloaded and cached in your system's temporary
directory.

You can also specify your own text files using the -w flag. The words
will be randomly selected from the set of words in the text files
listed on the command line. Pick any text file you like (or
files---you can list as many as you like with multiple -w flags).

The numeric parameter you specify is the number of random bits used to
create the password. This is a measure of the password strength
relative to an attacker that knows how the password was generated,
including what word list was used. Any real-world attacker will have
to brute-force at least this many bits.



[1]: http://xkcd.com/936/
[2]: http://en.wikipedia.org/wiki/Jane_Austen
[3]: http://www.gutenberg.org/ebooks/1342
[4]: http://www.gutenberg.org/
