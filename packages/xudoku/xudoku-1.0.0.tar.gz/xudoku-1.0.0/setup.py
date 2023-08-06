# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xudoku']

package_data = \
{'': ['*']}

install_requires = \
['exact-cover>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['doctest = run_tests:run_doctest',
                     'test = run_tests:test']}

setup_kwargs = {
    'name': 'xudoku',
    'version': '1.0.0',
    'description': "Solve sudoku using an 'exact cover' algorithm.",
    'long_description': '# xudoku - Solve sudoku using an \'exact cover\' algorithm\n[![PyPI version](https://badge.fury.io/py/xudoku.svg)](https://badge.fury.io/py/xudoku)\n![Run tests, lint, build](https://github.com/jwg4/xudoku/workflows/Run%20tests,%20lint,%20build/badge.svg)\n![Deploy to pypi](https://github.com/jwg4/xudoku/workflows/Deploy%20to%20pypi/badge.svg)\n\n\nThis is the sudoku code from @moygit\'s project \'exact_cover_np\'.\n\nThe package is maintained by me, @jwg4.\n\nI separated the code for the \'exact cover\' algorithm (now available at https://github.com/jwg4/exact_cover) from the sudoku code and created this package. At that package you can find more info about the exact cover algorithm, which can be used for lots of combinatoric problems.\n\n## How to use the package\n```\n>>> import xudoku\n>>> s = xudoku.Sudoku(9)\n>>> s.read("tests/files/insight.csv")\n>>> sol = s.solve()\n>>> sol._sudo.tolist()\n[[1, 3, 5, 2, 9, 7, 8, 6, 4], [9, 8, 2, 4, 1, 6, 7, 5, 3], [7, 6, 4, 3, 8, 5, 1, 9, 2], [2, 1, 8, 7, 3, 9, 6, 4, 5], [5, 9, 7, 8, 6, 4, 2, 3, 1], [6, 4, 3, 1, 5, 2, 9, 7, 8], [4, 2, 6, 5, 7, 1, 3, 8, 9], [3, 5, 9, 6, 2, 8, 4, 1, 7], [8, 7, 1, 9, 4, 3, 5, 2, 6]]\n>>> s._hardness\n\'Easy\'\n\n```\n\nCurrently the puzzle data can only be read from CSV. You could use `io.StringIO`, which turns a string into a file-like object, if you want to generate your sudoku puzzle in code.\n',
    'author': 'Moy Easwaran',
    'author_email': None,
    'maintainer': 'Jack Grahl',
    'maintainer_email': 'jack.grahl@gmail.com',
    'url': 'https://github.com/jwg4/xudoku',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
