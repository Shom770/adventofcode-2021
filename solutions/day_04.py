from helper import AOC

aoc = AOC()


@aoc.submit(part=1)
def part_one(file_text: str):
    def bingo(lst: list):
        for board in lst:
            for row in board:
                if row == ["T" for _ in range(len(row))]:
                    return board, True

        for position in range(len(lst[0][0])):
            for board in lst:
                print((board[0][position], board[1][position], board[2][position], board[3][position], board[4][position]))
                if (board[0][position], board[1][position], board[2][position], board[3][position], board[4][position]) \
                        == ("T") * 5:
                    return board, True

        return False

    order = map(int, file_text[0].split(","))

    file_text = [" ".join(line.split()) for line in file_text if line]
    boards = [[[int(item) for item in line.split() if item.strip().isnumeric()] for line in file_text[num:num+5]] for num in range(1, len(file_text), 5)]

    for number in order:
        for board in boards:
            for row in board:
                try:
                    row[row.index(number)] = "T"
                except ValueError:
                    pass

        result = bingo(boards)
        if result:
            board, _ = bingo(boards)
            break

    sum_of_unmarked = sum([item for row in board for item in row if item != "T"])
    return sum_of_unmarked * number

@aoc.submit(part=2, run=True,)
def part_one(file_text: str):
    def bingo(lst: list):
        all_removes = []
        for board in lst:
            for row in board:
                if row == ["T" for _ in range(len(row))]:
                    if board not in all_removes:
                        all_removes.append(board)

        for position in range(len(lst[0][0])):
            for board in lst:
                if (board[0][position], board[1][position], board[2][position], board[3][position], board[4][position]) \
                        == ("T",) * 5:
                    if board not in all_removes:
                        all_removes.append(board)

        if all_removes:
            return all_removes, True
        else:
            return False

    order = map(int, file_text[0].split(","))

    file_text = [" ".join(line.split()) for line in file_text if line]
    boards = [[[int(item) for item in line.split() if item.strip().isnumeric()] for line in file_text[num:num+5]] for num in range(1, len(file_text), 5)]

    total_len = len(boards) - 1
    boards_knocked_out = []
    for number in order:
        for board in boards:
            for row in board:
                try:
                    row[row.index(number)] = "T"
                except ValueError:
                    pass

        result = bingo(boards)
        if result and len(boards_knocked_out) == total_len:
            board, _ = result
            board = board[0]
            break
        elif result:
            for val in result[0]:
                boards_knocked_out.append(val)
                boards.remove(val)


    sum_of_unmarked = sum([item for row in board for item in row if item != "T"])
    print(sum_of_unmarked * number)