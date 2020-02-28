# CHACHACHA

[![Build Status](https://travis-ci.org/aogier/chachacha.svg?branch=master)](https://travis-ci.org/aogier/chachacha)
[![codecov](https://codecov.io/gh/aogier/chachacha/branch/master/graph/badge.svg)](https://codecov.io/gh/aogier/chachacha)
[![Package version](https://badge.fury.io/py/chachacha.svg)](https://pypi.org/project/chachacha)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/chachacha?logo=python&logoColor=%235F9)](https://pypi.org/project/chachacha)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/aogier/chachacha.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/aogier/chachacha/context:python)

Chachacha changes changelogs. This is a tool you can use to keep your changelog tidy,
following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
specification which is the most implemented plugin at the moment.

## Installation

Grab latest copy from [releases page](https://github.com/aogier/chachacha/releases)
and place it where you can invoke it.

Alternatively you can choose to install Python package and cope with `$PATH` configuration.

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
  init        initialize a new file
  config      configure changelog options
  release     release a version
  added       add an "added" entry
  changed     add a "changed" entry
  deprecated  add a "deprecated" entry
  fixed       add a "fixed" entry
  removed     add a "removed" entry
  security    add a "security" entry
```

So you can *add*, *change*, *deprecate*, *fix*, *remove* and *security
announce* your changes.

KAC format plugin driver heavily depends on Colin Bounouar's
[keepachangelog library](https://github.com/Colin-b/keepachangelog).

Releasing a version is simple as:

```shell
chachacha release --help

Usage: main.py release [OPTIONS] [SPEC]

  Update the changelog to release version SPEC.

  SPEC should either be the version number to release or the strings
  "major", "minor" or "patch".

Options:
  --help  Show this message and exit.
```

Specification follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
thanks to python [semver library](https://python-semver.readthedocs.io/en/latest/).

## Configuration

Starting from 0.1.3, Chachacha supports a small configuration system directly
embedded in the file via a hack on Markdown link syntax. This allow for
a number of features like generating compare history:

```shell
chachacha init

chachacha config git_provider GH
chachacha config repo_name aogier/chachacha
chachacha config tag_template 'v{t}'

chachacha added one feature
chachacha added another feature
chachacha release
chachacha security hole
chachacha added capability
cat CHANGELOG.md


[...]
- another feature

[Unreleased]: https://github.com/aogier/chachacha/compare/v0.0.1...HEAD
[0.0.1]: https://github.com/aogier/chachacha/releases/tag/v0.0.1

[//]: # (C3-1-DKAC-GGH-Raogier/chachacha-Tv{t})
```
Configuration system keys are:

* `git_provider`: a git repo provider driver (supported: `GH` for github.com)
* `repo_name`: repo name + namespace your repo is
* `tag_template`: a tag template which maps release versions with tag names.
  Variable `t` will be expanded with the version number.

## Examples

### Start a changelog, add entries and then release

```shell
chachacha init
# quoting is supported
chachacha added "this is a new feature I'm excited about"
chachacha added this is also good
chachacha deprecated this is no longer valid
```

File is now:

```shell
cat CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- this is a new feature I'm excited about
- this is also good

### Deprecated

- this is no longer valid

[//]: # (C3-1-DKAC)
```

Now release it:

```shell
chachacha release
chachacha added new version added item
```

File is now:

```
cat CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- new version added item

## [0.0.1] - 2020-02-26

### Added

- this is a new feature I'm excited about
- this is also good

### Deprecated

- this is no longer valid

[//]: # (C3-1-DKAC)
```