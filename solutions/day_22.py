def part_one():
    with open("./day_22/input.txt") as file:
        cubes = set()
        for line in file:
            print(line)
            direction, ranges = line.split()
            x_range, y_range, z_range = ranges.split(",")

            x_start, x_end = x_range.replace("x=", "").split("..")
            x_range = range(int(x_start), int(x_end) + 1)

            y_start, y_end = y_range.replace("y=", "").split("..")
            y_range = range(int(y_start), int(y_end) + 1)

            z_start, z_end = z_range.replace("z=", "").split("..")
            z_range = range(int(z_start), int(z_end) + 1)

            if (x_range.start < -50 or x_range.stop > 50) and (y_range.start < -50 or y_range.stop > 50) and (
                    z_range.start < -50 or z_range.stop > 50):
                continue

            x_overlaps, y_overlaps, z_overlaps = set(), set(), set()

            for x in x_range:
                for y in y_range:
                    for z in z_range:
                        if (x < -50 or x > 50) or (y < -50 or y > 50) or (z < -50 or z > 50):
                            continue

                        if direction == "off" and (x, y, z) in cubes:
                            cubes.remove((x, y, z))
                        elif direction == "on":
                            if line == "on x=-22..28,y=-29..23,z=-38..16":
                                if (x, y, z) in cubes:
                                    x_overlaps.add(x)
                                    y_overlaps.add(y)
                                    z_overlaps.add(z)

                            cubes.add((x, y, z))

            print(len(cubes))
            print(x_overlaps, y_overlaps, z_overlaps)

        return len(cubes)


def part_two():
    def calculate_area(cube: tuple):
        return (cube[1] - cube[0] + 1) * (cube[3] - cube[2] + 1) * (cube[5] - cube[4] + 1)

    def intersection(cube1: tuple, cube2: tuple):
        return (
            max(cube1[0], cube2[0]), min(cube1[1], cube2[1]),
            max(cube1[2], cube2[2]), min(cube1[3], cube2[3]),
            max(cube1[4], cube2[4]), min(cube1[5], cube2[5])
        )

    def overlapping(cube1: tuple, cube2: tuple):
        return not (
                cube1[1] < cube2[0] or cube1[0] > cube2[1]
                or cube1[3] < cube2[2] or cube1[2] > cube2[3]
                or cube1[5] < cube2[4] or cube1[4] > cube2[5]
        )

    cubes = []

    with open("./day_22/input.txt") as file:
        for line in file:
            direction, ranges_ = line.split()
            x_range, y_range, z_range = ranges_.split(",")

            x_start, x_end = map(int, x_range.replace("x=", "").split(".."))

            y_start, y_end = map(int, y_range.replace("y=", "").split(".."))

            z_start, z_end = map(int, z_range.replace("z=", "").split(".."))

            current_cube = (x_start, x_end, y_start, y_end, z_start, z_end)
            new_cubes = []

            for cube, sign in cubes:
                if overlapping(current_cube, cube):
                    new_cubes.append((intersection(current_cube, cube), -sign))

            if direction == "on":
                new_cubes.append((current_cube, 1))

            cubes += new_cubes

        return sum(calculate_area(cube) * sign for cube, sign in cubes)


res = part_two()
print(res)