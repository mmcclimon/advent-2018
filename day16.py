import operator
import re


def main():
    with open("d16.txt") as f:
        lines = [line.strip() for line in f]

    funcs = make_funcs()

    p1, possibles = part_one(funcs, lines[:3127])
    print("part 1:", p1)

    opcodes = resolve_ops(funcs, possibles)
    print("part 2:", run_program(opcodes, lines[3130:]))


def part_one(funcs, lines):
    opcodes = {op: set() for op in range(16)}
    multiples = 0

    for i in range(0, len(lines), 4):
        before = reg_from_line(lines[i])
        instr = [int(n) for n in lines[i + 1].split()]
        after = reg_from_line(lines[i + 2])
        matches = check(funcs, before, instr, after)

        if len(matches) >= 3:
            multiples += 1

        opcode = instr[0]
        for match in matches:
            opcodes[opcode].add(match)

    return multiples, opcodes


def reg_from_line(line):
    m = re.match(r"(?:Before|After):\s+\[(\d+), (\d+), (\d+), (\d+)\]", line)
    assert m is not None, line
    return [int(n) for n in m.groups()]


def check(funcs, before, instr, after):
    match = []

    for label, fn in funcs.items():
        reg = list(before)  # do not reuse the one we just did!
        fn(instr, reg)
        if tuple(reg) == tuple(after):
            match.append(label)

    return match


def resolve_ops(funcs, possibles):
    seen = set()
    lookup = {}

    while len(seen) < 16:
        k = next(k for k, possible in possibles.items() if len(possible) == 1)
        seen.add(k)

        to_remove = possibles[k].pop()
        lookup[k] = funcs[to_remove]
        for s in possibles.values():
            s.discard(to_remove)

    return lookup


def run_program(funcs, lines):
    reg = [0, 0, 0, 0]

    for line in lines:
        instr = [int(n) for n in line.split()]
        fn = funcs[instr[0]]
        fn(instr, reg)

    return reg[0]


# helpers


def make_funcs():
    reg = lambda registers, k: registers[k]  # noqa
    imm = lambda registers, k: k  # noqa

    return {
        "addr": make_op(operator.add, reg),
        "addi": make_op(operator.add, imm),
        "mulr": make_op(operator.mul, reg),
        "muli": make_op(operator.mul, imm),
        "banr": make_op(operator.and_, reg),
        "bani": make_op(operator.and_, imm),
        "borr": make_op(operator.or_, reg),
        "bori": make_op(operator.or_, imm),
        "setr": make_assn(reg),
        "seti": make_assn(imm),
        "gtir": make_cmp(operator.gt, imm, reg),
        "gtri": make_cmp(operator.gt, reg, imm),
        "gtrr": make_cmp(operator.gt, reg, reg),
        "eqir": make_cmp(operator.eq, imm, reg),
        "eqri": make_cmp(operator.eq, reg, imm),
        "eqrr": make_cmp(operator.eq, reg, reg),
    }


def make_op(op, lookup):
    def fn(instr, reg):
        _, a, b, c = instr
        reg[c] = op(reg[a], lookup(reg, b))

    return fn


def make_cmp(op, lookup_a, lookup_b):
    def fn(instr, reg):
        _, a, b, c = instr
        reg[c] = 1 if op(lookup_a(reg, a), lookup_b(reg, b)) else 0

    return fn


def make_assn(lookup):
    def fn(instr, reg):
        _, a, _, c = instr
        reg[c] = lookup(reg, a)

    return fn


if __name__ == "__main__":
    main()
