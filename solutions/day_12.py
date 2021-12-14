from collections import defaultdict


def part_one():
    with open("./day_12/input.txt") as file:
        lines = file.read().splitlines()
        cave_system = defaultdict(list)
        for line in lines:
            first, second = line.split("-")
            cave_system[first] += [second,]
            cave_system[second] += [first,]

        paths = 0

        def dfs(lst, key: str = "start"):
            nonlocal paths

            lst.append(key)

            for point in cave_system[key]:
                if point == "end":
                    paths += 1
                elif (point.islower() and point not in lst) or point.isupper():
                    dfs(lst[:], point)

        dfs([])
        print(paths)


def part_two():
    with open("./day_12/input.txt") as file:
        lines = file.read().splitlines()
        cave_system = defaultdict(list)
        for line in lines:
            first, second = line.split("-")
            cave_system[first] += [second,]
            cave_system[second] += [first,]

        paths = 0

        def dfs(dct, key: str = "start"):
            nonlocal paths

            if key not in dct.keys():
                dct[key] = 1
            else:
                dct[key] += 1

            for point in cave_system[key]:
                if point == "start":
                    continue
                elif point == "end":
                    paths += 1
                elif point.islower():
                    if any(value == 2 for key, value in dct.items() if key.islower()) and point not in dct.keys():
                        dfs(dict(dct), point)
                    elif all(value == 1 for key, value in dct.items() if key.islower()):
                        dfs(dict(dct), point)
                elif point.isupper():
                    dfs(dict(dct), point)

        dfs({})

        print(paths)
