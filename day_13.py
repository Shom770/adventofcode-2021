from ast import literal_eval


def part_two():
    with open("input.txt") as file:
        lines = file.read().splitlines()
        points = []

        fold_axes = []

        for line in lines:
            if "," not in line and "fold along" not in line:
                continue

            try:
                line = literal_eval(line)
                points.append(line)
            except SyntaxError:
                if line.startswith("fold along"):
                    if "x" in line:
                        fold_axes.append(("x", int(line.split("=")[-1])))
                    elif "y" in line:
                        fold_axes.append(("y", int(line.split("=")[-1])))

        for axis in fold_axes:
            if axis[0] == "x":
                reflected = [(2 * axis[1] - point[0], point[1]) for point in points if axis[1] <= point[0]]
                not_reflected = [point for point in points if point[0] < axis[1]]

            if axis[0] == "y":
                reflected = [(point[0], 2 * axis[1] - point[1]) for point in points if axis[1] <= point[1]]
                not_reflected = [point for point in points if point[1] < axis[1]]

            all_pts = sorted(list(set(reflected + not_reflected)), key=lambda x: x[-1])
            points = all_pts

        board = ""

        for y in range(points[-1][-1] + 1):
            for x in range(sorted(points)[-1][0] + 1):
                board += "#" if (x, y) in points else "-"
            board += "\n"

        print(board)
