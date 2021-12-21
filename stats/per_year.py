from bs4 import BeautifulSoup
import requests


def get_stats(year: int) -> dict:
    soup = BeautifulSoup(requests.get(f"https://adventofcode.com/{year}/stats").text, "lxml")
    soup = soup.body.main.pre

    all_days = [[*map(int, day_stat.split()[:3])] for day_stat in soup.text.split("\n")]
    all_days = [lst for lst in all_days if lst]

    all_stats = {day_info[0]: [*day_info[1:]] for day_info in all_days}

    return all_stats


def take_stats(stats: dict) -> None:
    for key in list(stats.keys())[::-1]:
        print(key)

    print("======")
    for value in list(stats.values())[::-1]:
        print(round(sum(value) / sum(list(stats.values())[-1]), 3))