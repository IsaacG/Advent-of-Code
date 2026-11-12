"""Everyone Codes Event 2026 Day N."""

import itertools
import math
import logging
import platform

try:
    from lib import helpers
    from lib import parsers
except ModuleNotFoundError as e:
    if platform.python_implementation() != "PyPy":
        raise

def overlaps(a1, a2, b1, b2, N):
    d1 = a1 - b1
    d2 = a2 - b2
    low = min(d1, d2)
    high = max(d1, d2)

    # Check if any multiple of N (k * N) lies in the range [low, high]
    # Copied from Discord. I do not understand.
    k_min = math.ceil(low / N)
    k_max = math.floor(high / N)

    return k_min <= k_max


def solve(part: int, data: str, testing) -> int:
    """Solve the parts.

    Each pair of hands can be solved independently.
    For every pair, use frame or reference of hand one, stationary at 0.
    Only one hand moves. If it crosses 0, it pulses.
    """
    pulses = 0
    clock_n = len(data)
    for clock_idx, dataset in enumerate(data, 1):
        # print(f"{clock_idx} / {clock_n}")
        vals = {}
        for a, b in dataset:
            vals[a] = [1 if i == "CW" else -1 if i == "CCW" else int(i) for i in b.split(":")]
        n = len(vals["hands"])

        for hand_one, hand_two in itertools.combinations(range(n), r=2):
            logging.debug("Solve for clock %03d, hands %d, %d", clock_idx, hand_one + 1, hand_two + 1)
            if vals["move"][hand_one] < vals["move"][hand_two]:
                hand_one, hand_two = hand_two, hand_one
            seen = {}
            pair_pulses = 0
            second = 0

            hands_one, hands_two = vals["hands"][hand_one], vals["hands"][hand_two]
            lcm = math.lcm(hands_one, hands_two)
            mult_one, mult_two = lcm // hands_one, lcm // hands_two

            pos_init_1, pos_init_2 = vals["current"][hand_one] * mult_one, vals["current"][hand_two] * mult_two
            pos_init_2 = (pos_init_2 - pos_init_1) % lcm
            pos_init_1 = 0


            pos_end_1, pos_end_2 = pos_init_1, pos_init_2
            e1, e2 = vals["move"][hand_one], vals["move"][hand_two]
            end, one_end = e1, e2
            assert end >= one_end
            step_1, step_2 = vals["direction"][hand_one] * mult_one, vals["direction"][hand_two] * mult_two
            combined_step = step_2 - step_1

            logging.debug("Hands %d and %d, raw size %d, %d", hand_one + 1, hand_two + 1, hands_one, hands_two)
            logging.debug("LCM=%d, mults %d, %d", lcm, mult_one, mult_two)
            logging.debug("Stops at %d, %d ==> %d", e1, e2, end)

            if combined_step == 0:
                second = one_end

            while second < end:
                if second == one_end:
                    combined_step = -step_1
                    seen = {}
                    if combined_step == 0:
                        break

                if False:
                    mult = 1
                else:
                    if combined_step > 0:
                        mult = (lcm - pos_init_2 - 1) // combined_step
                    else:
                        mult = (pos_init_2 - 1) // -combined_step
                    mult = min(end - second - 1, mult)
                    if second < one_end:
                        mult = min(one_end - second - 1, mult)
                    mult = max(1, mult)
                pos_end_2 = pos_init_2 + combined_step * mult
                second += mult
                pos_end_2 %= lcm

                if pos_init_2 != 0 and (pos_end_2 == 0 or combined_step > 0 and pos_end_2 < pos_init_2 or combined_step < 0 and pos_end_2 > pos_init_2):
                    pair_pulses += 1
                    logging.debug("T %d, hands %d & %d cross. (%d->%d and %d->%d)", second + 1, hand_one + 1, hand_two + 1, 0, 0, pos_init_2, pos_end_2)

                pos_init_2 = pos_end_2

                fp = (pos_init_2, combined_step)

                if fp in seen and second != one_end and second != end:
                    prior_second, prior_pulse = seen[fp]
                    stride = second - prior_second
                    assert stride > 0
                    if second < one_end:
                        local_end = one_end
                    else:
                        local_end = end
                    assert local_end > second
                    jumps = (local_end - second) // stride
                    assert jumps >= 0
                    logging.info("CYCLE @ second=%d pulse=%d, hands @ %d, %d: %s", second, pair_pulses, 0, pos_init_2, seen[fp])
                    logging.debug("Stride = %d, pulses = %d", stride, pair_pulses - prior_pulse)
                    logging.debug("Cycles remaining: %d = %d jumps", local_end - second, jumps)
                    second += jumps * stride
                    pair_pulses += jumps * (pair_pulses - prior_pulse)
                seen[fp] = (second, pair_pulses)

            logging.info("Solve for clock %03d, hands %d, %d => pulses = %s", clock_idx, hand_one + 1, hand_two + 1, pair_pulses)
            pulses += pair_pulses

    return pulses


