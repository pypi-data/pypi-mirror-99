# xudoku - Solve sudoku using an 'exact cover' algorithm
[![PyPI version](https://badge.fury.io/py/xudoku.svg)](https://badge.fury.io/py/xudoku)
![Run tests, lint, build](https://github.com/jwg4/xudoku/workflows/Run%20tests,%20lint,%20build/badge.svg)
![Deploy to pypi](https://github.com/jwg4/xudoku/workflows/Deploy%20to%20pypi/badge.svg)


This is the sudoku code from @moygit's project 'exact_cover_np'.

The package is maintained by me, @jwg4.

I separated the code for the 'exact cover' algorithm (now available at https://github.com/jwg4/exact_cover) from the sudoku code and created this package. At that package you can find more info about the exact cover algorithm, which can be used for lots of combinatoric problems.

## How to use the package
```
>>> import xudoku
>>> s = xudoku.Sudoku(9)
>>> s.read("tests/files/insight.csv")
>>> sol = s.solve()
>>> sol._sudo.tolist()
[[1, 3, 5, 2, 9, 7, 8, 6, 4], [9, 8, 2, 4, 1, 6, 7, 5, 3], [7, 6, 4, 3, 8, 5, 1, 9, 2], [2, 1, 8, 7, 3, 9, 6, 4, 5], [5, 9, 7, 8, 6, 4, 2, 3, 1], [6, 4, 3, 1, 5, 2, 9, 7, 8], [4, 2, 6, 5, 7, 1, 3, 8, 9], [3, 5, 9, 6, 2, 8, 4, 1, 7], [8, 7, 1, 9, 4, 3, 5, 2, 6]]
>>> s._hardness
'Easy'

```

Currently the puzzle data can only be read from CSV. You could use `io.StringIO`, which turns a string into a file-like object, if you want to generate your sudoku puzzle in code.
