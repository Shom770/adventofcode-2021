from operator import itemgetter


def part_one():
    def _extend(image, occurrences=0):
        new_image = {}
        max_y = max(image.keys(), key=itemgetter(1))[-1]
        max_x = max(image.keys(), key=itemgetter(0))[0] + 3

        if occurrences % 2 == 0:
            if image_algo[0] == "#":
                symb = "."
            else:
                symb = "#"
        else:
            symb = image_algo[0]

        new_image = [symb * max_x] + [f"{symb}{''.join([value for key, value in image.items() if key[-1] == y])}{symb}"
                                      for y in range(max_y + 1)] + [symb * max_x]

        return {(x, y): pixel for y, line in enumerate(new_image) for x, pixel in enumerate(line)}

    def _display_image(image):
        for y in range(max(image.keys(), key=lambda x: x[-1])[-1] + 1):
            for x in range(max(image.keys(), key=lambda x: x[0])[0] + 1):
                print(image[(x, y)], end="")
            print()

    def adjacents(x, y):
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1), (x, y + 1),
                (x + 1, y + 1)]

    def image_algorithm(image_algo, image, occurrences):
        new_image = {}
        max_x = max(image.keys(), key=lambda key: key[0])[0]
        if occurrences % 2 == 0:
            if image_algo[0] == "#":
                symb = "."
            else:
                symb = "#"
        else:
            symb = image_algo[0]

        for _, __ in image.items():
            try:
                next_position = list(new_image.keys())[-1]
            except IndexError:
                next_position = (-1, 0)

            if next_position[0] + 1 > max_x:
                next_position = (0, next_position[1] + 1)
            else:
                next_position = (next_position[0] + 1, next_position[1])

            to_index = int(
                "".join(image[adj] if adj in image.keys() else symb for adj in adjacents(*next_position)).replace("#",
                                                                                                                  "1").replace(
                    ".", "0"), 2)

            new_image[next_position] = image_algo[to_index]

        return new_image

    with open("./day_20/input.txt") as file:
        image_algo, _, *image = file.read().splitlines()

        image = {(x, y): pixel for y, line in enumerate(image) for x, pixel in enumerate(line)}

        image = _extend(image)

        next_img = image_algorithm(image_algo, image, 0)

        new_img = _extend(next_img, 1)
        new_img = image_algorithm(image_algo, new_img, 1)

        return list(new_img.values()).count("#")


def part_two():
    def _extend(image, occurrences=0):
        new_image = {}
        max_y = max(image.keys(), key=itemgetter(1))[-1]
        max_x = max(image.keys(), key=itemgetter(0))[0] + 3

        if occurrences % 2 == 0:
            if image_algo[0] == "#":
                symb = "."
            else:
                symb = "#"
        else:
            symb = image_algo[0]

        new_image = [symb * max_x] + [f"{symb}{''.join([value for key, value in image.items() if key[-1] == y])}{symb}"
                                      for y in range(max_y + 1)] + [symb * max_x]

        return {(x, y): pixel for y, line in enumerate(new_image) for x, pixel in enumerate(line)}

    def _display_image(image):
        for y in range(max(image.keys(), key=lambda x: x[-1])[-1] + 1):
            for x in range(max(image.keys(), key=lambda x: x[0])[0] + 1):
                print(image[(x, y)], end="")
            print()

    def adjacents(x, y):
        return [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1), (x - 1, y), (x, y), (x + 1, y), (x - 1, y + 1), (x, y + 1),
                (x + 1, y + 1)]

    def image_algorithm(image_algo, image, occurrences):
        new_image = {}
        max_x = max(image.keys(), key=lambda key: key[0])[0]
        if occurrences % 2 == 0:
            if image_algo[0] == "#":
                symb = "."
            else:
                symb = "#"
        else:
            symb = image_algo[0]

        for _, __ in image.items():
            try:
                next_position = list(new_image.keys())[-1]
            except IndexError:
                next_position = (-1, 0)

            if next_position[0] + 1 > max_x:
                next_position = (0, next_position[1] + 1)
            else:
                next_position = (next_position[0] + 1, next_position[1])

            to_index = int(
                "".join(image[adj] if adj in image.keys() else symb for adj in adjacents(*next_position)).replace("#", "1").replace(
                    ".", "0"), 2)

            new_image[next_position] = image_algo[to_index]

        return new_image

    with open("./day_20/input.txt") as file:
        image_algo, _, *image = file.read().splitlines()

        image = {(x, y): pixel for y, line in enumerate(image) for x, pixel in enumerate(line)}

        for occurrences in range(50):
            print(occurrences)
            image = _extend(image, occurrences)

            image = image_algorithm(image_algo, image, occurrences)

        return list(image.values()).count("#")

print(part_two())