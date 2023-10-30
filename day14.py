def digits(lst) -> str:
    return ''.join(map(str, lst))


class ElfRecipes:
    def __init__(self):
        self.scores = [3, 7]
        self.e1 = 0
        self.e2 = 1

    def _do_round(self):
        new = self.scores[self.e1] + self.scores[self.e2]
        if new >= 10:
            self.scores.extend(divmod(new, 10))
        else:
            self.scores.append(new)

        self.e1 = (self.e1 + self.scores[self.e1] + 1) % len(self.scores)
        self.e2 = (self.e2 + self.scores[self.e2] + 1) % len(self.scores)

    def do_rounds(self, n):
        for _ in range(n + 10):
            self._do_round()

        return digits(self.scores[n:n+10])

    def find_sequence(self, seq):
        n = len(seq)
        while True:
            self._do_round()
            last = digits(self.scores[-n-1:])

            if (idx := last.find(seq)) >= 0:
                return len(self.scores) - n - (1 - idx)


print("part 1:", ElfRecipes().do_rounds(409551))
print("part 2:", ElfRecipes().find_sequence('409551'))

# print(ElfRecipes().find_sequence('515891'))
