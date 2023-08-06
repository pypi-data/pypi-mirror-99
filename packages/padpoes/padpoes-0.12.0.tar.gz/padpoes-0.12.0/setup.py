# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['padpoes', 'padpoes.checkers']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.20.0,<3.0.0', 'simplelogging>=0.10,<0.12']

entry_points = \
{'console_scripts': ['padpoes = padpoes.padpo:main']}

setup_kwargs = {
    'name': 'padpoes',
    'version': '0.12.0',
    'description': 'Linter for gettext files',
    'long_description': '# padpoes\n\nLinter for gettext files (\\*.po)\n\nForked from https://github.com/AFPy/padpo\n\nCreated to help the translation of official Python docs in Spanish: https://github.com/python/python-docs-es\n\nThanks and creadits to all the python-docs-fr team (L)\n\n\n## License\n\nBSD 3-clause\n\nPull request are welcome.\n\n## Usage\n\nUsing the _activated virtual environment_ created during the installation:\n\nFor a local input file:\n\n```bash\npadpoes --input-path a_file.po\n```\n\nor for a local input directory:\n\n```bash\npadpoes --input-path a_directory_containing_po_files\n```\n\nor for a pull request in python-docs-fr repository (here pull request #978)\n\n```bash\npadpoes --python-docs-fr 978\n```\n\nor for a pull request in a GitHub repository (here python/python-docs-es/pull/978)\n\n```bash\npadpoes --github python/python-docs-fr/pull/978\n```\n\n![Screenshot](screenshot.png)\n\n### Color\n\nBy default, the output is colorless, and formatted like GCC messages. You can use `-c`\nor `--color` option to get a colored output.\n\n## Installation\n\n### Automatic installation\n\n```bash\npip install padpoes\n```\n\n### Manual installation\n\n1. Install dependencies\n\n   ```bash\n   poetry install\n   ```\n\n   Note: this uses `poetry` that you can get here: https://poetry.eustace.io/docs/\n\n2. Use virtual environment$\n\n   ```bash\n   poetry shell\n   ```\n\n## Update on PyPI\n\n`./deliver.sh`\n\n## Changelog\n\n### v0.12.0 (2021-03-22)\n\n- Removes `pygrammalect`\n- Removes NBSP checker\n- Migrates CLI commands to python-docs-es repository\n- Change glossary from French to Spanish\n\n### v0.11.0 (2021-02-02)\n\n- update glossary (fix #58)\n\n### v0.10.0 (2020-12-04)\n\n- use `pygrammalecte` v1.3.0\n- use GitHub Actions\n\n### v0.9.0 (2020-09-07)\n\n- use `pygrammalecte` default message for spelling errors\n\n### v0.8.0 (2020-08-25)\n\n- use [`pygrammalecte`](https://github.com/vpoulailleau/pygrammalecte)\n- add continuous integration\n- fix #12, #13, #14, #15, #17, #18, #20\n- add `--color` CLI option to get a colored output (default is colorless)\n\n### v0.7.0 (2019-12-11)\n\n- add `--version` CLI option to display the current version of `padpo`\n- `--input-path` CLI option now accepts several paths as in\n  `padpo --input-path file1.po file2.po directory1 directory2` or\n  `padpo -i file1.po file2.po directory1 directory2`\n\n### v0.6.0 (2019-12-9)\n\n- check errors against defined glossaries\n\n### v0.5.0 (2019-12-3)\n\n- check spelling errors with grammalecte\n- tag releases!\n\n### v0.4.0 (2019-12-2)\n\n- use poetry: https://poetry.eustace.io/docs/\n- add some tests with tox and pytests\n- fix some false positive issues with grammalecte\n',
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bgeninatti/padpo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
