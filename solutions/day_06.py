from collections import Counter


def part_one():
    with open("./day_06/input.txt") as file:
        days = 0
        lanternfish = list(map(int, file.readline().split(",")))


        for day in range(1, 81):
            new_lanternfish = lanternfish[:]
            for idx, item in enumerate(lanternfish):
                if item == 0 or (isinstance(item, list) and item[0] == 0):
                    new_lanternfish[idx] = [6, day]
                    new_lanternfish.append([8, day])

            lanternfish = new_lanternfish[:]

            for idx, item in enumerate(lanternfish):
                if isinstance(item, list) and day == item[-1]:
                    pass
                elif isinstance(item, list):
                    lanternfish[idx][0] -= 1
                else:
                    lanternfish[idx] -= 1

        print(len(lanternfish))


def part_two():
    with open("./day_06/input.txt") as file:
        lanternfish = {key: value for key, value in zip(range(0, 9), (0,) * 9)}
        lanternfish.update(
            Counter(list(map(int, file.readline().split(",")))).items()
        )

        for day in range(1, 257):
            if day != 1:
                lanternfish[f"6_{day}"] = lanternfish[0]
                lanternfish[f"8_{day}"] = lanternfish[0]
                try:
                    lanternfish[6] += lanternfish[f"6_{day - 1}"]
                    del lanternfish[f"6_{day - 1}"]
                except KeyError:
                    pass

                try:
                    lanternfish[8] += lanternfish[f"8_{day - 1}"]
                    del lanternfish[f"8_{day - 1}"]
                except KeyError:
                    pass

                lanternfish[0] = 0

            for key, value in lanternfish.items():
                if isinstance(key, int) and value != 0:
                    lanternfish[key - 1] = value
                    lanternfish[key] = 0

        print(sum(lanternfish.values()))


part_two()