# modular-towers

An algorithm that computes modular nested exponents (or towers) efficiently.

[![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/avivbrook/modular-towers/Test/master?logo=github&style=flat-square)](https://github.com/avivbrook/modular-towers/actions)
[![PyPI - License](https://img.shields.io/pypi/l/modular-towers?style=flat-square)](https://choosealicense.com/licenses/gpl-3.0/)
[![PyPI](https://img.shields.io/pypi/v/modular-towers?style=flat-square)](https://pypi.org/project/modular-towers/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/modular-towers?style=flat-square)](https://pypi.org/project/modular-towers/#files)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/modular-towers?style=flat-square)](https://pypi.org/project/modular-towers/#files)
[![GitHub issues](https://img.shields.io/github/issues/avivbrook/modular-towers?style=flat-square)](https://github.com/avivbrook/modular-towers/issues)
[![Downloads](https://img.shields.io/badge/dynamic/json?style=flat-square&color=303f9f&label=downloads&query=%24.total_downloads&url=https%3A%2F%2Fapi.pepy.tech%2Fapi%2Fprojects%2Fmodular-towers)](https://pepy.tech/project/modular-towers)

## 🚩 Table of Contents

- [Overview](#%EF%B8%8F-overview)
- [Prerequisites](#%EF%B8%8F-prerequisites)
- [Installation](#-installation)
- [Examples](#-examples)

## 🗺️ Overview

`modular-towers` exports a Python function `mod_tower` that takes as input an arbitrarily long sequence of positive integers `a₁, a₂, ..., aₙ` and a positive integer `m` and computes `a₁^(a₂^(···^aₙ)) mod m` efficiently (that is, without computing the value of the nested exponent).

## 🏳️ Prerequisites

`sympy` is currently required as the algorithm uses its `totient` function. In the future, a custom totient function will be added so that `sympy` is not required, making the module self-contained.

For best performance, install `gmpy2`:
```console
$ apt install libgmp-dev libmpfr-dev libmpc-dev # required for gmpy2
$ pip install gmpy2
```

`gmpy2` is not required but it offers more efficient versions of some of Python's built-in math functions. If `gmpy2` is not installed, the module simply uses the built-in functions.

## 🔧 Installation

Installing with `pip` is the easiest:
```console
$ pip install modular-towers
```

A development version can be installed from GitHub
using `setuptools`, provided you have `sympy` installed already:
```console
$ git clone https://github.com/avivbrook/modular-towers
$ cd modular-towers
$ python setup.py install
```

## 💡 Examples

```python
>>> from modular_towers import mod_tower as modtow
>>> modtow([6,5,4,3,2], 1948502738) # 6^(5^(4^(3^2))) mod 1948502738
951546056
```