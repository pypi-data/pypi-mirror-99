# distro-names

`A way to search OS distribution names and versions`

[![Build Status](https://travis-ci.org/igorlg/distro-names.svg?branch=master)](https://travis-ci.org/igorlg/distro-names)

Aren't you tired of searching things like "Which version is Ubuntu Trusty again", or "is Debian 8 _stretch_ or _wheezy_"? Well, I am... so I wrote this small python script to match OS versions with their names and vice versa.

Simply use the CLI to search like this:

```bash
$ distro trusty
Flavour:      Ubuntu
Full Name:    Trusty Thar
Name:         trusty
Versions:     14.04, 14.04.6
```

or use the version:
```bash
$ distro debian 7
Flavour:     Debian
Name:        wheezy
Versions:    7
```

# Install

Using Python pip:

```bash
$ pip install distro-names
```

# Contributing

Please feel free to contribute to this humble project - you can add distro names and versions to `distro/data.py` or improve the search capabilities in `distro/distro.py`.

This is a `pure Python` implementation, so no libs are required. If you'd like to contribute, only PyTest and make are required...
