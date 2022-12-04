from helper import AOC



for day in range(1, 26):
    aoc = AOC(day, 2021)

    data, answer = aoc.get_sample_input()

    print(data, answer)
    print(day)
    print("\n\n------------\n\n")
