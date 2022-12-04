from ast import literal_eval
from datetime import datetime
from textwrap import dedent
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

    def template(self) -> None:
        with open(f"./solutions/day_{str(self.day).zfill(2)}.py", "r+") as file:
            if not file.read():
                raise FileExistsError

            template_string = dedent(""""
            from helper import AOC
            
            aoc = AOC()
            
            @aoc.submit(part=1, run=True, test=True)
            def part_one(file_text: str):
                pass
                
            @aoc.submit(part=2, test=True)
            def part_one(file_text: str):
                pass
            """)
            file.write(template_string)

    def get_sample_input(self) -> tuple[str, Any]:
        resp = requests.get(url=self.url, cookies={"session": self.session})
        soup = BeautifulSoup(resp.text, "lxml")

        for possible_test_input in soup.find_all("pre"):
            preceding_text = possible_test_input.previous_element.previous_element.text.lower()
            if ("for example" in preceding_text or "consider" in preceding_text) and ":" in preceding_text:
                test_input = possible_test_input.text.strip()
            elif len(possible_test_input.text.split("\n")) > 1:
                test_input = possible_test_input.text.strip()

        current_part = soup.find_all("article")[-1]
        last_sentence = current_part.find_all("p")[-2]

        try:
            answer = last_sentence.find_all("code")[-1]
        except IndexError:
            raise RuntimeWarning(
                "Looks like there was an issue with retrieving the test data. Perhaps you could"
                "pass in test data manually or ignore testing altogether?"
            )
        if not answer.em:
            try:
                answer = last_sentence.find_all("em")[-1]
            except IndexError:
                pass

        answer = answer.text.strip().split()[-1]
        try:
            answer = literal_eval(answer)
        except ValueError:
            pass

        return test_input, answer

    def submit(self, part: int, *, run: bool = False, test: bool = False) -> Callable:
        """Function for submitting an AOC solution."""

        if test:
            sample_input, correct_answer = self.get_sample_input()

        def decorator(function: Callable) -> Union[None, Callable]:
            """Underlying decorator that returns `wrapper`"""
            def wrapper() -> None:
                """Handles submitting."""
                day_name = f"day_{str(self.day).zfill(2)}"

                if not test:
                    with open(f"./{day_name}/input.txt") as file:
                        text = file.read().splitlines()
                        result = function(text)
                else:
                    result = function(sample_input.splitlines())

                if not test:
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
                else:
                    assert result == correct_answer, f"Got {result}, was expecting {correct_answer}"

                    rich.print(
                        console.Text(
                            "The sample test case passed!",
                            style="bold green"
                        )
                    )

                    with open(f"./{day_name}/input.txt") as file:
                        text = file.read().splitlines()
                        result = function(text)

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
    cli_parser.add_argument("--template", help="Template a file.", type=bool)
    cli_args = cli_parser.parse_args()

    aoc = AOC(day=cli_args.input or cli_args.test or datetime.today().day, year=cli_args.year or datetime.today().year)
    if cli_args.input:
        aoc.get_input()
    elif cli_args.test:
        aoc.get_sample_input()

    if cli_args.template:
        aoc.template()


if __name__ == "__main__":
    run_cli()
