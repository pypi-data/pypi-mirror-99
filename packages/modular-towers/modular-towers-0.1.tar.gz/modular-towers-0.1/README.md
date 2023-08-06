# modular-towers

An algorithm that computes modular nested exponents (or towers) efficiently.

## 🚩 Table of Contents

- [Overview](#%EF%B8%8F-overview)
- [Installing](#-installing)
- [Examples](#-examples)

## 🗺️ Overview

`modular-towers` exports a Python function `mod_tower` that takes as input an arbitrarily long sequence of positive integers `a₁, a₂, ..., aₙ` and a positive integer `m` and computes `a₁^(a₂^(···^aₙ)) mod m` efficiently (that is, without computing the value of the nested exponent).

## 🔧 Installing

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