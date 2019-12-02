import logging
import sys


logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(stream=sys.stdout)]
)
