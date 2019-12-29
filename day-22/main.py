def deal_into_new_stack(cards):
    return list(reversed(cards))


def deal_with_increment(cards, increment):
    n = len(cards)
    result = [-1] * n

    next_index = 0
    for card in cards:
        result[next_index] = card
        next_index = (next_index + increment) % n

    return result


def cut(cards, n):
    return cards[n:] + cards[:n]


def part_one():
    DECK_SIZE = 10007

    cards = []
    for i in range(0, DECK_SIZE):
        cards.append(i)

    lines = []
    with open("./input.txt") as f:
        lines = list(map(str.strip, f.readlines()))

    for line in lines:
        if line == "deal into new stack":
            cards = deal_into_new_stack(cards)
        elif line.startswith("deal with increment"):
            increment = int(line[len("deal with increment ") :])
            cards = deal_with_increment(cards, increment)
        elif line.startswith("cut"):
            n = int(line[len("cut ") :])
            cards = cut(cards, n)
        else:
            raise Exception("unknown line: " + line)

    answer = cards.index(2019)

    print(answer)


if __name__ == "__main__":
    part_one()