PARSER = parsers.ParseBlocks([parsers.parse_multi_str_per_line])
TEST_DATA = [
    """\
hands 6:8:12
direction CW:CCW:CW
current 2:4:8
move 9:7:4""",
    """\
hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:15""",
    """\
hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:20
""",
    """\
hands 6:8:12
direction CW:CCW:CW
current 2:4:8
move 9:7:4

hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:15

hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 10:12:20""",
    """\
hands 10:10:10
direction CW:CW:CW
current 9:0:5
move 5400:0:0

hands 6:6:6
direction CW:CW:CW
current 1:1:1
move 6240:6240:6240

hands 9:11:20
direction CW:CCW:CW
current 0:1:17
move 7224:7352:7518

hands 5:8:27
direction CW:CW:CCW
current 0:5:8
move 9308:9113:8846

hands 8:4:28
direction CCW:CCW:CCW
current 6:0:20
move 11160:10415:10560

hands 8:5:27
direction CW:CW:CW
current 1:4:21
move 13215:12919:13217

hands 5:5:30
direction CCW:CW:CW
current 1:2:17
move 15924:15023:15840

hands 9:13:18
direction CCW:CCW:CW
current 7:12:0
move 18134:19319:19334

hands 7:9:24
direction CCW:CCW:CCW
current 2:1:7
move 22758:22565:22704

hands 6:5:29
direction CCW:CW:CCW
current 2:2:26
move 26460:26470:26296

hands 6:8:12
direction CW:CCW:CW
current 1:2:2
move 30958:32196:33434

hands 6:8:26
direction CCW:CW:CW
current 3:7:21
move 37900:40021:37761

hands 7:11:22
direction CW:CCW:CW
current 2:10:7
move 46384:46410:47902

hands 6:6:28
direction CCW:CW:CCW
current 1:2:22
move 54874:54399:54185

hands 4:11:25
direction CW:CW:CCW
current 2:1:16
move 65151:64221:67223

hands 5:6:29
direction CW:CW:CCW
current 3:0:27
move 79691:81207:81132

hands 7:13:20
direction CCW:CW:CCW
current 1:9:14
move 95447:99401:98234

hands 4:14:22
direction CW:CCW:CW
current 1:1:10
move 113209:113168:116641

hands 9:13:18
direction CCW:CCW:CW
current 8:5:11
move 133822:139621:141597

hands 4:4:32
direction CW:CCW:CCW
current 3:2:25
move 162645:166182:165763

hands 5:7:4
direction CW:CW:CW
current 4:6:3
move 191687:199354:207021

hands 4:10:26
direction CW:CCW:CCW
current 1:6:21
move 239508:248312:245348

hands 6:12:22
direction CW:CCW:CW
current 2:8:15
move 276804:295649:295844

hands 5:9:26
direction CW:CCW:CW
current 0:1:12
move 332616:342102:333918

hands 5:8:27
direction CW:CW:CW
current 3:6:23
move 415382:411779:414013

hands 7:8:25
direction CCW:CW:CW
current 3:3:19
move 495429:477912:502221

hands 7:11:22
direction CCW:CCW:CW
current 0:8:7
move 589770:585221:615741

hands 9:11:20
direction CCW:CW:CW
current 5:1:8
move 717368:708548:700363

hands 8:5:27
direction CW:CCW:CCW
current 6:3:16
move 883466:847488:886932

hands 5:4:31
direction CCW:CCW:CW
current 3:3:25
move 1056367:1044688:996370

hands 4:5:7
direction CCW:CCW:CCW
current 0:0:0
move 1186881:1234356:1281831

hands 8:12:20
direction CCW:CCW:CW
current 6:1:6
move 1484001:1435165:1478486

hands 9:4:27
direction CW:CW:CW
current 3:1:19
move 1715069:1829534:1818655

hands 9:11:20
direction CCW:CW:CW
current 7:8:9
move 2070902:2145956:2057168

hands 4:9:27
direction CCW:CCW:CW
current 3:5:7
move 2513967:2505323:2606813

hands 6:5:29
direction CCW:CCW:CCW
current 1:3:19
move 3049759:3071229:3046232

hands 4:4:32
direction CCW:CCW:CW
current 0:0:11
move 3654199:3572951:3725348

hands 9:10:21
direction CCW:CCW:CW
current 0:1:20
move 4430463:4435296:4445030

hands 4:10:26
direction CW:CCW:CW
current 1:0:7
move 5301615:5456976:5503438

hands 9:6:25
direction CW:CW:CCW
current 3:5:14
move 6146100:6425743:6406909

hands 5:7:9
direction CW:CCW:CW
current 0:0:0
move 7348857:7642811:7936765

hands 5:7:28
direction CW:CW:CW
current 4:1:26
move 9100463:9249888:9100571

hands 4:5:31
direction CW:CCW:CCW
current 0:1:10
move 10788421:11162892:10892093

hands 4:12:24
direction CCW:CCW:CCW
current 3:8:15
move 13328710:12923494:12932097

hands 4:11:25
direction CCW:CCW:CCW
current 2:9:7
move 15544904:16040567:15345891

hands 6:8:26
direction CW:CCW:CW
current 1:2:10
move 19607762:19614530:19335321

hands 8:12:20
direction CCW:CW:CCW
current 0:7:6
move 23028126:23696530:23636502

hands 4:7:29
direction CCW:CCW:CW
current 1:0:20
move 26807301:28063897:27898371

hands 5:11:24
direction CCW:CCW:CW
current 0:9:1
move 32405696:33522822:32146575

hands 9:6:25
direction CCW:CW:CW
current 6:4:7
move 40170062:40423242:40463770

hands 8:8:8
direction CW:CCW:CW
current 0:2:4
move 45502190:47322277:49142365

hands 6:10:24
direction CW:CW:CW
current 3:7:5
move 54756414:55585240:58733352

hands 5:13:22
direction CW:CCW:CW
current 0:10:2
move 69240290:67846689:67893341

hands 7:13:20
direction CCW:CCW:CW
current 5:6:16
move 80735504:80917311:84240549

hands 4:7:29
direction CW:CW:CW
current 3:0:21
move 101632269:99453357:100075800

hands 7:7:26
direction CCW:CCW:CCW
current 4:0:14
move 117621469:113388228:114138533

hands 4:4:32
direction CCW:CW:CCW
current 2:1:14
move 140217371:144808340:136984490

hands 5:9:26
direction CCW:CW:CCW
current 0:4:12
move 175664414:166031770:168435192

hands 9:11:20
direction CCW:CW:CW
current 3:4:11
move 201248140:208086411:205147134

hands 5:12:23
direction CW:CW:CW
current 3:9:4
move 241272341:247317339:249069750

hands 9:9:22
direction CW:CW:CCW
current 5:5:17
move 281737571:304276576:293007073

hands 7:5:28
direction CCW:CCW:CCW
current 5:1:15
move 345208521:355019777:345908210

hands 4:7:29
direction CW:CCW:CCW
current 1:4:7
move 425205151:429848516:422045914

hands 7:6:27
direction CW:CCW:CW
current 3:2:19
move 514490335:492273703:487668666

hands 5:12:23
direction CCW:CW:CCW
current 3:2:17
move 627341585:623630381:586651607

hands 9:9:22
direction CCW:CW:CW
current 6:2:21
move 724250555:709781252:744872785

hands 4:8:28
direction CCW:CCW:CCW
current 0:3:0
move 892277557:908280400:892115931

hands 6:14:20
direction CCW:CW:CCW
current 1:3:15
move 1032590987:1019575835:1025367117

hands 4:8:28
direction CW:CCW:CW
current 0:2:17
move 1295164346:1263345673:1266482949

hands 5:11:24
direction CCW:CW:CW
current 1:7:11
move 1504264288:1522501500:1469709231

hands 4:13:23
direction CW:CW:CW
current 0:11:0
move 1827638984:1841149402:1861815844

hands 7:8:25
direction CCW:CW:CCW
current 0:4:16
move 2117629998:2201363533:2116287664

hands 4:6:30
direction CCW:CW:CCW
current 0:3:3
move 2642066922:2596640396:2557580437

hands 4:10:26
direction CCW:CW:CCW
current 2:6:11
move 3235790557:3126386742:3179063974

hands 4:12:24
direction CCW:CCW:CW
current 3:0:11
move 3806937986:3765284682:3765950101

hands 4:14:22
direction CCW:CCW:CW
current 1:8:2
move 4515628522:4441384248:4580969493

hands 9:13:18
direction CCW:CW:CW
current 1:8:13
move 5308636058:5270235130:5399017155

hands 9:14:17
direction CW:CW:CW
current 0:7:7
move 6459418375:6450360670:6298500460

hands 9:4:27
direction CCW:CCW:CCW
current 5:1:12
move 7789337335:7967942960:7508742156

hands 8:12:20
direction CW:CW:CW
current 3:7:14
move 9079916574:9540090748:9445571020

hands 10:10:10
direction CW:CCW:CW
current 9:1:5
move 10801142310:11233188002:11665233694

hands 4:13:23
direction CW:CW:CW
current 1:6:14
move 13069835667:13342804480:13164710030

hands 6:7:27
direction CCW:CW:CW
current 0:1:9
move 16502966430:16428707135:16424774330

hands 6:5:29
direction CCW:CW:CW
current 1:3:5
move 19955784282:20154607830:19516840720

hands 8:12:20
direction CCW:CW:CW
current 6:9:1
move 22419823081:22702994938:23898837556

hands 9:4:27
direction CW:CCW:CW
current 8:1:6
move 28687874613:27898228176:28642148380

hands 4:14:22
direction CCW:CCW:CCW
current 1:11:3
move 33762282123:33221533469:33987317697

hands 4:5:31
direction CW:CCW:CW
current 0:2:28
move 40870722640:39981211754:40002006938

hands 8:4:28
direction CW:CCW:CW
current 1:3:13
move 49216162082:48134172331:47977967871

hands 7:9:24
direction CCW:CW:CW
current 3:0:4
move 59467619746:56391861670:55804098361

hands 5:12:23
direction CCW:CCW:CCW
current 3:10:21
move 69064112897:69827255049:68252221392

hands 7:10:23
direction CW:CCW:CW
current 3:1:12
move 80531722209:80546647374:81143517857

hands 8:11:21
direction CW:CW:CCW
current 2:8:8
move 101754973148:97458924292:98874068661

hands 8:4:28
direction CCW:CCW:CW
current 1:2:5
move 118228151875:117790193073:123058560999

hands 6:11:23
direction CW:CW:CCW
current 4:1:17
move 140022798175:148661306329:147645607830

hands 9:9:22
direction CW:CCW:CCW
current 4:7:3
move 168844982206:178458839941:168356754237

hands 7:11:22
direction CW:CW:CW
current 2:0:1
move 211545494212:208580513073:211999616458

hands 6:14:20
direction CW:CW:CW
current 4:3:4
move 254374424007:244565274211:254769377653

hands 7:7:26
direction CW:CW:CCW
current 0:1:6
move 289073190139:300457172176:300334525277

hands 4:8:12
direction CW:CCW:CW
current 1:2:3
move 345074893841:358877889594:372680885348""",
]
TESTS = [
    (1, TEST_DATA[0], 5),
    (1, TEST_DATA[1], 7),
    (1, TEST_DATA[2], 9),
    (2, TEST_DATA[3], 21),
    (3, TEST_DATA[4], 984329851511),
]

if __name__ == "__main__":
    helpers.run_solution(globals())
