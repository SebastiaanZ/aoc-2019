import concurrent.futures
import functools
import itertools
import logging
from typing import Callable, List, Tuple

from solutions.helpers import IntCodeApplication

log = logging.getLogger(__name__)


def _create_applications(phases: Tuple[int], data: List[int]) -> List[IntCodeApplication]:
    """Create a list of IntCodeApplications with stout -> stdin pipes between them."""
    applications = []

    for i, phase in enumerate(phases, 1):
        if not applications:
            app = IntCodeApplication(data, name=f"amp-{i}")
        else:
            app = IntCodeApplication(data, stdin=applications[-1].stdout, name=f"amp-{i}")
        app.stdin.put(phase)
        applications.append(app)

    return applications


def _run_applications(applications: List[IntCodeApplication]) -> List[IntCodeApplication]:
    """Run the IntCodeApplications listed in `applications` and return them."""
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(applications),
        thread_name_prefix="amp"
    ) as executor:
        futures = {executor.submit(app.run): f"amp-{i}" for i, app in enumerate(applications, 1)}

    done, _ = concurrent.futures.wait(futures)
    for future in done:
        try:
            future.result()
        except Exception:
            log.exception("Something went wrong when running the applications:")
        else:
            log.debug("Ran without issue!")

    return applications


def _setup_apps_part_one(applications: List[IntCodeApplication]) -> List[IntCodeApplication]:
    """Set up the `applications` for part 1."""
    applications[0].stdin.put(0)
    return applications


def _setup_apps_part_two(applications: List[IntCodeApplication]) -> List[IntCodeApplication]:
    """Set up the `applications` for part two."""
    applications[0].stdin.put(0)
    applications[-1].stdout = applications[0].stdin
    return applications


def run_phase_configuration(phases: Tuple[int], data: List[int], setup: Callable) -> int:
    """Run the amps with a single phase configuration and return the final signal strength."""
    applications = _create_applications(phases, data)
    applications = setup(applications)
    applications = _run_applications(applications)

    return applications[-1].stdout.get()


def part_one(data: List[int]) -> int:
    """Find the maximum single strength after chaining together the amps."""
    run_phase = functools.partial(run_phase_configuration, data=data, setup=_setup_apps_part_one)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        signal_strength = executor.map(run_phase, itertools.permutations(range(5), 5))

    return max(signal_strength)


def part_two(data: List[int]) -> int:
    """Find the maximum signal strength after creating a feedback loop with the amps."""
    run_phase = functools.partial(run_phase_configuration, data=data, setup=_setup_apps_part_two)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        signal_strength = executor.map(run_phase, itertools.permutations(range(5, 10), 5))

    return max(signal_strength)


def main(data: List[str]) -> Tuple[int, int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [int(number) for number in data[0].split(",")]

    answer_one = part_one(data=data)
    answer_two = part_two(data=data)
    return answer_one, answer_two
