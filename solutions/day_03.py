from helper import AOC

from collections import Counter

aoc = AOC()


# @aoc.submit(1)
# def part_one(file):
#     inp = file.read().splitlines()
#     result = ""
#     epsilon = ""
#
#     for idx in range(0, len(inp[0])):
#         result += Counter([line[idx] for line in inp]).most_common(1)[0][0]
#         epsilon += Counter([line[idx] for line in inp]).most_common(len(inp[0]))[-1][0]
#
#     return int(result, 2) * int(epsilon, 2)

@aoc.submit(2)
def part_two(file):
    inp = file.read().splitlines()

    current_oxygen = list(inp)

    for position in range(len(inp[0])):
        if len(current_oxygen) == 1:
            break

        lines_with_1 = [line for line in current_oxygen if line[position] == "1"]
        lines_with_0 = [line for line in current_oxygen if line[position] == "0"]

        if len(lines_with_1) > len(lines_with_0):
            current_oxygen = list(lines_with_1)
        elif len(lines_with_1) < len(lines_with_0):
            current_oxygen = list(lines_with_0)
        else:
            current_oxygen = list(lines_with_1)

    current_scrubber = list(inp)

    for position in range(len(inp[0])):
        if len(current_scrubber) == 1:
            break

        lines_with_1 = [line for line in current_scrubber if line[position] == "1"]
        lines_with_0 = [line for line in current_scrubber if line[position] == "0"]

        if len(lines_with_1) < len(lines_with_0):
            current_scrubber = list(lines_with_1)
        elif len(lines_with_1) > len(lines_with_0):
            current_scrubber = list(lines_with_0)
        else:
            current_scrubber = list(lines_with_0)

    return int(current_oxygen[0], 2) * int(current_scrubber[0], 2)