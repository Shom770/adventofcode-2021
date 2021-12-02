from datetime import datetime
from typing import Callable
from pathlib import Path
from time import sleep
import argparse
import os

from dotenv import load_dotenv
import requests
import rich
from rich import console

load_dotenv()


class APIError(Exception):
    """Exception for if a status code isn't 200."""
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


class AOC:
    """Class for the AOC helper."""
    def __init__(self, day: int = datetime.today().day):
        self.day = day
        self.session = os.environ["COOKIE"]
        self.url = f"https://adventofcode.com/2021/day/{self.day}"

    def submit(self, part: int) -> Callable:
        """Function for submitting an AOC solution."""
        def decorator(function: Callable) -> Callable:
            """Underlying decorator that returns `wrapper`"""
            def wrapper() -> None:
                """Handles submitting."""
                day_name = f"day_{str(self.day).zfill(2)}"

                with open(f"./solutions/{day_name}/input.txt") as file:
                    result = function(file)

                resp = requests.post(
                    url=f"{self.url}/answer",
                    cookies={"session": self.session},
                    data={"level": part, "answer": result}
                )
                match resp.status_code:
                    case 200:
                        success = console.Text(
                            text=f"Your answer for Part {part} for AOC day {self.day} has been submitted!",
                            style="bold green"
                        )
                        rich.print(success)
                    case _:
                        raise APIError(resp.text)
            return wrapper
        return decorator

    def get_input(self):
        day_name = f"day_{str(self.day).zfill(2)}"
        if not os.path.exists(f"./solutions/{day_name}/"):
            os.mkdir(f"./solutions/{day_name}")
            os.chdir(f"./solutions/{day_name}")
            Path(f"{day_name}.py").touch()
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
    cli_args = cli_parser.parse_args()

    aoc = AOC(day=cli_args.input)
    aoc.get_input()


if __name__ == "__main__":
    run_cli()