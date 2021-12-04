from ast import literal_eval
from datetime import datetime
from typing import Any, Callable, Union
from pathlib import Path
import argparse
import os

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from rich import console
import requests
import rich

load_dotenv()


class APIError(Exception):
    """Exception for if a status code isn't 200."""
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class AOC:
    """Class for the AOC helper."""
    def __init__(self, day: int = datetime.today().day, year: int = datetime.today().year):
        self.day = day
        self.year = year
        self.session = os.environ["COOKIE"]
        self.url = f"https://adventofcode.com/{year}/day/{self.day}"

    def get_sample_input(self) -> tuple[str, Any]:
        resp = requests.get(url=self.url, cookies={"session": self.session})
        soup = BeautifulSoup(resp.text, "lxml")
        test_input = soup.pre.text.strip()

        current_part = soup.find_all("article")[-1]
        last_sentence = current_part.find_all("p")[-2]
        answer = last_sentence.find_all("code")[-1]
        if not answer.em:
            answer = last_sentence.find_all("em")[-1]

        answer = answer.text.strip()
        try:
            answer = literal_eval(answer)
        except ValueError:
            pass

        return test_input, answer

    def submit(self, part: int, *, run: bool = False, test: bool = False) -> Callable:
        """Function for submitting an AOC solution."""
        def decorator(function: Callable) -> Union[None, Callable]:
            """Underlying decorator that returns `wrapper`"""
            def wrapper() -> None:
                """Handles submitting."""
                day_name = f"day_{str(self.day).zfill(2)}"

                with open(f"./{day_name}/input.txt") as file:
                    result = function(file)

                resp = requests.post(
                    url=f"{self.url}/answer",
                    cookies={"session": self.session},
                    data={"level": part, "answer": result}
                )
                match resp.status_code:
                    case 200:
                        success = console.Text(
                            text=resp.text,
                            style="bold green"
                        )
                        rich.print(success)
                    case _:
                        raise APIError(resp.text)

            if run:
                wrapper()
            else:
                return wrapper

        return decorator

    def get_input(self):
        day_name = f"day_{str(self.day).zfill(2)}"
        if not os.path.exists(f"./solutions/{day_name}/"):
            os.mkdir(f"./solutions/{day_name}")
            Path(f"./solutions/{day_name}.py").touch()
            os.chdir(f"./solutions/{day_name}")
            Path(f"input.txt").touch()
            Path("README.md").touch()
            os.chdir(fr"C:\Users\{os.environ['NAME']}\PycharmProjects\adventofcode\adventofcode-2021")

        with open(f"./solutions/{day_name}/input.txt", "w") as file:
            resp = requests.get(f"{self.url}/input", cookies={"session": self.session})
            match resp.status_code:
                case 200:
                    success = console.Text(
                        text=f"The input has been saved in solutions/{day_name}/input.txt!",
                        style="bold green"
                    )
                    rich.print(success)
                case _:
                    raise APIError(resp.text)

            file.write(resp.text)


def run_cli() -> None:
    """Runs the CLI that will get the input."""
    cli_parser = argparse.ArgumentParser(description="A CLI for personal use to make getting AoC input easier")
    cli_parser.add_argument("-input", "--input", help="The day to get the input from.", type=int)
    cli_parser.add_argument("--test", help="Day for getting sample input.", type=int)
    cli_parser.add_argument("--year", help="Year for getting input.", type=int)
    cli_args = cli_parser.parse_args()

    aoc = AOC(day=cli_args.input or cli_args.test, year=cli_args.year)
    if not cli_args.test:
        aoc.get_input()
    else:
        aoc.get_sample_input()


if __name__ == "__main__":
    run_cli()
