#!/bin/awk -f

BEGIN { sizes[1] = 2; sizes[2] = 12; }

# Find the first instance of the largest number, ignoring the remaining last chars.
# Update `val` with the number and strip everything until that number from `line`.
function find_largest(remaining) {
    remaining--
    # Find the max.
    most = 0
    most_idx = 0
    for (i = 1; i <= length(line) - remaining; i++) {
        digit = substr(line, i, 1)
        if (digit > most) {
            most = digit
            most_idx = i
        }
    }
    # Update the line and val.
    line = substr(line, most_idx + 1)
    val = val most
    # Call recursively until we used up all slots.
    if (remaining) {
        find_largest(remaining)
    }
}

{
    for (part in sizes) {
        line = $0
        val = ""
        find_largest(sizes[part])
        out[part] += val
    }
}

END {
    print("2025/03", out[1], out[2])
}

# vim:expandtab:sw=4:ts=4
