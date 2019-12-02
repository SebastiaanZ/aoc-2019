# Advent of Code 2019 - My Solutions

![Python Discord - Advent Of Code](https://raw.githubusercontent.com/python-discord/branding/master/logos/logo_seasonal/christmas/2019/banner.png)

This repository contains my solutions to the [Advent of Code 2019](https://adventofcode.com/2019/). For those unfamiliar with the Advent of Code, it is an Advent calendar of programming puzzles for a variety of skill sets and skill levels that can be solved in any programming language. As I'm quite active in an [online Python community](https://pythondiscord.com), I've picked [Python](https://www.python.org/) to solve the puzzles.

## Requirements

- Python 3.8.0
- [SciPy Library](https://www.scipy.org/): numpy, scipy, matplotlib, ipython, jupyter, pandas, sympy, nose
- [NetworkX](https://networkx.github.io/)
- [Requests](https://requests.readthedocs.io/en/master/)

#### Details

As I want to get some experience with the walrus operator (["assignment expressions"](https://www.python.org/dev/peps/pep-0572/)), I've decided to use `Python 3.8.0` for this year's Advent of Code. That means that if you want to run my solutions, you need to make sure that you're using an appropriate version of Python.

I'm also using a number of third-party packages installed from PyPI. As I'm using `pipenv` to manage my virtual environment, I've included both a `Pipfile` and a `Pipfile.lock` to allow you to recreate a virtual environment similar to mine. Use `pipenv sync --dev` to ensure you're using similar versions to those I've used in my solutions. In addition, for those that don't want to use `pipenv`, I've included a `requirements.txt` with a `pip freeze` of my virtual environment.

## Basic Usage

If you want to run my solutions, you can use the following command line arguments from the root `aoc-2019` folder of the repository:

```
python -m solutions --solve [day]
```

To make it easier to run this command using a `pipenv` virtual environment, I've also included a `pipenv` shortcut:

```
pipenv run day [day]
```

## Advanced usage

### Creating a solution directory
You can also use the `solutions` package to create an empty solution folder for a given day based on the template directory located in the `solutions/templates` subdirectory. The command line arguments to do that are:

```
python -m solutions --create [day]
```

There's also a `pipenv` shortcut script:

```py
pipenv run create [day]
```

### Automatically download the input data

When running the solution using `python -m solutions --solve [day]`, the `get_data` function in `solutions.data` can also download the input data for you from the Advent of Code website. For this to work, you need to set the value of your session cookie for the Advent of Code website as the environment variable `AOC_SESSION`. 

Note: The `get_data` function will only download your input data once to limit the number of requests to the Advent of Code website. The data gets stored in a text file located in the `solutions/data` subdirectory and the cached data will be returned on subsequent calls. If you want to force the `get_data` function to bypass this cache and download the data again, specify `use_cache=False` in the function call. 
