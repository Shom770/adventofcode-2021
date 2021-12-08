from itertools import permutations


def part_one():
    with open("input.txt") as file:
        mapping_sizes = {2: 1, 3: 7, 4: 4, 7: 8}
        ct = 0
        for line in file:
            output = line.split("|")[-1].strip().split()
            for digit in output:
                if mapping_sizes.get(len(digit), None) is not None:
                    ct += 1

        print(ct)


def part_two():
    with open("input.txt") as file:
        total = 0
        all_perms = permutations("abcdefg", 7)
        for line in file:
            bruteforce = line.split("|")[0].strip().split()
            "abcdefg"
            """
            1 is {perm[2], perm[-2]},
            2 is {perm[0], perm[2], perm[3], perm[4], perm[-1]3 is {perm[0], perm[2], perm[3], perm[-2], perm[-1]},
            4 is {perm[1], perm[2], perm[3], perm[-2]},
            5 is {perm[0], perm[1], perm[3], perm[-2], perm[-1]}
            6 is {perm[0], perm[1], perm[3], perm[4], perm[-2], perm[-1]}
            7 is {perm[0], perm[2], perm[-2]}
            8 is set(perm)
            9 is {perm[0], perm[1], perm[2], perm[3], perm[-2], perm[-1]}
            }
            """
            output = line.split("|")[-1].strip().split()
            for perm in all_perms:
                if set([item for item in bruteforce if len(item) == 2][0]) - {perm[2], perm[-2]}:
                    continue

                if set([item for item in bruteforce if len(item) == 4][0]) - {perm[1], perm[2], perm[3], perm[-2]}:
                    continue

                if set([item for item in bruteforce if len(item) == 3][0]) - {perm[0], perm[2], perm[-2]}:
                    continue

                if set([item for item in bruteforce if len(item) == 7][0]) - set(perm):
                    continue

                mapping = [
                    (set(perm) - {perm[3]}, "0"),
                    ({perm[2], perm[-2]}, "1"),
                    ({perm[0], perm[2], perm[3], perm[4], perm[-1]}, "2"),
                    ({perm[0], perm[2], perm[3], perm[-2], perm[-1]}, "3"),
                    ({perm[1], perm[2], perm[3], perm[-2]}, "4"),
                    ({perm[0], perm[1], perm[3], perm[-2], perm[-1]}, "5"),
                    ({perm[0], perm[1], perm[3], perm[4], perm[-2], perm[-1]}, "6"),
                    ({perm[0], perm[2], perm[-2]}, "7"),
                    (set(perm), "8"),
                    ({perm[0], perm[1], perm[2], perm[3], perm[-2], perm[-1]}, "9")
                ]

                for dig in output:
                    for set_corr, corresponding in mapping:
                        if len(dig) == len(set_corr) and not set(dig) - set_corr:
                            continue_next = False
                            break_out = False
                            break

                        if set_corr == mapping[-1][0] and corresponding == "9":
                            continue_next = True
                            break_out = True

                    if break_out:
                        break

                if continue_next:
                    continue

                break

            result = ""

            for digit in output:
                if len(digit) == 2:
                    result += "1"
                elif len(digit) == 3:
                    result += "7"
                elif len(digit) == 4:
                    result += "4"
                elif len(digit) == 5:
                    checks = mapping[2], mapping[3], mapping[5]
                    for check in checks:
                        if len(set(digit)) == len(check[0]) and not set(digit) - set(check[0]):
                            result += check[-1]
                elif len(digit) == 6:
                    checks = mapping[0], mapping[6], mapping[9]
                    for check in checks:
                        if len(set(digit)) == len(check[0]) and not set(digit) - set(check[0]):
                            result += check[-1]
                elif len(digit) == 7:
                    result += "8"

            total += int(result)
            all_perms = permutations("abcdefg", 7)
        print(total)