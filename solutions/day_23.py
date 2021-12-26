import functools

HALLWAYS = [(x, 1) for x in (1, 2, 4, 6, 8, 10, 11)]
ROOMS = [((x, 2), (x, 3)) for x in (3, 5, 7, 9)]
TOPMOST_ROOMS = [room[0] for room in ROOMS]
BOTTOM_MOST_ROOMS = [room[-1] for room in ROOMS]

COLUMNS = {"A": 3, "B": 5, "C": 7, "D": 9}


def solved(grid: dict):
    corresponding = {letter: value for value, letter in zip(range(4), "ABCD")}

    for key, value in grid.items():
        if value.isalpha() and key not in ROOMS[corresponding[value]]:
            return False

    return True


def valid_positions(grid: dict):
    move_nodes = [key for key, value in grid.items()
                  if value.isalpha() and (key in HALLWAYS or grid.get((key[0], key[1] - 1)) == ".")]

    def all_adjacent(x: int, y: int, all_spaces: list):
        for adjacent in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if adjacent in grid.keys() and grid[adjacent] == "." and adjacent not in all_spaces:
                all_spaces.append(adjacent)
                all_adjacent(*adjacent, all_spaces)

        return all_spaces

    corresponding = {}

    for node in move_nodes:
        spaces = all_adjacent(*node, [])
        # Check if the node is in a room
        if node in TOPMOST_ROOMS or (node in BOTTOM_MOST_ROOMS and grid[(node[0], node[1] - 1)] == "."):
            # Check if the node is in its correct room
            if node[0] == COLUMNS[grid[node]]:
                if node[1] == 3:
                    continue
                elif grid[(node[0], node[1] + 1)] == grid[node]:
                    continue

            spaces = [space for space in spaces if space in HALLWAYS]

            if not spaces:
                continue

            corresponding[node] = spaces
        elif node in HALLWAYS:
            spaces = [space for space in spaces if space[0] == COLUMNS[grid[node]] and space[-1] in {2, 3}
                      and (
                              grid[(space[0], 2)] in {".", grid[node]}
                              and grid[(space[0], 3)] in {".", grid[node]}
                      )]

            if not spaces:
                continue

            if (COLUMNS[grid[node]], 2) in spaces and grid[(COLUMNS[grid[node]], 3)] == ".":
                spaces.remove((COLUMNS[grid[node]], 2))

            corresponding[node] = spaces

    return corresponding


def pprint_(grid):
    # ignore this, pretty prints
    x_values = range(0, max(grid.keys(), key=lambda coord: coord[0])[0] + 1)
    y_values = range(0, max(grid.keys(), key=lambda coord: coord[-1])[-1] + 1)

    display = ""

    for y in y_values:
        for x in x_values:
            display += grid[(x, y)]
        display += "\n"

    return display.rstrip("\n")


def part_one():
    with open("./day_23/input.txt") as file:
        inp = file.read().splitlines()
        grid = {}
        energy_cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

        for y, line in enumerate(inp):
            line += " " * (13 - len(line))
            for x, char in enumerate(line):
                grid[(x, y)] = char

        @functools.cache
        def min_energy(grid: tuple):
            grid = dict(grid)

            if solved(grid):
                return 0

            low = float("inf")

            for node, valids in valid_positions(grid).items():
                character = grid[node]
                for valid in valids:
                    calc_cost = (abs(valid[1] - node[1]) + abs(valid[0] - node[0])) * energy_cost[character]
                    grid[node], grid[valid] = ".", character
                    cost_so_far = min_energy(tuple(grid.items()))
                    grid[node], grid[valid] = character, "."

                    if calc_cost + cost_so_far < low:
                        low = calc_cost + cost_so_far

            return low

        return min_energy(tuple(grid.items()))


print(part_one())
