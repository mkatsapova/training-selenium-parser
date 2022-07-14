import pathlib
from typing import Final

ROOT_PATH: Final[pathlib.Path] = pathlib.Path(__file__).parents[1]

RESULTS_FOLDER_PATH: Final[pathlib.Path] = ROOT_PATH.joinpath('results')
