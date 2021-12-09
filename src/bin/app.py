import fire
from pathlib import Path

import os
import sys

WORKING_DIR = str(Path(os.path.realpath(__file__)).parents[2])
sys.path.append(WORKING_DIR)

from src.bin.interface import CLIInterface


def main():
    fire.Fire(CLIInterface)


if __name__ == "__main__":
    main()
