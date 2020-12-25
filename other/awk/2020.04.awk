#!/bin/awk -f

BEGIN {
    cnt=0
    cnt2=0
    RS="\n\n"
}
{
    for (i=1; i<=NF; i++) {
        split($i, a, ":");
        d[a[0]]=NR
        e[a[0]] = a[1]
    }
    if (   d["byr"] == NR \
        && d["iyr"] == NR \
        && d["eyr"] == NR \
        && d["hgt"] == NR \
        && d["hcl"] == NR \
        && d["ecl"] == NR \
        && d["pid"] == NR \
    ) {
        cnt++
    } else {
        next
    }
    if (   e["byr"] < 1920 || e["byr"] > 2002 \
        || e["iyr"] < 2010 || e["iyr"] > 2020 \
        || e["eyr"] >= 2020 || e["eyr"] > 2030 \
    ) next
    if (e["hgt"] ~ /[0-9]*in/ && (e["hgt"] < 59 || e["hgt"] > 76) {
        next
    } else if (e["hgt"] ~ /[0-9]*cm/ && (e["hgt"] < 150 || e["hgt"] > 193) {
        next
    }
    if (! e["hcl"] ~ /#[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f]/) next
    if (! e["ecl"] ~ /amb|blu|brn|gry|grn|hzl|oth/) next
    if (! e["pid"] ~ /^[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]$/) next
    cnt2++
}
END {
    print cnt
    print cnt2
}

