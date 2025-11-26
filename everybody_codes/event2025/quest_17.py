"""Everyone Codes Day N."""

import collections
import logging
import queue
import functools
from lib import helpers
from lib import parsers

log = logging.info

def solve(part: int, data: str) -> int:
    """Solve the parts."""
    Xv, Yv = data.coords["@"].copy().pop()

    @functools.cache
    def burns(rad):
        target = rad * rad
        return {
            (Xc, Yc)
            for (Xc, Yc), num in data.chars.items()
            if num.isalnum() and (Xv - Xc) * (Xv - Xc) + (Yv - Yc) * (Yv - Yc) <= target
        }

    @functools.cache
    def damage(target):
        return sum(
            int(num)
            for (Xc, Yc), num in data.chars.items()
            if num.isalnum() and (Xv - Xc) * (Xv - Xc) + (Yv - Yc) * (Yv - Yc) <= target
        )

    if part == 1:
        return damage(10*10)

    if part == 2:
        delta, i = max(
            (damage((i+1)**2) - damage(i*i), i)
            for i in range(data.max_x)
        )
        return delta * (i + 1)

    start_x, start_y = data.coords["S"].copy().pop()
    vals = {k: int(v) for k, v in data.chars.items() if v.isdigit()}
    vals[start_x, start_y] = 0

    for rad in range(1, 45):
        counter = 0
        max_steps = 30 * (rad + 1)
        viable = set(vals) - set(burns(rad))
        assert (start_x, start_y) in vals
        assert (start_x, start_y) in viable

        best = {(start_x, start_y): 0}
        target_groups = [
            {
                (x, y)
                for x, y in viable
                if l(x, y)
            }
            for l in [
                (lambda x, y: y == Yv and x < Xv),  # left
                (lambda x, y: x == Xv and y > Yv),  # bottom
                (lambda x, y: y == Yv and x > Xv),  # right
                (lambda x, y: x == start_x and y == start_y),  # start
            ]
        ]
        # print(target_groups)

        for idx, targets in enumerate(target_groups):
            pending = set(targets) & viable
            # print(f"{rad}.{idx} {pending}, {best}")

            seen = set()
            todo = queue.PriorityQueue()
            for (x, y), steps in best.items():
                todo.put((steps, x, y))
            best = {}

            while pending:
                assert not todo.empty()
                steps, x, y = todo.get()

                if (x, y) in pending:
                    pending.remove((x, y))
                    best[x, y] = steps
                    if idx == 3 and x == start_x and y == start_y:
                        if steps < max_steps:
                            return rad * steps
                        break

                for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if (nx, ny) not in viable or (nx, ny) in seen:
                        continue
                    seen.add((nx, ny))
                    nsteps = steps + vals[nx, ny]
                    todo.put((nsteps, nx, ny))

            # print(rad, idx, best)





PARSER = parsers.CoordinatesParser()
TEST_DATA = [
    """\
189482189843433862719
279415473483436249988
432746714658787816631
428219317375373724944
938163982835287292238
627369424372196193484
539825864246487765271
517475755641128575965
685934212385479112825
815992793826881115341
1737798467@7983146242
867597735651751839244
868364647534879928345
519348954366296559425
134425275832833829382
764324337429656245499
654662236199275446914
317179356373398118618
542673939694417586329
987342622289291613318
971977649141188759131""",
    """\
4547488458944
9786999467759
6969499575989
7775645848998
6659696497857
5569777444746
968586@767979
6476956899989
5659745697598
6874989897744
6479994574886
6694118785585
9568991647449""",
    """\
2645233S5466644
634566343252465
353336645243246
233343552544555
225243326235365
536334634462246
666344656233244
6426432@2366453
364346442652235
253652463426433
426666225623563
555462553462364
346225464436334
643362324542432
463332353552464""",
    """\
545233443422255434324
5222533434S2322342222
523444354223232542432
553522225435232255242
232343243532432452524
245245322252324442542
252533232225244224355
523533554454232553332
522332223232242523223
524523432425432244432
3532242243@4323422334
542524223994422443222
252343244322522222332
253355425454255523242
344324325233443552555
423523225325255345522
244333345244325322335
242244352245522323422
443332352222535334325
323532222353523253542
553545434425235223552""",
    """\
5441525241225111112253553251553
133522122534119S911411222155114
3445445533355599933443455544333
3345333555434334535435433335533
5353333345335554434535533555354
3533533435355443543433453355553
3553353435335554334453355435433
5435355533533355533535335345335
4353545353545354555534334453353
4454543553533544443353355553453
5334554534533355333355543533454
4433333345445354553533554555533
5554454343455334355445533453453
4435554534445553335434455334353
3533435453433535345355533545555
534433533533535@353533355553345
4453545555435334544453344455554
4353333535535354535353353535355
4345444453554554535355345343354
3534544535533355333333445433555
3535333335335334333534553543535
5433355333553344355555344553435
5355535355535334555435534555344
3355433335553553535334544544333
3554333535553335343555345553535
3554433545353554334554345343343
5533353435533535333355343333555
5355555353355553535354333535355
4344534353535455333455353335333
5444333535533453535335454535553
3534343355355355553543545553345"""
]
TESTS = [
    (1, TEST_DATA[0], 1573),
    (2, TEST_DATA[1], 1090),
    (3, TEST_DATA[2], 592),
    (3, TEST_DATA[3], 330),
    # (3, TEST_DATA[4], 3180),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
