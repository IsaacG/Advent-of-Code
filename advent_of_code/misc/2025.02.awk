#!/bin/awk -f

BEGIN { p1 = 0; p2 = 0; RS = ","; FS = "-"; }

# Return if the number is made of a pattern repeated times times.
function repeats(num, times,   i) {
    len = length(num)
    # Only consider multiples of the length.
    if (len % times) return 0;
    segment_length = len / times;
    first = substr(num, 1, segment_length);
    for (i = 1; i < times; i++)
        if (substr(num, 1 + i * segment_length, segment_length) != first)
            return 0;
    return 1
}

{
    for (i = $1; i <= $2; i++) {
        if (repeats(i, 2)) p1 += i

        for (j = 2; j <= length(i); j++) {
            if (repeats(i, j)) {
                p2 += i
                break
            }
        }
    }
}
END {
    print("2025/02", p1, p2)
}
