# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['liter']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['liter = liter.console:app']}

setup_kwargs = {
    'name': 'liter',
    'version': '0.0.2',
    'description': 'Tool for automating basic python packages task.',
    'long_description': '# liter\n\nTool for automating basic python packages task.\n\n## Installation\n\n```shell\npip install liter\n```\n\n## Features\n\n- Changelog autogeneration based on git history.\n- Changing project version recursively\n  \n## How to use\n\n### Generating changelogs\n\nIt will separate the project versions according to the version tags added on git.\n\nTo generate a basic `CHANGELOG.md` file type:\n\n```shell\nliter changelog\n```\n\nIf you want the changelog to start at a specific version type:\n\n```shell\nliter changelog --start-in [VERSION]\n```\n\nExample:\n\n```shell\nliter changelog --start-in 0.2.0\n```\n\n### Changing version\n\nChanging version with **liter** will find all the files in your project recursively where your current package version is written. For each line in every file where a version match is found you can choose if modify the line or not.\n\nTo change project version type:\n\n```shell\nliter version\n```\n\nWhich is the same as:\n\n```shell\nliter version patch\n```\n\nTo upgrade another version number type:\n\n```shell\nliter version minor\n```\n\nor:\n\n```shell\nliter version major\n```\n\nWhere `major`, `minor` and `patch` refers to the 1st, 2nd and 3rd version numbers respectively. (See [Semantic Versioning](https://semver.org/) for mor information).\n\n## Liter config file\n\nWhen runing any command in **liter** a `literconfig.json` file will be created with some default configuraions. You can customize this parameters as you want.\n\n### Config parameters\n\n- `version`\n\n    This is your current package version. By default **liter** will look for a `setup.py` or a `pyproject.toml` to find your current version. If you do not have any of this file you must change the `version` parameter in `literconfig.json` to your current package version.\n\n- `version_ignore`\n\n    List of patters to ignore when searching a version match in files.\n\n- `changelog_sections`\n\n    Sections that will be included in changelog file. Each key, value pair represents the section names and a list of *key words* respectively. A commit will be added to a section if the first word of the commit is any of the sections defined *key word*.\n\n- `changelog_include_others`\n\n    Wheter to include or not the `Others` section in changelogs. The `Other` sections contains all the commits that did not match with any of the *key words* added in any section of `changelog_sections`.\n\n- `changelog_ignore_commits`\n\n    All the commits that match with any of these *key words* will not be included in the changelog file.\n\n- `changelog_only_path_pattern`\n\n    Only include commits that affected files which path contains any of the patterns specified.\n',
    'author': 'Jorge Morgado',
    'author_email': 'jorge.morgadov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
