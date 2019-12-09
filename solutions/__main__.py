import argparse
import importlib
import logging
import pathlib
import shutil
import timeit
import webbrowser

from solutions.data import get_data

log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description='Run or create the solutions for Advent of Code 2019')
parser.add_argument(
    'day',
    type=int,
    choices=range(1, 26),
    help='an integer representing the day'
)
parser.add_argument(
    '-t',
    '--timeit',
    dest="timeit",
    type=int,
    metavar="NUMBER",
    help="test the solution using timeit with NUMBER iterations",
)
parser.add_argument(
    '-a',
    '--alternative',
    dest="alternative",
    type=str,
    metavar="IMPORT_NAME",
    help="run an alternative solution for a day",
)
action_group = parser.add_mutually_exclusive_group(required=True)
action_group.add_argument(
    '-c',
    '--create',
    dest="create",
    action='store_true',
    help='create a directory for the specified day from the solution template'
)
action_group.add_argument(
    '-s',
    '--solve',
    dest="solve",
    action='store_true',
    help='run the solution of the specified day'
)
parser.add_argument(
    "-v",
    "--verbose",
    dest="debug",
    action="store_true",
    help="increase the verbosity of the logger"
)

args = parser.parse_args()

SOLUTIONS_PATH = pathlib.Path(__file__).parent
DAY_PATH = SOLUTIONS_PATH / pathlib.Path(f"day{args.day:0>2d}")

if args.debug:
    log.info("Setting the log level to DEBUG")
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

if args.create:
    template_path = SOLUTIONS_PATH / pathlib.Path("templates/dayx")

    if not DAY_PATH.exists():
        shutil.copytree(template_path, DAY_PATH)
    else:
        log.error("A folder for this day already exists!")

    log.debug(f"Opening a webbrowser to day {args.day}")
    webbrowser.open(f"https://adventofcode.com/2019/day/{args.day}")

if args.solve:
    if not DAY_PATH.exists():
        log.error(f"Can't run solution for day {args.day} as it does not exist yet!")
    else:
        import_path = f"solutions.day{args.day:0>2d}"
        if args.alternative:
            import_path += f".{args.alternative}"
        day = importlib.import_module(import_path)

        if args.timeit:
            execution_times = []
            for _ in range(args.timeit):
                data = get_data(day=args.day)
                time_prior = timeit.default_timer()
                answer_one, answer_two = day.main(data)
                time_after = timeit.default_timer()
                execution_times.append(time_after - time_prior)

            print(f"Answer to part one: {answer_one}")
            print(f"Answer to part two: {answer_two}")

            average_time = sum(execution_times) / len(execution_times)
            print(f"Average running time: {average_time:.6f} seconds ({args.timeit} iterations)")
        else:
            data = get_data(day=args.day)
            time_prior = timeit.default_timer()
            answer_one, answer_two = day.main(data)
            time_after = timeit.default_timer()
            print(f"Answer to part one: {answer_one}")
            print(f"Answer to part two: {answer_two}")
            print(f"Total running time: {time_after - time_prior:.6f} seconds")
