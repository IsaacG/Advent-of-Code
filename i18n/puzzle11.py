"""i18n puzzle day N."""

import string
import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    variants = {"Οδυσσεα", "Οδυσσει", "Οδυσσευ", "Οδυσσευς", "Οδυσσεως"}
    # Fold the florish sigma into a regular sigma. Use lowercase only.
    variants = {v.lower().replace("ς", "σ") for v in variants}
    # Length filtering to ignore some words.
    longest = max(len(i) for i in variants)
    shortest = min(len(i) for i in variants)
    lower = "αβγδεζηθικλμνξοπρστυφχψω"
    lowers = lower * 2

    count = 0
    for line in data.splitlines():
        found = False
        # Extract words, ignoring non-letters.
        words = "".join(i for i in line.lower() if i in lower + " ").split()
        for word in words:
            # Filter words by length.
            if not shortest <= len(word) <= longest:
                continue
            # Try shifting.
            for shift in range(len(lower)):
                shifted = "".join(lowers[lower.index(char) + shift] for char in word)
                if shifted in variants:
                    count += shift
                    found = True
                    break
            if found:
                break
    return count



TEST_DATA = """\
σζμ γ' ωοωλδθαξλδμξρ οπξρδυζ οξκτλζσθρ Ξγτρρδτρ.
αφτ κ' λαλψφτ ωπφχλρφτ δξησηρζαλψφτ φελο, Φκβωωλβ.
γ βρφαγζ ωνψν ωγφ πγχρρφ δρδαθωραγζ ρφανφ.
"""
TESTS = [
    (1, TEST_DATA, 19),
]
