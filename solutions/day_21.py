from collections import defaultdict
from enum import Enum
import itertools
from functools import lru_cache


class Player:
    def __init__(self, position: int) -> None:
        self.all_positions = itertools.cycle(range(1, 11))

        for _ in range(position):
            self.position = next(self.all_positions)

        self.score = 0

    @property
    def won_game(self):
        if self.score >= 1000:
            return True
        else:
            return False


class Die:
    def __init__(self):
        self._die = itertools.cycle(range(1, 101))
        self.times = 0

    @property
    def current_position(self):
        self.times += 1
        return next(self._die)


class Turn:
    PLAYER_1 = 0
    PLAYER_2 = 1


def part_one():
    die = Die()

    with open("./day_21/input.txt") as file:
        player1 = Player(int(file.readline().split(":")[-1]))
        player2 = Player(int(file.readline().split(":")[-1]))

    while True:
        for _ in range(sum([die.current_position for __ in range(3)])):
            player1.position = next(player1.all_positions)

        player1.score += player1.position

        if player1.won_game:
            break

        for _ in range(sum([die.current_position for __ in range(3)])):
            player2.position = next(player2.all_positions)

        player2.score += player2.position

        if player2.won_game:
            break

    if player1.won_game:
        return player2.score * die.times
    else:
        return player1.score * die.times


def part_two():
    with open("./day_21/input.txt") as file:
        player1 = int(file.readline().split(":")[-1])
        player2 = int(file.readline().split(":")[-1])

    @lru_cache(maxsize=None)
    def universes(player1pos, player1score, player2pos, player2score, turn):
        if player1score >= 21:
            return 1, 0

        if player2score >= 21:
            return 0, 1

        player1universes, player2universes = 0, 0

        for poss_roll in itertools.product(range(1, 4), repeat=3):
            rolls = sum(poss_roll)

            if turn == Turn.PLAYER_1:
                new_p1_pos = (player1pos - 1 + rolls) % 10 + 1
                new_p1_score = player1score + new_p1_pos

                p1uni, p2uni = universes(new_p1_pos, new_p1_score, player2pos, player2score, Turn.PLAYER_2)
                player1universes += p1uni
                player2universes += p2uni
            elif turn == Turn.PLAYER_2:
                new_p2_pos = (player2pos - 1 + rolls) % 10 + 1
                new_p2_score = player2score + new_p2_pos

                p1uni, p2uni = universes(player1pos, player1score, new_p2_pos, new_p2_score, Turn.PLAYER_1)
                player1universes += p1uni
                player2universes += p2uni

        return player1universes, player2universes

    return sorted(universes(player1, 0, player2, 0, Turn.PLAYER_1))[-1]


print(part_two())