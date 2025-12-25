OCR_MAP = {
    # 2022/10: 6x5
    # From https://github.com/SizableShrimp/AdventOfCode2022/blob/main/src/util/java/me/sizableshrimp/adventofcode2022/helper/LetterParser.java
    # V, W, X not included
    0b01100_10010_10010_11110_10010_10010: "A",
    0b11100_10010_11100_10010_10010_11100: "B",
    0b01100_10010_10000_10000_10010_01100: "C",
    0b11100_10010_10010_10000_10010_11100: "D",
    0b11110_10000_11100_10000_10000_11110: "E",
    0b11110_10000_11100_10000_10000_10000: "F",
    0b01100_10010_10000_10110_10010_01110: "G",
    0b10010_10010_11110_10010_10010_10010: "H",
    0b11100_01000_01000_01000_01000_11100: "I",
    0b00110_00010_00010_00010_10010_01100: "J",
    0b10010_10100_11000_10100_10100_10010: "K",
    0b10000_10000_10000_10000_10000_11110: "L",
    0b10010_11110_11110_10010_10010_10010: "M",
    0b10010_11010_10110_10010_10010_10010: "N",
    0b01100_10010_10010_10010_10010_01100: "O",
    0b11100_10010_10010_11100_10000_10000: "P",
    0b01100_10010_10010_10010_10100_01010: "Q",
    0b11100_10010_10010_11100_10100_10010: "R",
    0b01110_10000_10000_01100_00010_11100: "S",
    0b01110_10000_01100_00010_00010_11100: "S",
    0b11100_01000_01000_01000_01000_01000: "T",
    0b11111_00100_00100_00100_00100_00100: "T",
    0b10010_10010_10010_10010_10010_01100: "U",
    0b10001_10001_01010_00100_00100_00100: "Y",
    0b11110_00010_00100_01000_10000_11110: "Z",
    # 2018: 6x8
    0b100010_100010_100010_111110_100010_100010_100010_100010: "H",
    0b111000_010000_010000_010000_010000_010000_010000_111000: "I",
    # 2018: 7x10 from https://github.com/mstksg/advent-of-code-ocr/blob/main/src/Advent/OCR/LetterMap.hs#L210
    0b0011000_0100100_1000010_1000010_1000010_1111110_1000010_1000010_1000010_1000010: "A",
    0b1111100_1000010_1000010_1000010_1111100_1000010_1000010_1000010_1000010_1111100: "B",
    0b0111100_1000010_1000000_1000000_1000000_1000000_1000000_1000000_1000010_0111100: "C",
    0b1111110_1000000_1000000_1000000_1111100_1000000_1000000_1000000_1000000_1111110: "E",
    0b1111110_1000000_1000000_1000000_1111100_1000000_1000000_1000000_1000000_1000000: "F",
    0b0111100_1000010_1000000_1000000_1000000_1001110_1000010_1000010_1000110_0111010: "G",
    0b1000010_1000010_1000010_1000010_1111110_1000010_1000010_1000010_1000010_1000010: "H",
    0b0001110_0000100_0000100_0000100_0000100_0000100_0000100_1000100_1000100_0111000: "J",
    0b1000010_1000100_1001000_1010000_1100000_1100000_1010000_1001000_1000100_1000010: "K",
    0b1000000_1000000_1000000_1000000_1000000_1000000_1000000_1000000_1000000_1111110: "L",
    0b1000010_1100010_1100010_1010010_1010010_1001010_1001010_1000110_1000110_1000010: "N",
    0b1111100_1000010_1000010_1000010_1111100_1000000_1000000_1000000_1000000_1000000: "P",
    0b1111100_1000010_1000010_1000010_1111100_1001000_1000100_1000100_1000010_1000010: "R",
    0b1000010_1000010_0100100_0100100_0011000_0011000_0100100_0100100_1000010_1000010: "X",
    0b1111110_0000010_0000010_0000100_0001000_0010000_0100000_1000000_1000000_1111110: "Z",
}



class OCR:
    """OCR helper for pixel displays."""

    DIMS = {6: 5, 8: 6, 10: 7}

    def __init__(self, output: list[list[bool]], validate: bool = True):
        self.output = output
        self.height = len(output)
        if not validate:
            return
        if self.height not in (6, 8, 10):
            raise ValueError(f"Must have 6, 8, 10 rows; found {len(output)}")
        # 6x5 or 10x7
        self.width = self.DIMS[self.height]
        if any(len(line) != len(output[0]) for line in output):
            raise ValueError("Lines are not uniform size.")
        # Zero-pad rows if needed with a space.
        if len(output[0]) % self.width == self.width - 1:
            self.output = [row + [] for row in self.output]

    def blocks(self):
        transposed = zip(*self.output)
        while True:
            bits = []
            col = next(transposed, None)
            while col and not any(col):
                col = next(transposed, None)
            if col is None:
                return
            bits.append(col)
            try:
                while any(col):
                    col = next(transposed)
                    bits.append(col)
            except StopIteration:
                pass
            while len(bits) < self.width:
                bits.append([False] * self.height)
            combined = []
            for row in zip(*bits):
                combined.extend(row)
            yield combined

    def as_string(self) -> str:
        """Return the OCR text."""
        chars = []
        for block in self.blocks():
            num = 0
            alternative = 0
            for byte in block:
                num = num << 1 | byte
                alternative = alternative << 1 | (not byte)
            if num not in OCR_MAP:
                if alternative in OCR_MAP:
                    num = alternative
                else:
                    print(f"Unknown char: {bin(num)}")
            chars.append(OCR_MAP.get(num, "?"))
        if "?" in chars:
            self.render()
        return "".join(chars)

    def is_valid(self) -> bool:
        for block in self.blocks():
            num = 0
            alternative = 0
            for byte in block:
                num = num << 1 | byte
                alternative = alternative << 1 | (not byte)
            if num not in OCR_MAP and alternative not in OCR_MAP:
                return False
        return True

    def render(self) -> None:
        """Print the pixels to STDOUT."""
        pixel = {True: COLOR_SOLID, False: COLOR_EMPTY}
        for row in self.output:
            print("".join(pixel[i] for i in row))

    @classmethod
    def from_point_set(cls, points: set[complex]):
        """OCR from a set of points."""
        rows = point_set_to_lists(points)
        width = cls.DIMS[len(rows)]
        while len(rows[0]) % width:
            rows = [row + [False] for row in rows]
        return cls(rows)
