from ast import literal_eval

def part_one():
    with open("./day_19/input.txt") as file:
        scanners = []
        for line in file:
            if line == "\n":
                continue

            if "---" in line:
                scanners.append([])
            else:
                scanners[-1].append(eval(line))

    beacons = len(scanners[0])
    positions = {0: (0, 0, 0)}
    orig_scanners = scanners[:]

    while len(positions) != len(scanners):
        for idx, scanner in enumerate(scanners):
            print(positions)
            if idx in positions.keys():
                continue

            beacons += len(scanner)
            for indx in positions.keys():
                other_scanner = scanners[indx]

                orientations = [
                    lambda a, b, c: (a, b, c),
                    lambda a, b, c: (b, c, a),
                    lambda a, b, c: (c, a, b),
                    lambda a, b, c: (-a, -b, c),
                    lambda a, b, c: (-b, -c, a),
                    lambda a, b, c: (-c, -a, b),
                    lambda a, b, c: (-a, b, -c),
                    lambda a, b, c: (-b, c, -a),
                    lambda a, b, c: (-c, a, -b),
                    lambda a, b, c: (a, -b, -c),
                    lambda a, b, c: (b, -c, -a),
                    lambda a, b, c: (c, -a, -b),
                    lambda a, b, c: (-a, -c, -b),
                    lambda a, b, c: (-c, -b, -a),
                    lambda a, b, c: (-b, -a, -c),
                    lambda a, b, c: (a, c, -b),
                    lambda a, b, c: (c, b, -a),
                    lambda a, b, c: (b, a, -c),
                    lambda a, b, c: (a, -c, b),
                    lambda a, b, c: (c, -b, a),
                    lambda a, b, c: (b, -a, c),
                    lambda a, b, c: (-a, c, b),
                    lambda a, b, c: (-c, b, a),
                    lambda a, b, c: (-b, a, c),
                ]

                for orientation in orientations:
                    mappings = {
                        (
                            other_coord[0] - orientation(*coord)[0],
                            other_coord[1] - orientation(*coord)[1],
                            other_coord[2] - orientation(*coord)[2]
                        )
                        for other_coord in other_scanner for coord in scanner[:13]
                    }
                    for mapping in mappings:
                        break_out = False
                        transformed = [
                            (
                                orientation(*coordinate)[0] + mapping[0],
                                orientation(*coordinate)[1] + mapping[1],
                                orientation(*coordinate)[2] + mapping[2]
                            ) for coordinate in scanner
                        ]

                        temp_scanner = set(other_scanner)

                        if [
                            item in temp_scanner for item in transformed
                        ].count(True) >= 12:
                            scanners[idx] = transformed
                            positions[idx] = mapping
                            break_out = True
                            break

                    if break_out:
                        break

                if break_out:
                    break

    return len({beacon for scan in scanners for beacon in scan}), orig_scanners, positions


def part_two():
    scanners = {
        0: (0, 0, 0), 6: (1259, -25, 96), 14: (131, 1177, 119), 24: (34, -1251, 105),
        2: (24, -1203, -1060), 13: (42, -1129, 1156), 18: (-8, -1141, 2420), 22: (102, -1253, -2391),
        1: (-1073, -1262, -1084), 5: (8, -2369, 1232), 8: (1185, -1172, 2461), 9: (-1136, -1251, 1226),
        11: (95, -1228, 3607), 12: (-2264, -1282, 1228), 15: (-1229, -1121, -2263), 16: (118, -2436, 2536),
        17: (5, -3612, 2371), 21: (1311, -1135, 3694), 26: (-1170, -2479, 1245), 28: (1242, -2451, 1335),
        3: (-1206, -1134, -3529), 4: (-1215, -1176, 3631), 7: (-1222, -2464, 34), 10: (-1103, -3646, 1333),
        20: (1300, -3697, 1199), 23: (1207, -2384, 98), 27: (2422, -2319, 1314), 19: (2468, -2359, 2369), 25: (2376, -2330, 3618)
    }
    md = []
    for scanner in scanners.values():
        for other_scanner in scanners.values():
            md.append(
                abs(other_scanner[0] - scanner[0]) +
                abs(other_scanner[1] - scanner[1]) +
                abs(other_scanner[2] - scanner[2])
            )

    return max(md)