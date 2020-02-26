# CHACHACHA

[![Build Status](https://travis-ci.org/aogier/chachacha.svg?branch=master)](https://travis-ci.org/aogier/chachacha)
[![codecov](https://codecov.io/gh/aogier/chachacha/branch/master/graph/badge.svg)](https://codecov.io/gh/aogier/chachacha)
[![Package version](https://badge.fury.io/py/chachacha.svg)](https://pypi.org/project/chachacha)

Chachacha changes changelogs. This is a tool you can use to keep your changelog tidy,
for now it only supports the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)
specification but the tool's architecture is plugin-based so expect other formats
and/or contribute by yourself what matters! Yay!

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
  release     release a version
  added       add an "added" entry
  changed     add a "changed" entry
  deprecated  add a "deprecated" entry
  fixed       add a "fixed" entry
  removed     add a "removed" entry
  security    add a "security" entry
```

Once again please note that KeepAChangelog format is a plugin, and
implementing other formats is planned/expected. KAC format driver heavily
depends on Colin Bounouar's [keepachangelog library](https://github.com/Colin-b/keepachangelog).

Releasing a version is simple as:

```shell
chachacha release --help

Usage: chachacha release [OPTIONS]

  release a version

Options:
  --major  bump a major version
  --minor  bump a minor version
  --patch  bump a patch version
  --help   Show this message and exit.
```

Where:

* major: release a major
* minor: release a minor
* patch: release a patch

Specification on this behaviour is directly taken from [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
thanks to python [semver library](https://python-semver.readthedocs.io/en/latest/).

## Examples

### Start a changelog, add entries and then bump it

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
```