class Grid:
    def __init__(self, lines: list[str]):
        self.grid = []

        for y, line in enumerate(lines):
            self.grid.append([])
            for x, char in enumerate(line):
                self.grid[-1].append(char)

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

    def move(self):
        moved = 0

        orig = [row.copy() for row in self.grid]
        for y, row in enumerate(orig):
            for x, char in enumerate(row[:]):
                if char == ">":
                    if x + 1 >= len(row) and orig[y][0] == ".":
                        self.grid[y][x], self.grid[y][0] = ".", ">"
                        moved += 1

                    elif x + 1 < len(row) and orig[y][x + 1] == ".":
                        self.grid[y][x], self.grid[y][x + 1] = ".", ">"
                        moved += 1

        orig = [row.copy() for row in self.grid]
        for y, row in enumerate(orig):
            for x, char in enumerate(row):
                if char == "v":
                    if y + 1 >= len(self.grid) and orig[0][x] == ".":
                        self.grid[y][x], self.grid[0][x] = ".", "v"
                        moved += 1

                    elif y + 1 < len(self.grid) and orig[y + 1][x] == ".":
                        self.grid[y][x], self.grid[y + 1][x] = ".", "v"
                        moved += 1

        return moved


def part_one():
    with open("./day_25/input.txt") as file:
        grid = Grid(file.read().splitlines())

        ct = 1
        while grid.move():
            ct += 1

        return ct


print(part_one())
