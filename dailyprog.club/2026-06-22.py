"""Count vowel-dominant words

A word is vowel-dominant when it has more vowels than consonants.
Vowels are a, e, i, o, u, case-insensitive.
Non-letter characters don't count at all.
Given an array of words, return how many of them are vowel-dominant.
"""

import string

def countVowelDominant(words):
    return sum(
        sum(i.isalpha() for i in word.lower()) < 2 * sum(i in "aeiou" for i in word.lower())
        for word in words
    )

assert countVowelDominant(["hello", "world", "aei", "bcdf"]) == 1
assert countVowelDominant(["AA", "bb"]) == 1
assert countVowelDominant(["xyz"]) == 0

