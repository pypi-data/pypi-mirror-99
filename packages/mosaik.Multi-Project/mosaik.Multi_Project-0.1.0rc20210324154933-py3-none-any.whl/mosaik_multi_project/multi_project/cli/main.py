from functools import partial
from multiprocessing import cpu_count, Pool
from typing import Union, List

import click

from mosaik_multi_project.multi_project.library.get_log_message_module import \
    get_log_message
from mosaik_multi_project.multi_project.library.list_operations_module import \
    list_operations
from mosaik_multi_project.multi_project.library.load_config import \
    load_simulators
from mosaik_multi_project.multi_project.library.load_project_aliases_module \
    import load_project_aliases
from mosaik_multi_project.multi_project.library.setup_project import \
    setup_project
from mosaik_multi_project.multi_project.library.strings import \
    ALL_OPERATIONS_MAGIC_WORD, ALL_PROJECTS_MAGIC_WORD


@click.command()
@click.option(
    '--project',
    '-p',
    multiple=True,
    default=ALL_PROJECTS_MAGIC_WORD,
    help='The project to manage. Can be repeated.',
    show_default=True,
    type=click.Choice(
        sorted(load_project_aliases() + [ALL_PROJECTS_MAGIC_WORD])
    ),
)
@click.option(
    '--operation',
    '-o',
    multiple=True,
    default=ALL_OPERATIONS_MAGIC_WORD,
    help='The operation to run. Can be repeated.',
    show_default=True,
    type=click.Choice(list_operations() + [ALL_OPERATIONS_MAGIC_WORD]),
)
@click.option(
    '--parallel',
    default=False,
    help='Whether or not to run the commands in parallel per project.',
    show_default=True,
    type=bool,
)
def main(
    *,
    operation: Union[str, List[str]],
    parallel: bool,
    project: Union[str, List[str]],
) -> None:
    # Augment inputs
    if operation[0] == ALL_OPERATIONS_MAGIC_WORD:
        operation = list_operations()
    if project[0] == ALL_PROJECTS_MAGIC_WORD:
        project = load_project_aliases()

    log_message = get_log_message(
        operation=operation,
        parallel=parallel,
        project=project,
    )
    print(log_message)

    projects = [project] if isinstance(project, str) else project

    project_dictionaries = [
        simulator
        for simulator in load_simulators()
        if simulator['alias'] in projects
    ]

    setup_project_partial = partial(
        setup_project, operations=operation,
    )

    if parallel:
        Pool(cpu_count()).map(
            setup_project_partial, project_dictionaries
        )
    if not parallel:
        list(map(
            setup_project_partial, project_dictionaries
        ))

    print('[INFO] Done running operations on projects!')


if __name__ == '__main__':
    main()
