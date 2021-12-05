from collections import defaultdict


def part_one():
    with open("./day_05/input.txt") as file:
        all_points = defaultdict(int)
        lines = file.read().splitlines()
        for line in lines:
            x1, y1, x2, y2 = map(
                int, line.replace(" -> ", ",").split(",")
            )

            if x1 == x2:
                for x, y in zip((x1,) * (abs(y2 - y1) + 1), range(min((y1, y2)), max((y1, y2)) + 1)):
                    all_points[(x, y)] += 1
            elif y1 == y2:
                for x, y in zip(range(min((x1, x2)), max((x1, x2)) + 1), (y1,) * (abs(x2 - x1) + 1)):
                    all_points[(x, y)] += 1
            else:
                pass

        print(len([value for value in all_points.values() if value >= 2]))


def part_two():
    with open("./day_05/input.txt") as file:
        all_points = defaultdict(int)
        lines = file.read().splitlines()
        for line in lines:
            x1, y1, x2, y2 = map(
                int, line.replace(" -> ", ",").split(",")
            )

            if x1 == x2:
                for x, y in zip((x1,) * (abs(y2 - y1) + 1), range(min((y1, y2)), max((y1, y2)) + 1)):
                    all_points[(x, y)] += 1
            elif y1 == y2:
                for x, y in zip(range(min((x1, x2)), max((x1, x2)) + 1), (y1,) * (abs(x2 - x1) + 1)):
                    all_points[(x, y)] += 1
            elif abs(x1 - x2) == abs(y1 - y2) and x1 != x2 and y1 != y2:
                less_than_x = 1 if x1 < x2 else -1
                less_than_y = 1 if y1 < y2 else -1

                for x, y in zip(
                        range(x1, x2 + less_than_x, less_than_x), range(y1, y2 + less_than_y, less_than_y)
                ):
                    all_points[(x, y)] += 1
            else:
                pass

        print(len([value for value in all_points.values() if value >= 2]))
