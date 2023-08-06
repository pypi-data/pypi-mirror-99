from typing import List

from mosaik_multi_project.multi_project.library.load_config import \
    load_simulators


def load_project_aliases() -> List[str]:
    simulator_aliases: List = \
        [simulator['alias'] for simulator in load_simulators()]
    return simulator_aliases
