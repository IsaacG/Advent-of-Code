"""i18n puzzle day 1."""

import logging

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    total = 0
    for line in data.splitlines():
        if len(line.encode()) <= 160 and len(line) <= 140:
            total += 13
        elif len(line.encode()) <= 160:
            total += 11
        elif len(line) <= 140:
            total += 7
    return total


TEST_DATA = [
    """\
néztek bele az „ártatlan lapocskába“, mint ahogy belenézetlen mondták ki rá a halálos itéletet a sajtó csupa 20–30 éves birái s egyben hóhérai.
livres, et la Columbiad Rodman ne dépense que cent soixante livres de poudre pour envoyer à six milles son boulet d'une demi-tonne.  Ces
Люди должны были тамъ и сямъ жить въ палаткахъ, да и мы не были помѣщены въ посольскомъ дворѣ, который также сгорѣлъ, а въ двухъ деревянныхъ
Han hade icke träffat Märta sedan Arvidsons middag, och det hade gått nära en vecka sedan dess. Han hade dagligen promenerat på de gator, där"""
]
TESTS = [
    (1, TEST_DATA[0], 31),
    # (2, TEST_DATA[1], None),
    # (3, TEST_DATA[2], None),
]
