"""The Tablet of Echoes

Ancient scribes wrote a sacred incantation by stringing word fragments end-to-end.
The incantation is effective only if the full text reads the same forward and backward.
Given a list of fragments words, determine whether you can arrange all fragments in some order to form a single palindrome.
You must use every fragment exactly once.
Return true if possible, false otherwise.
"""


""" cat  catal"""
def canForm(suffix, words):
    length = len(suffix)
    if not words and suffix == suffix[::-1]:
        return True
    candidates = {i for i in words if suffix.startswith(i[:length])}
    for candidate in candidates:
        remaining_words = words.copy()
        remaining_words.remove(candidate)
        if len(candidate) <= length:
            leftover = suffix.removeprefix(candidate)
        else:
            leftover = candidate.removeprefix(suffix)[::-1]
        if canForm(leftover, remaining_words):
            return True
    return False

def canFormPalindrome(words):
    """Return True if the words can be arranged into a palindrome."""
    return canForm("", words)


assert canFormPalindrome(["ab", "ba", "a"]) == True
assert canFormPalindrome(["aa", "bb", "cc"]) == False
assert canFormPalindrome(["racecar"]) == True

