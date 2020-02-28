import os
from datetime import datetime

import keepachangelog
import pytest
from click.testing import CliRunner

from chachacha import drivers, main
from chachacha.configuration import CONFIG_SIGNATURE
from chachacha.drivers.kac import DEFAULT_HEADER

try:
    from dataclasses import asdict
except ImportError:  # pragma: no cover
    from chachacha.vendor_dataclasses import asdict


def test_kac_init(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    with open("CHANGELOG.md") as changelog:

        assert changelog.read() == DEFAULT_HEADER + "\n\n[//]: # (C3-1-DKAC)\n"


def test_kac_init_overwrite(tmp_path, capsys):
    os.chdir(tmp_path)
    filename = "FILENAME.md"

    with open(filename, "w") as changelog:
        changelog.write("foo")

    driver = drivers.kac.ChangelogFormat(filename)
    with pytest.raises(SystemExit):
        driver.init()

    output = capsys.readouterr()
    assert output.out == "file exists\n"

    driver.init(overwrite=True)

    with open("FILENAME.md") as changelog:
        assert changelog.read() == DEFAULT_HEADER + "\n\n[//]: # (C3-1-DKAC)\n"


def test_git_provider_missing_param(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    config = driver.get_config(init=True)

    config.git_provider = "GH"
    driver.write(config=config)
    config.tag_template = "v{t}"
    driver.write(config=config)
    config.driver = "KAC"
    driver.write(config=config)

    for _ in range(3):

        driver.add_entry("added", "a changelog entry string")
        driver.add_entry("added", "a changelog entry string")
        driver.release("major")

    assert (
        open("CHANGELOG.md").read()
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [2.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [1.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string


[//]: # (C3-1-DKAC-GGH-Tv{{t}})
""".format(
            date=datetime.now().isoformat().split("T")[0]
        )
    )


def test_git_provider_full_config(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    config = driver.get_config(init=True)

    config.git_provider = "GH"
    driver.write(config=config)
    config.tag_template = "v{t}"
    driver.write(config=config)
    config.driver = "KAC"
    driver.write(config=config)
    config.repo_name = "aogier/chachacha"
    driver.write(config=config)

    for _ in range(3):

        driver.add_entry("added", "a changelog entry string")
        driver.add_entry("added", "a changelog entry string")
        driver.release("major")

    driver.add_entry("added", "a changelog entry string")

    assert (
        open("CHANGELOG.md").read()
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- a changelog entry string

## [3.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [2.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [1.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

[Unreleased]: https://github.com/aogier/chachacha/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/aogier/chachacha/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/aogier/chachacha/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/aogier/chachacha/releases/tag/v1.0.0

[//]: # (C3-1-DKAC-GGH-Raogier/chachacha-Tv{{t}})
""".format(
            date=datetime.now().isoformat().split("T")[0]
        )
    )


def test_git_provider_gitlab(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    config = driver.get_config(init=True)

    config.git_provider = "GL"
    driver.write(config=config)
    config.tag_template = "v{t}"
    driver.write(config=config)
    config.driver = "KAC"
    driver.write(config=config)
    config.repo_name = "aogier/chachacha"
    driver.write(config=config)

    for _ in range(3):

        driver.add_entry("added", "a changelog entry string")
        driver.add_entry("added", "a changelog entry string")
        driver.release("major")

    driver.add_entry("added", "a changelog entry string")

    assert (
        open("CHANGELOG.md").read()
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- a changelog entry string

## [3.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [2.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [1.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

[Unreleased]: https://gitlab.com/aogier/chachacha/-/compare/v3.0.0...HEAD
[3.0.0]: https://gitlab.com/aogier/chachacha/-/compare/v2.0.0...v3.0.0
[2.0.0]: https://gitlab.com/aogier/chachacha/-/compare/v1.0.0...v2.0.0
[1.0.0]: https://gitlab.com/aogier/chachacha/-/tags/v1.0.0

[//]: # (C3-1-DKAC-GGL-Raogier/chachacha-Tv{{t}})
""".format(
            date=datetime.now().isoformat().split("T")[0]
        )
    )


def test_git_provider_unknown(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    config = driver.get_config(init=True)

    config.git_provider = "XX"
    driver.write(config=config)
    config.tag_template = "v{t}"
    driver.write(config=config)
    config.driver = "KAC"
    driver.write(config=config)
    config.repo_name = "aogier/chachacha"
    driver.write(config=config)

    for _ in range(3):

        driver.add_entry("added", "a changelog entry string")
        driver.add_entry("added", "a changelog entry string")
        driver.release("major")

    driver.add_entry("added", "a changelog entry string")

    assert (
        open("CHANGELOG.md").read()
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- a changelog entry string

## [3.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [2.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string

## [1.0.0] - {date}

### Added

- a changelog entry string
- a changelog entry string


[//]: # (C3-1-DKAC-GXX-Raogier/chachacha-Tv{{t}})
""".format(
            date=datetime.now().isoformat().split("T")[0]
        )
    )


def test_configuration(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()
    config = driver.get_config(init=True)

    found = False
    with open("CHANGELOG.md") as changelog:
        for line in changelog:
            if line.startswith(CONFIG_SIGNATURE):
                found = True

    assert found

    config.driver = "KACZ"
    driver.write(config=config)

    found = False
    with open("CHANGELOG.md") as changelog:
        for line in changelog:
            if line.startswith(CONFIG_SIGNATURE):
                found = True

    assert found

    assert {
        "driver": "KACZ",
        "git_provider": "",
        "repo_name": "",
        "tag_template": "",
    } == asdict(config)


def test_release_major(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("added", "a changelog entry string")
    driver.release("major")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)
    assert parsed == {
        "1.0.0": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "1.0.0",
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2020-02-28

### Added

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_release_minor(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("added", "a changelog entry string")
    driver.release("minor")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)
    assert parsed == {
        "0.1.0": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "0.1.0",
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2020-02-28

### Added

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_release_patch(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("added", "a changelog entry string")
    driver.release("patch")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)
    assert parsed == {
        "0.0.1": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "0.0.1",
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2020-02-28

### Added

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_release(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("added", "a changelog entry string")
    driver.release("patch")
    driver.add_entry("added", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)
    assert parsed == {
        "Unreleased": {
            "added": ["- a changelog entry string"],
            "release_date": None,
            "version": "Unreleased",
        },
        "0.0.1": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "0.0.1",
        },
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- a changelog entry string

## [0.0.1] - 2020-02-28

### Added

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_added(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("added", "a changelog entry string")

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "added": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_changed(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("changed", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "changed": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_deprecated(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("deprecated", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "deprecated": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Deprecated

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_fixed(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("fixed", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "fixed": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_security(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("security", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "security": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Security

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_removed(tmp_path):
    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("removed", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "removed": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Removed

- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )


def test_add_entries(tmp_path):

    os.chdir(tmp_path)
    filename = "CHANGELOG.md"

    driver = drivers.kac.ChangelogFormat(filename)
    driver.init()

    driver.add_entry("removed", "a changelog entry string")
    driver.add_entry("added", "a changelog entry string")
    driver.add_entry("removed", "a changelog entry string")

    parsed = keepachangelog.to_dict(filename, show_unreleased=True)

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "removed": ["- a changelog entry string", "- a changelog entry string"],
            "added": ["- a changelog entry string"],
        }
    }

    with open(filename) as output:
        changelog = output.read()

    assert (
        changelog
        == """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- a changelog entry string

### Removed

- a changelog entry string
- a changelog entry string

[//]: # (C3-1-DKAC)
"""
    )
