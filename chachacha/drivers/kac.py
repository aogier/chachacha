"""
Created on 25 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""

import os.path
import typing
from datetime import datetime

import keepachangelog
import semver
from jinja2 import Template

DEFAULT_HEADER = """
# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

""".strip()

TEMPLATE = Template(
    """

{{ header }}

{%- for version, changes in current.items() %}

## [{{ version }}]{% if changes.release_date %} - {{ changes.release_date }}{% endif %}
{%- for section in ['added', 'changed', 'deprecated', 'removed', 'fixed', 'security'] %}
{%- if changes[section] %}

### {{ section | title }}
{% for entry in changes[section] %}
{{ entry }}
{%- endfor %}
{%- endif %}
{%- endfor %}
{%- endfor %}
""".strip()
)


class ChangelogFormat:
    def __init__(self, filename):
        self.filename = filename

    def init(self, overwrite: bool = False):
        if os.path.exists(self.filename) and not overwrite:
            print("file exists")
            import sys

            sys.exit(1)

        with open(self.filename, "w") as outfile:
            outfile.write(TEMPLATE.render(header=DEFAULT_HEADER, current={}) + "\n")

        print("changelog created")

    def _write(self, current: dict) -> None:
        with open(self.filename, "w") as outfile:

            outfile.write(
                TEMPLATE.render(header=DEFAULT_HEADER, current=current) + "\n"
            )

    def add_entry(
        self, section_name: str, changelog_line: typing.Union[str, tuple]
    ) -> None:

        _changelog_line = "- " + " ".join(changelog_line)
        current = keepachangelog.to_dict(self.filename, show_unreleased=True)

        if "Unreleased" not in current:
            unreleased = {"Unreleased": {"version": "Unreleased", "release_date": None}}

            new = {}
            new.update(unreleased)
            new.update(current)

            current = new

        else:
            unreleased = current["Unreleased"]

        unreleased = current.setdefault(
            "Unreleased", {"version": "Unreleased", "release_date": None}
        )

        section = unreleased.setdefault(section_name, [])

        section.append(_changelog_line)

        self._write(current)

    def release(self, mode: str) -> None:

        current = keepachangelog.to_dict(self.filename, show_unreleased=True)

        if "Unreleased" not in current:
            print("nothing to bump!")
            import sys

            sys.exit(1)

        try:
            last = [version for version in current if version != "Unreleased"][0]
        except IndexError:
            last = "0.0.0"

        version = semver.parse_version_info(last)

        if mode == "major":
            last = str(version.bump_major())
        elif mode == "minor":
            last = str(version.bump_minor())
        else:
            last = str(version.bump_patch())

        entries = current.pop("Unreleased")

        changelog = {last: entries}
        changelog[last]["release_date"] = datetime.now().isoformat().split("T")[0]
        changelog.update(current)

        self._write(changelog)
