import itertools
import string

encoded = "Wii kxtszof ova fsegyrpm d lnsrjkujvq roj! Kdaxii svw vnwhj pvugho buynkx tn vwh-gsvw ruzqia. Mrq'x kxtmjw bx fhlhlujw cjoq! Hmg tyhfa gx dwd fdqu bsm osynbn oulfrex, kahs con vjpmd qtjv bx whwxssp cti hmulkudui yqg f Miywh Sj Efh!"
pi = "3141592653589793"

out = ""
for letter, shift in zip(encoded.lower(), itertools.cycle(pi)):
    if letter.isalpha():
        out += string.ascii_lowercase[(string.ascii_lowercase.index(letter.lower()) + 26 - int(shift)) % 26]
    else:
        out += letter
print(out)

numbers = "zero one two three four five size seven eight nine ten".split()
result = 1
out = "".join(i for i in out if i.isalpha())
for i in range(len(out)):
    for idx, num in enumerate(numbers):
        if out[i:].startswith(num):
            result *= idx
print(result)
