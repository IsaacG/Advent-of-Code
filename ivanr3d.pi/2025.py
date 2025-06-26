import string


def solve(pi, data):
    # 32 digits of pi.
    digits = str(pi).replace(".", "")[:32]

    # Find entries with a price which is in pi.
    corrupt = []
    for line in data.splitlines()[1:]:
        day, price, ticker = line.split()
        if price.replace(".", "") in digits:
            corrupt.append((int(day), float(price), ticker))

    # Part one. Collect correupt prices.
    val = corrupt[0][1]
    for day, price, ticker in corrupt:
        if day % 2 == 0:
            val *= price
        else:
            val /= price

    val = int(str(val).replace(".", ""))
    print(str(val)[:10])

    # Part two.

    # Map ticker to day and price for lookups.
    tick_prices = {}
    for line in data.splitlines()[1:]:
        day, price, ticker = line.split()
        tick_prices[ticker] = (int(day), int(str(price).replace(".", "")))
    # Load the cipher_map into a list.
    cipher_map = [i for line in CIPHER_MAP_TXT.splitlines() for i in line.split()]

    phrase = []
    for day, price, ticker in corrupt:
        shift = int(str(price).replace(".", ""))
        other_ticker = "".join(
            string.ascii_uppercase[(string.ascii_uppercase.index(i) + shift) % 26]
            for i in ticker
        )
        other_day, other_price = tick_prices[other_ticker]
        letter = cipher_map[other_price % 256]
        phrase.append((other_day, letter))
    print("".join(i for _, i in sorted(phrase)))


DATA = """\
Day          Price ($)          Ticker
1            150.00             TLM
2            93.23              PIH
3            300.50             MTH
4            420.75             IUV
5            3.14               GST
6            720.20             FKE
7            12.57              KVW
8            88.90              TEC
9            210.00             OIL
10           2.64               PHI
11           45.60              CUV
12           33.83              SPI
13           999.99             MEME
14           28.27              MED
15           123.45             BIA
16           65.80              REN
17           6.53               HST
18           250.00             AND
19           18.85              YVO
20           33.33              XOR
21           8.46               NUM
22           777.77             POT
23           9.42               BNO
24           199.99             NOT
25           15.92              SPI
26           850.00             VSL
27           19.94              IVA
28           58.97              GST
29           27.95              PHI
30           21.99              EXW
"""

CIPHER_MAP_TXT = """\
X J P Z Q T M C A O W Y B G D A
N F R S H V K U E X J P Z Q T M
C L O W Y B G D A N F R S H V K
G E X J P Z Q T M P L O W Y B G
D A N F R S H V K U E X J P Z Q
T M A L O W Y B G D A O F I S H
A K U E X J P Z Q T M C L O W Y
O G D A N F R S H V K U E X J P
Y Q T M C L O W Y B G D A N F R
S H V K U E X Y G Z Q T M C L O
D Y B G D A N F R S H V K U D X
J P Z Q T M C L O W Y B G D A N
F R S H V K U E X J P Z Q T M C
D O W Y B G D A N F R S H V K U
E X J P Z Q T M C O O W Y B G D
A N F R S H V K U E X J P Z Q T"""


if __name__ == "__main__":
    solve("314159265358979323846264338327950288419716939937510", DATA)


