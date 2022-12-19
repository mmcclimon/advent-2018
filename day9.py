class Node:
    def __init__(self, value, prev=None, nxt=None):
        self.value = value
        self.prev = prev if prev is not None else self
        self.next = nxt if nxt is not None else self

    def __repr__(self):
        return f"<marble {self.value}, next={self.next.value}, prev={self.prev.value}" # noqa


# this is just a ring buffer
class Circle:
    def __init__(self):
        zero = Node(value=0)

        self.cur = zero
        self.length = 1

    def __repr__(self) -> str:
        cur = self.cur
        lst = []
        for i in range(self.length):
            lst.append(cur.value)
            cur = cur.next

        return repr(lst)

    def add_marble(self, n: int) -> int:
        if n % 23 == 0:
            cur = self.cur
            for _ in range(7):
                cur = cur.prev

            # remove this marble
            cur.prev.next = cur.next
            cur.next.prev = cur.prev
            self.cur = cur.next
            return n + cur.value

        cur = self.cur
        # we skip a marble here
        prev = cur.next
        succ = prev.next

        marble = Node(value=n, prev=prev, nxt=succ)
        prev.next = marble
        succ.prev = marble

        self.cur = marble
        # print(f"added marble {self.cur}")
        self.length += 1

        return 0


def play_game(n_players: int, end_at: int):
    c = Circle()
    players = [0] * n_players

    for i in range(1, end_at + 1):
        idx = i % n_players
        score = c.add_marble(i)
        players[idx] += score

    print(max(players))


play_game(473, 70904)
play_game(473, 70904 * 100)
