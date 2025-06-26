# Solution by analysis

## Step one

```
INIT
                            # a =  1
         0| set b 57        # b = 57
         1| set c b         # 
         2| jnz a 2         # 
         3| jnz 1 5         # 
         4| mul b 100       # 
         5| sub b -100000   # 
         6| set c b         # 
         7| sub c -17000    # 
L1
         8| set f 1         # 
         9| set d 2         # 
L2
        10| set e 2         # 
L3
        11| set g d         # 
        12| mul g e         # 
        13| sub g b         # 
        14| jnz g 2         # if (g == 0) f = 0; break
        15| set f 0         # 
        16| sub e -1        # 
        17| set g e         # 
        18| sub g b         # 
        19| jnz g -8        #  GOTO L2
        20| sub d -1        # 
        21| set g d         # 
        22| sub g b         # 
        23| jnz g -13       #  GOTO L2
        24| jnz f 2         #  if (f == 0) h++
        25| sub h -1        # 
        26| set g b         # 
        27| sub g c         # 
        28| jnz g 2         #  if (g == 0) return h
        29| jnz 1 3         #  RETURN
        30| sub b -17       #  b += 17
        31| jnz 1 -23       #  GOTO L2
```

## Step two

```
INIT
            a = 1
            b = 105700
            c = 122700
            result = 0
L1
            f = 1
            d = 2
L2
            e = 2
L3
        11| set g d         #  x = d * e - b
        15| set f 0         #  if (x == 0) f = 0; break
        16| sub e -1        #  e += 1
        18| sub g b         #  g = e - b
        19| jnz g -8        #  GOTO L3
        20| sub d -1        #  d += 1
        22| sub g b         #  g = d - b 
        23| jnz g -13       #  GOTO L2
        25| sub h -1        #  if (f == 0) h++
        27| sub g c         #  g = b - c
        28| jnz g 2         #  if (g == 0) return h
        29| jnz 1 3         #  RETURN
        30| sub b -17       #  b += 17
        31| jnz 1 -23       #  GOTO L1
```

## Step three

```
INIT
            a = 1
            b = 105700
            c = 122700
            result = 0
L1
            f = 1
            d = 2
L2
            e = 2
L3
        15| set f 0         #  if (d * e == b) f = 0; break
        16| sub e -1        #  e += 1
        18| sub g b         #  g = e - b
        19| jnz g -8        #  if (e != b) GOTO L3

        20| sub d -1        #  d += 1
        23| jnz g -13       #  if (d != b) GOTO L2
        25| sub h -1        #  if (f == 0) h++
        28| jnz g 2         #  if (b == c) return h
        30| sub b -17       #  b += 17
        31| jnz 1 -23       #  GOTO L1
```

## Step four

```
INIT
            a = 1
            b = 105700
            c = 122700
            result = 0
while True:
    f = 1
    d = 2
    for d in range(2, b):
        for e in range(2, b)
            if (d * e == b) f = 0; break 2

    25| sub h -1        #  if (f == 0) h++
    28| jnz g 2         #  if (b == c) return h
    30| sub b -17       #  b += 17
```

## Step five

```
INIT
            a = 1
            b = 105700
            c = 122700
            result = 0
while True:
    f = 1
    for d in range(2, b):
        for e in range(2, b)
            if (d * e == b) f = 0; break 2

    if (f == 0) h++
    if (b == c) return h
    b += 17
```

## Step six

```
result = 0
for b in range(105700, 122700 + 1, 17):
    f = 1
    if any(
        d * e == b
        for d in range(2, b)
        for e in range(d, b)
    ):
        result += 1
```

## Step seven

```
result = 0
for b in range(105700, 122700 + 1, 17):
    if any(
        d * e == b
        for d in range(2, b)
        for e in range(d, b)
    ):
        result += 1


import math
result = 0
for b in range(105700, 122700 + 1, 17):
    if any(
        b % i == 0 for i in range(2, math.ceil(math.sqrt(b)))
    ):
        result += 1


import math
sum(
    1
    for b in range(105700, 122700 + 1, 17)
    if any(b % i == 0 for i in range(2, math.ceil(math.sqrt(b))))
)
```
