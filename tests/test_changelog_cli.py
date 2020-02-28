import json
import os
from datetime import datetime

import keepachangelog
from click.testing import CliRunner

from chachacha import main
from chachacha.configuration import CONFIG_SIGNATURE
from chachacha.drivers.kac import DEFAULT_HEADER


def test_git_provider_missing_param(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["config", "git_provider", "GH"])
    assert result.exit_code == 0, result.output
    result = runner.invoke(main.main, ["config", "tag_template", "v{t}"])
    assert result.exit_code == 0, result.output
    result = runner.invoke(main.main, ["config", "driver", "KAC"])
    assert result.exit_code == 0, result.output

    for _ in range(3):
        result = runner.invoke(main.main, ["added", "a changelog entry string"])
        assert result.exit_code == 0, result.output
        result = runner.invoke(main.main, ["added", "a changelog entry string"])
        assert result.exit_code == 0, result.output
        result = runner.invoke(main.main, ["release", "--major"])
        assert result.exit_code == 0, result.output

    changelog = open("CHANGELOG.md").read()

    assert (
        changelog
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


def test_git_provider(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["config", "git_provider", "GH"])
    assert result.exit_code == 0
    result = runner.invoke(main.main, ["config", "tag_template", "v{t}"])
    assert result.exit_code == 0
    result = runner.invoke(main.main, ["config", "driver", "KAC"])
    assert result.exit_code == 0
    result = runner.invoke(main.main, ["config", "repo_name", "aogier/chachacha"])
    assert result.exit_code == 0

    for _ in range(3):
        result = runner.invoke(main.main, ["added", "a changelog entry string"])
        assert result.exit_code == 0
        result = runner.invoke(main.main, ["added", "a changelog entry string"])
        assert result.exit_code == 0
        result = runner.invoke(main.main, ["release", "--major"])
        assert result.exit_code == 0

    changelog = open("CHANGELOG.md").read()

    assert (
        changelog
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

[Unreleased]: https://github.com/aogier/chachacha/compare/v3.0.0...HEAD
[3.0.0]: https://github.com/aogier/chachacha/compare/v2.0.0...v3.0.0
[2.0.0]: https://github.com/aogier/chachacha/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/aogier/chachacha/releases/tag/v1.0.0

[//]: # (C3-1-DKAC-GGH-Raogier/chachacha-Tv{{t}})
""".format(
            date=datetime.now().isoformat().split("T")[0]
        )
    )


def test_configuration(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["config", "driver", "KAC"])
    assert result.exit_code == 0

    found = False
    with open("CHANGELOG.md") as changelog:
        for line in changelog:
            if line.startswith(CONFIG_SIGNATURE):
                found = True

    assert found

    result = runner.invoke(main.main, ["config", "driver", "KACZ"])
    assert result.exit_code == 0

    found = False
    with open("CHANGELOG.md") as changelog:
        for line in changelog:
            if line.startswith(CONFIG_SIGNATURE):
                found = True

    assert found

    result = runner.invoke(main.main, ["config"])
    assert result.exit_code == 0

    assert result.output == "driver=KACZ\ngit_provider=\nrepo_name=\ntag_template=\n"


def test_release_major(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    runner.invoke(main.main, ["added", "a changelog entry string"])
    result = runner.invoke(main.main, ["release", "--major"])
    assert result.exit_code == 0

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert parsed == {
        "1.0.0": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "1.0.0",
        }
    }


def test_release_minor(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    runner.invoke(main.main, ["added", "a changelog entry string"])
    result = runner.invoke(main.main, ["release", "--minor"])
    assert result.exit_code == 0

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)

    assert parsed == {
        "0.1.0": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "0.1.0",
        }
    }


def test_release_patch(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    runner.invoke(main.main, ["added", "a changelog entry string"])
    result = runner.invoke(main.main, ["release", "--patch"])
    assert result.exit_code == 0

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert parsed == {
        "0.0.1": {
            "added": ["- a changelog entry string"],
            "release_date": datetime.now().isoformat().split("T")[0],
            "version": "0.0.1",
        }
    }


def test_release(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main.main, ["init"])
    assert result.exit_code == 0

    result = runner.invoke(main.main, ["release"])
    assert result.exit_code == 1

    result = runner.invoke(main.main, ["added", "a changelog entry string"])

    result = runner.invoke(main.main, ["release"])
    assert result.exit_code == 0

    # test changelog entries order creation
    result = runner.invoke(main.main, ["added", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert list(parsed.keys()) == ["Unreleased", "0.0.1"]
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


def test_file_creation(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    result = runner.invoke(main.main, ["init"])

    assert result.exit_code == 0

    with open("CHANGELOG.md") as changelog:

        assert changelog.read() == DEFAULT_HEADER + "\n\n[//]: # (C3-1-DKAC)\n"

    with open("FILENAME.md", "w") as changelog:
        changelog.write("foo")

    result = runner.invoke(main.main, ["--filename", "FILENAME.md", "init"])
    assert result.exit_code == 1

    result = runner.invoke(
        main.main, ["--filename", "FILENAME.md", "init", "--overwrite"]
    )
    assert result.exit_code == 0

    with open("FILENAME.md") as changelog:

        assert changelog.read() == DEFAULT_HEADER + "\n\n[//]: # (C3-1-DKAC)\n"


def test_add_added(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["added", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "added": ["- a changelog entry string"],
        }
    }


def test_add_changed(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["changed", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "changed": ["- a changelog entry string"],
        }
    }


def test_add_deprecated(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["deprecated", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "deprecated": ["- a changelog entry string"],
        }
    }


def test_add_fixed(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["fixed", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "fixed": ["- a changelog entry string"],
        }
    }


def test_add_security(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["security", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "security": ["- a changelog entry string"],
        }
    }


def test_add_removed(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["removed", "a changelog entry string"])
    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)
    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "removed": ["- a changelog entry string"],
        }
    }


def test_add_entries(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["added", "a changelog entry string"])

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)

    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "added": ["- a changelog entry string"],
        }
    }

    result = runner.invoke(
        main.main, ["added", "an", "unquoted", "changelog", "entry", "string"]
    )

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)

    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "added": [
                "- a changelog entry string",
                "- an unquoted changelog entry string",
            ],
        }
    }

    result = runner.invoke(
        main.main, ["changed", "an", "unquoted", "changelog", "entry", "string"]
    )

    parsed = keepachangelog.to_dict("CHANGELOG.md", show_unreleased=True)

    assert result.exit_code == 0

    assert parsed == {
        "Unreleased": {
            "version": "Unreleased",
            "release_date": None,
            "changed": ["- an unquoted changelog entry string"],
            "added": [
                "- a changelog entry string",
                "- an unquoted changelog entry string",
            ],
        }
    }


def test_dict(tmp_path):
    os.chdir(tmp_path)
    runner = CliRunner()
    runner.invoke(main.main, ["init"])

    result = runner.invoke(main.main, ["added", "a changelog entry string"])
    assert result.exit_code == 0

    result = runner.invoke(main.main, ["query"])
    assert result.exit_code == 0

    assert json.loads(result.output) == {
        "Unreleased": {
            "release_date": None,
            "added": ["- a changelog entry string"],
            "version": "Unreleased",
        }
    }
