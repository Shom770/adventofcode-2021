def part_one():
    def adjacents(position: tuple) -> tuple:
        return ((position[0] - 1, position[1] - 1), (position[0], position[1] - 1),
        (position[0] - 1, position[1] + 1), (position[0] - 1, position[1]), (position[0] + 1, position[1]),
        (position[0] + 1, position[1] - 1), (position[0], position[1] + 1), (position[0] + 1, position[1] + 1))

    with open("day_11/input.txt") as file:
        lines = file.read().splitlines()
        octopuses = {(x, y): int(lines[y][x]) for y in range(10) for x in range(10)}

        flashes = 0
        for step in range(100):
            for key in octopuses.keys():
                if octopuses[key] == -1:
                    octopuses[key] = 1
                else:
                    octopuses[key] += 1

            while any(value > 9 for value in octopuses.values()):
                for key, value in octopuses.items():
                    if value > 9:
                        flashes += 1
                        octopuses[key] = -1

                        for position in adjacents(key):
                            if position in octopuses.keys() and octopuses[position] != -1:
                                octopuses[position] += 1

    return flashes


def part_two():
    def adjacents(position: tuple) -> tuple:
        return ((position[0] - 1, position[1] - 1), (position[0], position[1] - 1),
                (position[0] - 1, position[1] + 1), (position[0] - 1, position[1]), (position[0] + 1, position[1]),
                (position[0] + 1, position[1] - 1), (position[0], position[1] + 1),
                (position[0] + 1, position[1] + 1))

    with open("day_11/input.txt") as file:
        lines = file.read().splitlines()
        octopuses = {(x, y): int(lines[y][x]) for y in range(10) for x in range(10)}

        flashes = 0
        step = 1
        while True:
            for key in octopuses.keys():
                if octopuses[key] == -1:
                    octopuses[key] = 1
                else:
                    octopuses[key] += 1

            while any(value > 9 for value in octopuses.values()):
                for key, value in octopuses.items():
                    if value > 9:
                        flashes += 1
                        octopuses[key] = -1

                        for position in adjacents(key):
                            if position in octopuses.keys() and octopuses[position] != -1:
                                octopuses[position] += 1

            if len(octopuses.values()) == len([value for value in octopuses.values() if value == -1]):
                return step
            step += 1
