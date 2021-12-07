from functools import lru_cache


def part_one():
  with open("input.txt") as file:
    crabs = [*map(int, file.readline().split(","))]

    median = sorted(crabs)[len(crabs) // 2]
    return sum([abs(item - median) for item in crabs])

def part_two():
  with open("input.txt") as file:
    crabs = sorted([*map(int, file.readline().split(","))])

    @lru_cache()
    def calculate(cur_num, number):
      return sum(range(abs(number - cur_num), -1, -1))

    return min([sum([
      calculate(cur_num, item)
      for item in crabs
    ]) for cur_num in range(crabs[0], crabs[-1] + 1)])