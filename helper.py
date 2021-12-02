from datetime import datetime
import os
from pathlib import Pathlib
from typing import Any, Callable

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
        self.url = f"https://adventofcode.com/day/{self.day}"

    def submit(self, part: int) -> Callable:
        """Function for submitting an AOC solution."""
        def decorator(function: Callable) -> Callable:
            """Underlying decorator that returns `wrapper`"""
            def wrapper(*args, **kwargs) -> None:
                """Handles submitting."""
                result = function(*args, **kwargs)

                resp = requests.post(
                    url=f"{self.url}/answer",
                    cookies=self.session,
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