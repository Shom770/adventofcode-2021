from functools import reduce
from operator import mul


def part_one():
    with open("input.txt") as file:
        heightmap = [list(map(int, list(line))) for line in file.read().splitlines()]

        low_points = []
        for row, lst in enumerate(heightmap):
            for col, item in enumerate(lst):
                if row - 1 >= 0:
                    lower_than_above = item < heightmap[row - 1][col]
                else:
                    lower_than_above = True

                if row + 1 < len(heightmap):
                    lower_than_below = item < heightmap[row + 1][col]
                else:
                    lower_than_below = True

                if col - 1 >= 0:
                    lower_than_left = item < lst[col - 1]
                else:
                    lower_than_left = True

                if col + 1 < len(lst):
                    lower_than_right = item < lst[col + 1]
                else:
                    lower_than_right = True

                if lower_than_above and lower_than_below and lower_than_left and lower_than_right:
                    low_points.append(item)

        return sum(map(lambda x: x + 1, low_points))


print(part_one())


def part_two():
    with open("input.txt") as file:
        heightmap = [list(map(int, list(line))) for line in file.read().splitlines()]
        columns_remaining = {(row, col): item for row, lst in enumerate(heightmap) for col, item in enumerate(lst) if
                             item != 9}

        def bfs(lst, position):
            lst.append((columns_remaining[position], position))
            del columns_remaining[position]

            up_value = (position[0] - 1, position[1])
            down_value = (position[0] + 1, position[1])
            left_value = (position[0], position[1] - 1)
            right_value = (position[0], position[1] + 1)
            if up_value in columns_remaining.keys():
                bfs(lst, up_value)

            if down_value in columns_remaining.keys():
                bfs(lst, down_value)

            if left_value in columns_remaining.keys():
                bfs(lst, left_value)

            if right_value in columns_remaining.keys():
                bfs(lst, right_value)

            return lst

        all_basins = []
        while columns_remaining:
            all_basins.append(bfs([], list(columns_remaining.keys())[0]))

        return reduce(mul, sorted(map(len, all_basins))[-3:])


print(part_two())
