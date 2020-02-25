# CHACHACHA

[![Build Status](https://travis-ci.org/aogier/chachacha.svg?branch=master)](https://travis-ci.org/aogier/chachacha)
[![codecov](https://codecov.io/gh/aogier/chachacha/branch/master/graph/badge.svg)](https://codecov.io/gh/aogier/chachacha)
[![Package version](https://badge.fury.io/py/chachacha.svg)](https://pypi.org/project/chachacha)

Chachacha changes changelogs.

## Installation

```console
$ pip install chachacha

...
```

## Quickstart

Init a new changelog and then add some changes:

```shell
chachacha init
chachacha added Glad to meet you
cat CHANGELOG.md
```

Subcommands are modeled from [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
specification:

```shell
chachacha --help
Usage: chachacha [OPTIONS] COMMAND [ARGS]...

Options:
  --filename TEXT  changelog filename
  --driver TEXT    changelog format driver
  --help           Show this message and exit.

Commands:
  added       add an "added" entry
  changed     add a "changed" entry
  deprecated  add a "deprecated" entry
  fixed       add a "fixed" entry
  init        initialize a new file
  release     release a version
  removed     add a "removed" entry
  security    add a "security" entry
```

Please note that KeepAChangelog format is a plugin, and implementing other
formats is planned. KAC format driver heavily depends on Colin Bounouar's
[keepachangelog library](https://github.com/Colin-b/keepachangelog).

Releasing a version is simple as:

```shell
chachacha release --help

Usage: chachacha release [OPTIONS]

  release a version

Options:
  --major  overwrite
  --minor  overwrite
  --patch  overwrite
  --help   Show this message and exit.

```

Where:

* major: release a major
* minor: release a minor
* patch: release a patch

Specification on this behavious is directly taken from [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
thanks to python [semver library](https://python-semver.readthedocs.io/en/latest/).
