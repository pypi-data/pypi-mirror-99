import inspect
import json
import os
from json import JSONDecodeError
from typing import Dict, List

from mosaik_multi_project.multi_project.util.paths import DATA_PATH


def load_simulators() -> List[Dict]:
    _, _, filenames = next(os.walk(DATA_PATH))
    simulators: List[Dict] = []
    for config_file_path in filenames:
        with open(DATA_PATH / config_file_path, 'r') as config_file:
            try:
                simulators += json.load(config_file)['projects']
            except (JSONDecodeError, TypeError) as malformed_json_error:
                print(
                    'Error: '
                    'A function encountered an error where the '
                    'data being deserialized is not a valid JSON document. '
                    'The function:', inspect.stack()[0][3],
                    'The document:', config_file
                )
                raise malformed_json_error

    return simulators
