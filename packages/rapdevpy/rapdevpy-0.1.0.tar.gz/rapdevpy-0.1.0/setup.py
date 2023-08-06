# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rapdevpy']

package_data = \
{'': ['*']}

install_requires = \
['lxml>=4.6.2,<5.0.0', 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['rapdevpy = rapdevpy.runner:run']}

setup_kwargs = {
    'name': 'rapdevpy',
    'version': '0.1.0',
    'description': 'A (personal) rapid development Python library that manages all tests and knowledge for the execution of common tasks.',
    'long_description': '## Rapid Development Library for Python\n\n```\n# Note: Install Python 3\n# Update pip and install virtualenv (dependency encapsulator) and black (linter; IDE needs to be restarted)\n\n# Note: install Poetry for Linux\n$: curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\n# Note: install Poetry for Windows\n$: (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python\n# Note: do NOT update Poetry, it will break itself\n\n$: python get-poetry.py --uninstall\n```\n\n```\n# Note: `.toml` project name and package have to match (rapdevpy; rapdevpy)\n$: poetry install  # install all dependencies\n```\n\n### dist\n\n```\n$: pip install dist/rapdevpy-0.1.3-py3-none.any.whl\n\n$: rapdevpy\n```\n\n### docs\n\n```\n$: poetry shell\n$: cd docs\n# Note: review source/conf.py and source/index.rst\n$: make html\n# Note: see docs in docs/build/apidocs/index.html\n```\n\n### rapdevpy\n\n```\n$: poetry run python ./rapdevpy/runner.py\n```\n\n### tests\n\n```\n$: poetry run pytest --durations=0\n```\n\n```\n$: poetry run pytest --cov=rapdevpy --cov-report=html tests\n#: Note: see coverage report in htmlcov/index.html\n```\n\n### poetry.lock\n\nDependencies, Python version and the virtual environment are managed by `Poetry`.\n\n```\n$: poetry search Package-Name\n$: poetry add Package-Name[==Package-Version]\n```\n\n### pyproject.toml\n\nDefine project entry point and metadata.  \n\n### setup.cfg\n\nConfigure Python libraries.  \n\n### Linters\n\n```\n$: poetry run black .\n```\n\n### cProfile\n\n```\n$: poetry run python ./rapdevpy/profiler.py\n```\n\n### Build and publish\n\n```\n$: poetry build\n\n# Note: get the token from your PiPy account\n$: poetry config pypi-token.pypi PyPI-Api-Access-Token\n$: poetry publish --build\n```\n\n```\nhttps://pypi.org/project/rapdevpy/\n```\n',
    'author': 'Mislav Jaksic',
    'author_email': 'jaksicmislav@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MislavJaksic/rapdevpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
