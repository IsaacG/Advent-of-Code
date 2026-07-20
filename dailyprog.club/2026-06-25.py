"""Valid Palindrome with One Skip

A tired air traffic controller is checking if a sequence of tower codes reads the same forward and backward.
They can afford to overlook one mistake.
Given a string code, return true if it can be a palindrome after deleting at most one character, otherwise false.
"""

def canBePalindrome(code):
    # Return True if code can be a palindrome after deleting at most one character
    i, j = 0, len(code) - 1
    while i < j and code[i] == code[j]:
        i += 1
        j -= 1
    return i >= j or code[i:j] == code[i:j][::-1] or code[i + 1:j + 1] == code[i + 1:j + 1][::-1]

assert canBePalindrome("aba") == True
assert canBePalindrome("abca") == True

# extra
assert canBePalindrome("acba") == True
