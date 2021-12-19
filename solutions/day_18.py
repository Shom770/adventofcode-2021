from ast import literal_eval
from functools import cache
from itertools import permutations
from math import ceil, floor
from time import perf_counter


def timer(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print(f"Time taken: {((perf_counter() - start) * 1000):.3f}ms")
        return result
    return wrapper


@timer
def part_one():
    def magnitude(flattened_list):
        while (min_depth := max(flattened_list, key=lambda x: x[-1])[-1]) != 0:
            all_in_depth = [item for item in flattened_list if item[-1] == min_depth]
            for first, second in zip(all_in_depth[::2], all_in_depth[1::2]):
                idx = flattened_list.index(first)
                flattened_list[idx] = (3 * first[0] + 2 * second[0], first[-1] - 1)
                flattened_list.pop(idx + 1)

        return flattened_list[0][0]

    def explodable(current_num):
        return any(item[-1] == 5 for item in current_num)

    def splittable(current_num):
        return any(item[0] >= 10 for item in current_num)

    def generate_number(current_num, all_pairs, depth=1):
        for pair in current_num:
            if isinstance(pair, int):
                all_pairs.append((pair, depth))
            else:
                generate_number(pair, all_pairs, depth + 1)

        return all_pairs

    with open("./day_18/input.txt") as file:
        snailfish_numbers = file.read().splitlines()
        current_number = generate_number(literal_eval(snailfish_numbers.pop(0)), [])
        while snailfish_numbers:
            next_number = generate_number(literal_eval(snailfish_numbers.pop(0)), [])
            current_number += next_number
            current_number = [(element[0], element[1] + 1) for element in current_number]

            while (exploding := explodable(current_number)) or (splitting := splittable(current_number)):
                if exploding:
                    for idx, (first, second) in enumerate(zip(current_number[:], current_number[1:])):
                        if first[-1] == 5 and second[-1] == 5:
                            if idx + 2 < len(current_number):
                                current_number[idx + 2] = (
                                    current_number[idx + 2][0] + second[0], current_number[idx + 2][-1]
                                )
                            if idx - 1 >= 0:
                                current_number[idx - 1] = (
                                    current_number[idx - 1][0] + first[0], current_number[idx - 1][-1]
                                )

                            current_number[idx] = (0, current_number[idx][-1] - 1)
                            current_number.pop(idx + 1)
                            break
                elif splitting:
                    for idx, number in enumerate(current_number[:]):
                        if number[0] >= 10:
                            current_number[idx] = (floor(number[0] / 2), number[1] + 1)
                            current_number.insert(idx + 1, (ceil(number[0] / 2), number[1] + 1))
                            break

        return magnitude(current_number)


@timer
def part_two():
    def magnitude(flattened_list):
        while (min_depth := max(flattened_list, key=lambda x: x[-1])[-1]) != 0:
            all_in_depth = [item for item in flattened_list if item[-1] == min_depth]
            for first, second in zip(all_in_depth[::2], all_in_depth[1::2]):
                idx = flattened_list.index(first)
                flattened_list[idx] = (3 * first[0] + 2 * second[0], first[-1] - 1)
                flattened_list.pop(idx + 1)

        return flattened_list[0][0]

    def explodable(current_num):
        return any(item[-1] == 5 for item in current_num)

    def splittable(current_num):
        return any(item[0] >= 10 for item in current_num)

    def generate_number(current_num, all_pairs, depth=1):
        for pair in current_num:
            if isinstance(pair, int):
                all_pairs.append((pair, depth))
            else:
                generate_number(pair, all_pairs, depth + 1)

        return all_pairs

    with open("./day_18/input.txt") as file:
        snailfish_numbers = file.read().splitlines()

        @cache
        def two_numbers(first, second):
            current_number = generate_number(literal_eval(first), [])
            next_number = generate_number(literal_eval(second), [])
            current_number += next_number
            current_number = [(element[0], element[1] + 1) for element in current_number]

            while (exploding := explodable(current_number)) or (splitting := splittable(current_number)):
                if exploding:
                    for idx, (first, second) in enumerate(zip(current_number[:], current_number[1:])):
                        if first[-1] == 5 and second[-1] == 5:
                            if idx + 2 < len(current_number):
                                current_number[idx + 2] = (
                                    current_number[idx + 2][0] + second[0], current_number[idx + 2][-1]
                                )
                            if idx - 1 >= 0:
                                current_number[idx - 1] = (
                                    current_number[idx - 1][0] + first[0], current_number[idx - 1][-1]
                                )

                            current_number[idx] = (0, current_number[idx][-1] - 1)
                            current_number.pop(idx + 1)
                            break
                elif splitting:
                    for idx, number in enumerate(current_number[:]):
                        if number[0] >= 10:
                            current_number[idx] = (floor(number[0] / 2), number[1] + 1)
                            current_number.insert(idx + 1, (ceil(number[0] / 2), number[1] + 1))
                            break

            return magnitude(current_number)

        return max([two_numbers(*perm) for perm in permutations(snailfish_numbers, 2)])

part_two()