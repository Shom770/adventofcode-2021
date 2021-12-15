import heapq
from math import inf
from time import perf_counter
from functools import cache


def part_one():
    def adjacents(x: int, y: int):
        yield from [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    with open("./day_15/input.txt") as file:
        nodes = {(x, y): (inf, inf, inf, (x, y), int(num)) for y, line in enumerate(file.read().splitlines()) for x, num
                 in enumerate(line)}
        open_nodes = []
        end_node = list(nodes.keys())[-1]
        coordinates = (0, 0)
        current_node = nodes[(0, 0)]
        current_node = (0, 0, 0, coordinates, current_node[-1])
        open_nodes.append(current_node)
        closed_nodes = {current_node[-2]}

        while coordinates != end_node:
            for adjacent in adjacents(*coordinates):
                if adjacent in nodes.keys() and adjacent not in closed_nodes and nodes[adjacent] not in open_nodes:
                    neighbor_node = nodes[adjacent]
                    manhattan_dist = abs(neighbor_node[-2][0] - current_node[-2][0]) + abs(
                        neighbor_node[-2][-1] - current_node[-2][-1])
                    risk_factor = current_node[1] + neighbor_node[-1]
                    neighbor_node = (
                        manhattan_dist + risk_factor, risk_factor, manhattan_dist, adjacent, neighbor_node[-1])
                    heapq.heappush(open_nodes, neighbor_node)

            if open_nodes:
                while True:
                    new_node = heapq.heappop(open_nodes)
                    if nodes[new_node[-2]][1] > new_node[1]:
                        current_node = new_node
                        coordinates = new_node[-2]
                        nodes[new_node[-2]] = new_node

                        closed_nodes.add(current_node[-2])
                        break

        return current_node


def part_two():
    @cache
    def adjacents(x: int, y: int):
        yield from [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

    with open("./day_15/input.txt") as file:
        file_text = file.read().splitlines()
        for idx, line in enumerate(file_text):
            first = list(map(int, line))
            second = list(map(lambda x: x + 1 if x + 1 <= 9 else 1, first))
            third = list(map(lambda x: x + 1 if x + 1 <= 9 else 1, second))
            fourth = list(map(lambda x: x + 1 if x + 1 <= 9 else 1, third))
            fifth = list(map(lambda x: x + 1 if x + 1 <= 9 else 1, fourth))

            file_text[idx] = "".join(map(str, first + second + third + fourth + fifth))

        prev_block = file_text[:]
        for _ in range(4):
            new_block = ["".join(map(lambda x: str(int(x) + 1) if int(x) + 1 <= 9 else "1", line))
                         for line in prev_block]
            file_text.extend(
                new_block
            )
            prev_block = new_block

        nodes = {(x, y): (inf, inf, inf, (x, y), int(num)) for y, line in enumerate(file_text) for x, num
                 in enumerate(line)}
        open_nodes = []
        end_node = list(nodes.keys())[-1]
        coordinates = (0, 0)
        current_node = nodes[(0, 0)]
        current_node = (0, 0, 0, coordinates, current_node[-1])
        open_nodes.append(current_node)
        closed_nodes = {current_node[-2]}

        while coordinates != end_node:
            for adjacent in adjacents(*coordinates):
                if adjacent in nodes.keys() and adjacent not in closed_nodes and nodes[adjacent] not in open_nodes:
                    neighbor_node = nodes[adjacent]
                    manhattan_dist = abs(neighbor_node[-2][0] - current_node[-2][0]) + abs(
                        neighbor_node[-2][-1] - current_node[-2][-1])
                    risk_factor = current_node[1] + neighbor_node[-1]
                    neighbor_node = (
                        manhattan_dist + risk_factor, risk_factor, manhattan_dist, adjacent, neighbor_node[-1]
                    )
                    heapq.heappush(open_nodes, neighbor_node)

            if open_nodes:
                while True:
                    new_node = heapq.heappop(open_nodes)
                    if nodes[new_node[-2]][1] > new_node[1]:
                        current_node = new_node
                        coordinates = new_node[-2]
                        nodes[new_node[-2]] = new_node

                        closed_nodes.add(current_node[-2])
                        break

        return current_node[1]


print(part_two())
