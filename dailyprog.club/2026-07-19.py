import functools

def minLandings(asteroids):
    if len(asteroids) <= 1:
        return 0
    return solve(tuple(asteroids))
    
@functools.cache
def solve(asteroids):
    boost, *rest = asteroids
    if boost >= len(rest):
        return 1
    return 1 + min(
        solve(tuple(rest[i:]))
        for i in range(boost)
    )

assert minLandings([0]) == 0
assert minLandings([2, 1, 1, 1]) == 2
assert minLandings([1, 2, 1, 1]) == 2
