from itertools import chain
from functools import cache
import math

HALLWAYS = [(x, 1) for x in (1, 2, 4, 6, 8, 10, 11)]
ROOMS = list(chain.from_iterable([((x, 2), (x, 3)) for x in (3, 5, 7, 9)]))


class Grid:
    """The grid of the input."""

    def __init__(self, inp: dict):
        self.grid = inp
        self.pods = []
        self.corresponding = {3: "A", 5: "B", 7: "C", 9: "D"}
        for key, value in self.grid.items():
            if value.isalpha():
                self.pods.append((value, key))

    def __getitem__(self, point_tup: tuple):
        return self.grid[point_tup]

    def __setitem__(self, key, value):
        self.grid[key] = value

    def __str__(self):
        x_values = range(0, max(self.grid.keys(), key=lambda coord: coord[0])[0] + 1)
        y_values = range(0, max(self.grid.keys(), key=lambda coord: coord[-1])[-1] + 1)

        display = ""

        pods = {pod[-1]: pod[0] for pod in self.pods}

        for y in y_values:
            for x in x_values:
                if (x, y) in pods.keys():
                    display += pods[(x, y)]
                elif self.grid[(x, y)].isalpha():
                    display += "."
                else:
                    display += self.grid[(x, y)]
            display += "\n"

        return display.rstrip("\n")

    def __hash__(self):
        return hash(tuple(self.pods))

    def finalized(self):
        all_finalized = []
        for pod in self.pods:
            if pod[0] == "A":
                all_finalized.append(pod[1][0] == 3 and pod[1][1] in (2, 3))
            if pod[0] == "B":
                all_finalized.append(pod[1][0] == 5 and pod[1][1] in (2, 3))
            if pod[0] == "C":
                all_finalized.append(pod[1][0] == 7 and pod[1][1] in (2, 3))
            if pod[0] == "D":
                all_finalized.append(pod[1][0] == 9 and pod[1][1] in (2, 3))

        return all(all_finalized)

    def all_positions_for(self, pod: tuple[str, int, int]):
        char, (x_, y_) = pod
        if x_ == {"A": 3, "B": 5, "C": 7, "D": 9}[char] and y_ in (2, 3):
            return []

        pods = [pod[1] for pod in self.pods]

        def all_adjacent(x: int, y: int, all_spaces: list):
            for adjacent in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if adjacent in self.grid.keys() and (self.grid[adjacent] == "."
                                                     or (self.grid[adjacent] != "#" and adjacent not in pods)) \
                        and adjacent not in all_spaces and adjacent not in pods:
                    all_spaces.append(adjacent)
                    all_adjacent(*adjacent, all_spaces)

            return all_spaces

        spaces = all_adjacent(*pod[1], [])
        if pod[1] in ROOMS:
            return [space for space in spaces if self.grid[(space[0], space[1] + 1)] == "#"]
        elif pod[1] in HALLWAYS:
            return [space for space in spaces
                    if space in ROOMS and self.grid[(space[0], space[1] + 1)] in ("#", pod[0])
                    and pod[0] == self.corresponding[space[0]]
                    ]


def part_one():
    with open("./day_23/input.txt") as file:
        inp = file.read().splitlines()
        grid = {}
        energy_cost = {"A": 1, "B": 10, "C": 100, "D": 1000}

        for y, line in enumerate(inp):
            line += " " * (13 - len(line))
            for x, char in enumerate(line):
                grid[(x, y)] = char

        grid = Grid(grid)

        @cache
        def min_energy(grid: Grid):
            if grid.finalized():
                return 0
            else:
                lowest = math.inf

                for idx, pod in enumerate(grid.pods):
                    char, pos = pod
                    for position in grid.all_positions_for(pod):
                        x1, y1, x2, y2 = (*pos, *position)
                        g_cost = (abs(x2 - x1) + abs(y2 - y1)) * energy_cost[char]
                        grid.pods[idx] = (char, (x2, y2))
                        print(grid.pods[idx])
                        cost_so_far = min_energy(grid)
                        grid.pods[idx] = (char, (x1, y1))
                        if g_cost + cost_so_far < lowest:
                            lowest = g_cost + cost_so_far

                return lowest

        return min_energy(grid)


print(part_one())
