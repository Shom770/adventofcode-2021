from collections import Counter, defaultdict


def part_one():
    def valid_insertions(insertions):
        return {insertion: to_insert for insertion, to_insert in insertions.items() if insertion in polymers}

    all_insertions = {}
    with open("input.txt") as file:
        for idx, line in enumerate(file):
            line = line.strip()
            if idx == 0:
                polymers = defaultdict(int)
                polymer_string = line
                for first, second in zip(line, line[1:]):
                    polymers[first + second] += 1
            elif line:
                insertion, to_insert = line.split(" -> ")
                all_insertions[insertion] = to_insert

    all_cts = Counter()

    for idx, (key, val) in enumerate(polymers.items()):
        if idx == 0:
            all_cts[key[0]] += val
        all_cts[key[1]] += val

    for step in range(40):
        new_polymers = defaultdict(int, **polymers)

        for insertion, to_insert in all_insertions.items():
            if insertion in polymers.keys() and polymers[insertion] > 0:
                amount = polymers[insertion]

                new_polymers[insertion] -= amount
                if new_polymers[insertion] < 0:
                    new_polymers[insertion] = 0

                all_cts[to_insert] += amount

                new_polymers[insertion[0] + to_insert] += amount

                new_polymers[to_insert + insertion[-1]] += amount

        polymers = new_polymers

    common = all_cts.most_common()

    return common[0][-1] - common[-1][-1]


print(part_one())
