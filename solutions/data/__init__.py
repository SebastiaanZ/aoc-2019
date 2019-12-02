import logging
import os
import pathlib
from typing import List

import requests

log = logging.getLogger(__name__)


class ImpatientPuzzlerError(Exception):
    """This exception is raised when we try to fetch the input data before it became available."""
    pass


def get_data(day: int, use_cache: bool = True) -> List[str]:
    """
    Gets the input data for the given day and returns it as-is as a string.

    To avoid making multiple, unnecessary requests to the Advent of Code server, the puzzle data is
    cached using a flat text file (`day{day}.txt`). If, for some reason, we need a fresh copy of the
    data, the `use_cache` parameter can be used to force a request.
    """

    data_root = pathlib.Path(__file__).parent
    data_file = data_root / pathlib.Path(f"day{day:0>2d}.txt")

    if not data_file.exists() or not use_cache:
        cookies = {"session": os.environ.get("AOC_SESSION")}
        response = requests.get(f"https://adventofcode.com/2019/day/{day}/input", cookies=cookies)
        response.raise_for_status()

        if "Please don't repeatedly request this endpoint before it unlocks!" in response.text:
            raise ImpatientPuzzlerError("The input data is not yet available...")

        data_file.write_text(response.text)
        log.info(f"Fetched input data for day {day} from the Advent of Code website.")
    else:
        log.debug(f"A data file for day {day} already exists; using cached version.")

    return data_file.read_text().splitlines()
