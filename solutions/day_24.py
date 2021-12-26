from functools import cache


def part_one():
    @cache
    def search(operation_i: int, w: int, x: int, y: int, z: int):
        if operation_i >= len(all_lines):
            return z == 0, ""

        sym_table = {"w": w, "x": x, "y": y, "z": z}

        line = all_lines[operation_i].split()
        match line:
            case ("inp", variable):
                for digit in range(1, 10):
                    sym_table[variable] = digit
                    backtrack = search(operation_i + 1, **sym_table)
                    if backtrack and backtrack[0]:
                        return True, str(digit) + backtrack[1]

                return False

            case ("add", variable, value):
                if value.isnumeric() or "-" in value:
                    sym_table[variable] += int(value)
                else:
                    sym_table[variable] += sym_table[value]
            case ("sub", variable, value):
                if value.isnumeric() or "-" in value:
                    sym_table[variable] -= int(value)
                else:
                    sym_table[variable] -= sym_table[value]
            case ("mul", variable, value):
                if value.isnumeric() or "-" in value:
                    sym_table[variable] *= int(value)
                else:
                    sym_table[variable] *= sym_table[value]
            case ("div", variable, value):
                if value.isnumeric() or "-" in value:
                    sym_table[variable] //= int(value)
                else:
                    sym_table[variable] //= sym_table[value]
            case ("mod", variable, value):
                if value.isnumeric() or "-" in value:
                    sym_table[variable] %= int(value)
                else:
                    sym_table[variable] %= sym_table[value]
            case ("eql", variable, value):
                if value.isnumeric() or "-" in value:
                    sym_table[variable] = int(sym_table[variable] == int(value))
                else:
                    sym_table[variable] = int(sym_table[value] == sym_table[variable])

        return search(operation_i + 1, **sym_table)

    with open("./day_24/input.txt") as file:
        all_lines = file.read().splitlines()

        return search(0, 0, 0, 0, 0)


print(part_one())
