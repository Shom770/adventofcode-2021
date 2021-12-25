import heapq
from rich import print as rprint
from rich.console import Text

HALLWAYS = [(x, 1) for x in (1, 2, 4, 6, 8, 10, 11)]
ROOMS = [((x, 2), (x, 3)) for x in (3, 5, 7, 9)]
TOPMOST_ROOMS = [room[0] for room in ROOMS]
BOTTOM_MOST_ROOMS = [room[-1] for room in ROOMS]

COLUMNS = {"A": 3, "B": 5, "C": 7, "D": 9}


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
            if node[0] == COLUMNS[grid[node]] and node[1] in {2, 3}:
                continue
            spaces = [space for space in spaces
                      if space in HALLWAYS or (space[0] == COLUMNS[grid[node]] and space[-1] in {2, 3})]
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

            corresponding[node] = spaces

    return corresponding


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

        for node, pos in valid_positions(grid).items():
            for y in range(max(grid.keys(), key=lambda k: k[-1])[-1] + 1):
                for x in range(max(grid.keys(), key=lambda k: k[0])[0] + 1):
                    char = grid[(x, y)]
                    if (x, y) == node:
                        rprint(Text(char, style="bold yellow"), end="")
                    elif (x, y) in pos:
                        rprint(Text("*", style="bold green"), end="")
                    else:
                        rprint(Text(char), end="")
                rprint()
            rprint()
            input()

        # inc = 1
        # heap = [(0, inc, dict(grid))]
        #
        # while heap:
        #     print(grid)
        #     input()
        #     cost, to_run = heapq.heappop(heap).args
        #     to_run()
        #
        #     if grid.finalized():
        #         return cost
        #
        #     for idx, pod in enumerate(grid.pods):
        #         if pod[1] in ROOMS and pod[1][1] != 2:
        #             continue
        #
        #         print(pod[1] in ROOMS, pod)
        #
        #         for position in grid.all_positions_for(pod):
        #             step_cost = (abs(position[1] - pod[1][1]) + abs(position[0] - pod[1][0])) * energy_cost[pod[0]]
        #             heapq.heappush(heap, HeapCalc(cost + step_cost, lambda: grid.pods.__setitem__(idx, (pod[0], position))))


print(part_one())
