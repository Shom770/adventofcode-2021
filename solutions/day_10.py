def part_one():
    with open("input.txt") as file:
        syntax_stack = []
        PUSH = syntax_stack.append
        POP = syntax_stack.pop

        def PEEK():
            return syntax_stack[-1]

        illegal_chars = []
        opposite = {">": "<", ")": "(", "]": "[", "}": "{"}
        for line in file:
            for char in line:
                if char in ("(", "[", "<", "{"):
                    PUSH(char)
                elif char in (")", "]", ">", "}"):
                    tos = PEEK()
                    if opposite[char] != tos:
                        illegal_chars.append(char)
                        break
                    else:
                        POP()

        return (illegal_chars.count(")") * 3 + illegal_chars.count("]") * 57 + illegal_chars.count(
            "}") * 1197 + illegal_chars.count(">") * 25137)


def part_two():
    with open("input.txt") as file:
        syntax_stack = []

        autocomplete_results = []
        opposite = {"<": ">", "(": ")", "[": "]", "{": "}"}
        for line in file:
            autocomplete = ""
            for char in line:
                if char in ("(", "[", "<", "{"):
                    syntax_stack.append(char)
                elif char in (")", "]", ">", "}"):
                    if {value: key for key, value in opposite.items()}[char] != syntax_stack[-1]:
                        break_out = True
                        break
                    else:
                        break_out = False
                        syntax_stack.pop()

            if break_out:
                syntax_stack = []
                continue

            for remaining in syntax_stack[::-1]:
                autocomplete += opposite[remaining]

            syntax_stack = []

            if autocomplete:
                score_mapping = {")": 1, "]": 2, "}": 3, ">": 4}
                score = 0
                for char in autocomplete:
                    score *= 5
                    score += score_mapping[char]

                autocomplete_results.append(score)

        return sorted(autocomplete_results)[len(autocomplete_results) // 2]


print(part_two())