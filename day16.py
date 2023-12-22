import operator
import re


def main():
    with open("d16.txt") as f:
        lines = [line.strip() for line in f]

    funcs = {
        "addr": make_reg(operator.add),
        "addi": make_imm(operator.add),
        "mulr": make_reg(operator.mul),
        "muli": make_imm(operator.mul),
        "banr": make_reg(operator.and_),
        "bani": make_imm(operator.and_),
        "borr": make_reg(operator.or_),
        "bori": make_imm(operator.or_),
        "setr": setr,
        "seti": seti,
        "gtir": make_comp_ir(operator.gt),
        "gtri": make_comp_ri(operator.gt),
        "gtrr": make_comp_rr(operator.gt),
        "eqir": make_comp_ir(operator.eq),
        "eqri": make_comp_ri(operator.eq),
        "eqrr": make_comp_rr(operator.eq),
    }

    multiples = 0

    opcodes = {op: set() for op in range(16)}

    i = 0
    while i < 3130:
        if lines[i].startswith("Before:"):
            before = reg_from_line(lines[i])
            instr = tuple(int(n) for n in lines[i + 1].split())
            after = reg_from_line(lines[i + 2])
            matches = check(funcs, before, instr, after)

            if len(matches) >= 3:
                multiples += 1

            opcode = instr[0]
            for match in matches:
                opcodes[opcode].add(match)

            i += 2

        i += 1

    print("part 1:", multiples)

    seen = set()
    lookup = {}

    while len(seen) < 16:
        k = next(k for k, possible in opcodes.items() if len(possible) == 1)
        seen.add(k)

        to_remove = opcodes[k].pop()
        lookup[k] = funcs[to_remove]
        for op, s in opcodes.items():
            s.discard(to_remove)

    print("part 2:", run_program(lookup, lines[3130:]))


def reg_from_line(line):
    m = re.match(r"(?:Before|After):\s+\[(\d+), (\d+), (\d+), (\d+)\]", line)
    assert m is not None, line
    return tuple(int(n) for n in m.groups())


def check(funcs, before, instr, after):
    match = []

    for label, fn in funcs.items():
        # print(label, ":")
        compare = fn(instr, before)
        # print(f"after {label}, {before} -> {compare}")
        if compare == after:
            match.append(label)

    return match


def make_reg(op):
    def fn(instr, reg):
        out = list(reg)
        opcode, a, b, c = instr
        out[c] = op(reg[a], reg[b])
        return tuple(out)

    return fn


def run_program(funcs, lines):
    reg = [0, 0, 0, 0]

    for line in lines:
        instr = tuple(int(n) for n in line.split())
        fn = funcs[instr[0]]
        reg = list(fn(instr, reg))

    return reg[0]


def make_imm(op):
    def fn(instr, reg):
        out = list(reg)
        opcode, a, b, c = instr
        out[c] = op(reg[a], b)
        return tuple(out)

    return fn


def make_comp_ir(op):
    def fn(instr, reg):
        out = list(reg)
        opcode, a, b, c = instr
        out[c] = 1 if op(a, reg[b]) else 0
        return tuple(out)

    return fn


def make_comp_ri(op):
    def fn(instr, reg):
        out = list(reg)
        opcode, a, b, c = instr
        out[c] = 1 if op(reg[a], b) else 0
        return tuple(out)

    return fn


def make_comp_rr(op):
    def fn(instr, reg):
        out = list(reg)
        opcode, a, b, c = instr
        out[c] = 1 if op(reg[a], reg[b]) else 0
        return tuple(out)

    return fn


def setr(instr, reg):
    out = list(reg)
    opcode, a, b, c = instr
    out[c] = reg[a]
    return tuple(out)


def seti(instr, reg):
    out = list(reg)
    opcode, a, b, c = instr
    out[c] = a
    return tuple(out)


if __name__ == "__main__":
    main()
