# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typed_linter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'typed-linter',
    'version': '0.0.0',
    'description': 'Linter and code quality tool that uses real type information to find bugs and problems',
    'long_description': '# typed-linter\n\n[![Build Status](https://github.com/wemake.services/typed-linter/workflows/test/badge.svg?branch=master&event=push)](https://github.com/wemake.services/typed-linter/actions?query=workflow%3Atest)\n[![codecov](https://codecov.io/gh/wemake.services/typed-linter/branch/master/graph/badge.svg)](https://codecov.io/gh/wemake.services/typed-linter)\n[![Python Version](https://img.shields.io/pypi/pyversions/typed-linter.svg)](https://pypi.org/project/typed-linter/)\n[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)\n\nLinter and code quality tool that uses real type information to find bugs and problems\n\n\n## Installation\n\n```bash\npip install typed-linter\n```\n\n## Credits\n\nThis project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [de63faa912eb36309c37c94bced64bd2cf3584a3](https://github.com/wemake-services/wemake-python-package/tree/de63faa912eb36309c37c94bced64bd2cf3584a3). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/de63faa912eb36309c37c94bced64bd2cf3584a3...master) since then.\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/wemake.services/typed-linter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
