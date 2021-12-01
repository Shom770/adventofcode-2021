with open("input.txt") as file:
  inp = list(map(int, file.readlines()))
  print(len([first < second for first, second in zip(inp, inp[1:]) if first < second]))

with open("input.txt") as file:
  print(len(list(filter(lambda item: item[0] is True, [(inp := [int(line.strip()) for line in file.readlines()]), (prev_sum := sum(inp[0:3])), [[sum(inp[idx:idx+3]) > prev_sum, prev_sum := sum(inp[idx:idx+3])] for idx, _ in enumerate(inp)]][-1]))))