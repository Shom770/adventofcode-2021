from helper import AOC

aoc = AOC(day=2)


# @aoc.submit(1, run=True, test=True)
# def part_one(file) -> int:
#     lines = file.read().splitlines()
#     depth, horiz = 0, 0
#     for line in lines:
#         match line.split():
#             case ("forward", num):
#                 horiz += int(num)
#             case ("up", num):
#                 depth -= int(num)
#             case ("down", num):
#                 depth += int(num)
#
#     return depth * horiz


@aoc.submit(2, run=True, test=True)
def part_two(file) -> int:
    lines = file
    depth, horiz, aim = 0, 0, 0
    for line in lines:
        match line.split():
            case ("forward", num):
                horiz += int(num)
                depth += int(num) * aim
            case ("up", num):
                aim -= int(num)
            case ("down", num):
                aim += int(num)

    return depth * horiz