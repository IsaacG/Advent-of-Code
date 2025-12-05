#!/bin/awk -f

BEGIN { position = 50; p1 = 0; p2 = 0; }

/L/ { step = -1 }
/R/ { step =  1 }
{
    distance = substr($0, 2) + 0;
    for (i = 0; i < distance ; i++) {
        position += step;
        if (position % 100 == 0) {
            p2++
        }
    }
    if (position % 100 == 0) {
        p1++
    }
}
END {
    print("2025/01", p1, p2)
}
