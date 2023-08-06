from typing import List


def list_operations() -> List[str]:
    operations_list: List[str] = [
        'git-clone',
        'git-remote',
        'git-fetch',
        'git-checkout',
        'git-pull',
        'init-remove',
        'venv-remove',
        'venv',
        'venv-ensure-pip',
        'venv-upgrade-pip',
        'venv-install-pur',
        'venv-pur',
        'venv-install',
        'venv-install-wheel',
        'tox-remove',
        'tox-create',
        'tox-install-pur',
        'tox-pur',
        'tox-create',
        'docker-build',
    ]

    return operations_list
