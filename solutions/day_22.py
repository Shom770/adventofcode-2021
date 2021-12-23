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

            x_overlaps, y_overlaps, z_overlaps = (0, 0, 0)

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
                                    x_overlaps += 1
                                    y_overlaps += 1
                                    z_overlaps += 1

                            cubes.add((x, y, z))

        return len(cubes)


def part_two():
    def overlap_off(range_rem: range, all_ranges: set):
        new_ranges = set()
        x_rem, y_rem, z_rem = set(), set(), set()

        for x_r, y_r, z_r in all_ranges:
            result = overlap((x_r, y_r, z_r), range_rem)
            if isinstance(result, tuple):
                overlap_rem = result
                x_r = range(max((x_r.start, overlap_rem[0].start)), min((x_r.stop, overlap_rem[0].stop)))
                y_r = range(max((y_r.start, overlap_rem[1].start)), min((y_r.stop, overlap_rem[1].stop)))
                z_r = range(max((z_r.start, overlap_rem[2].start)), min((z_r.stop, overlap_rem[2].stop)))

                x_rem = {*x_rem, *tuple(x_r)}
                y_rem = {*y_rem, *tuple(y_r)}
                z_rem = {*z_rem, *tuple(z_r)}

            new_ranges.add((x_r, y_r, z_r))

        return new_ranges, len(x_rem) * len(y_rem) * len(z_rem)

    def overlap(range1: tuple, range2: tuple):
        x1, x2 = range1[0], range2[0]
        y1, y2 = range1[1], range2[1]
        z1, z2 = range1[2], range2[2]

        x_val = range(max((x2.start, x1.start)), min((x2.stop, x1.stop)))
        y_val = range(max((y2.start, y1.start)), min((y2.stop, y1.stop)))
        z_val = range(max((z2.start, z1.start)), min((z2.stop, z1.stop)))

        if not (x1.start <= x_val.start <= x1.stop or x1.start <= x_val.stop <= x1.stop):
            return None

        if not (y1.start <= y_val.start <= y1.stop or y1.start <= y_val.stop <= y1.stop):
            return None

        if not (z1.start <= z_val.start <= z1.stop or z1.start <= z_val.stop <= z1.stop):
            return None

        return x_val, y_val, z_val

    cubes = 0

    with open("./day_22/input.txt") as file:
        ranges = set()
        for line in file:
            direction, ranges_ = line.split()
            x_range, y_range, z_range = ranges_.split(",")

            x_start, x_end = x_range.replace("x=", "").split("..")
            x_range = range(int(x_start), int(x_end) + 1)

            y_start, y_end = y_range.replace("y=", "").split("..")
            y_range = range(int(y_start), int(y_end) + 1)

            z_start, z_end = z_range.replace("z=", "").split("..")
            z_range = range(int(z_start), int(z_end) + 1)

            x_overlaps, y_overlaps, z_overlaps = set(), set(), set()

            remove = False

            for range_ in ranges:
                if direction == "on":
                    result = overlap(range_, (x_range, y_range, z_range))
                    if isinstance(result, tuple):
                        overlap_ = result
                        x_overlaps = set((*x_overlaps, *overlap_[0]))
                        y_overlaps = set((*y_overlaps, *overlap_[1]))
                        z_overlaps = set((*z_overlaps, *overlap_[2]))
                else:
                    ranges, to_remove = overlap_off((x_range, y_range, z_range), ranges)
                    remove = True

            if not remove:
                print(len(x_overlaps))
                print(len(y_overlaps))
                print(len(z_overlaps))

                cubes += (len(x_range) * len(y_range) * len(z_range)) - \
                         (len(x_overlaps) * len(y_overlaps) * len(z_overlaps))
                ranges.add((x_range, y_range, z_range))
            else:
                cubes -= to_remove

            print(cubes)
        return cubes


res = part_one()
print(res == 2758514936282235, abs(res - 2758514936282235), res)