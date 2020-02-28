"""
Created on 25 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""

import os.path
import typing
from copy import deepcopy
from datetime import datetime

import keepachangelog
import semver

from chachacha.configuration import CONFIG_SIGNATURE, Configuration
from chachacha.drivers.git_provider import Provider


DEFAULT_HEADER = """
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

""".strip()


class ChangelogFormat:
    def __init__(self, filename):
        self.filename = filename

    def init(self, overwrite: bool = False):
        if os.path.exists(self.filename):
            if not overwrite:
                print("file exists")
                import sys

                sys.exit(1)
            else:
                os.unlink(self.filename)

        config = self.get_config(init=True)
        config.driver = "KAC"

        with open(self.filename, "w") as outfile:
            outfile.write(DEFAULT_HEADER + "\n\n")
            outfile.write(config.marshal() + "\n")

        print("changelog created")

    @property
    def dict(self):
        return keepachangelog.to_dict(self.filename, show_unreleased=True)

    def generate_header(self, release):
        out = "## [{version}]".format(version=release["version"])
        if release["release_date"]:
            out += " - {release_date}".format(release_date=release["release_date"])
        return out

    def generate_notes(self, release):
        out = ""
        for section in [
            "added",
            "changed",
            "deprecated",
            "removed",
            "fixed",
            "security",
        ]:
            if section in release:
                out += "### {section}\n\n".format(section=section.capitalize())
                for entry in release[section]:
                    out += "{entry}\n".format(entry=entry)
                out += "\n"

        return out

    def write(self, *, current: dict = None, config: Configuration = None) -> None:
        if not config:
            config = self.get_config(init=True)
            config.driver = "KAC"
        if not current:
            current = keepachangelog.to_dict(self.filename, show_unreleased=True)

        #         ctx = dict(header=DEFAULT_HEADER, current=current)

        if config.git_provider:
            git_provider = Provider(current, config)
        #             ctx["git_provider"] = git_provider

        #         if config:
        #             ctx["config"] = config.marshal()

        with open(self.filename, "w") as outfile:

            outfile.write(DEFAULT_HEADER + "\n\n")

            zcurrent = deepcopy(current)
            for _, changes in zcurrent.items():

                header = self.generate_header(changes)
                outfile.write(header + "\n\n")

                notes = self.generate_notes(changes)
                outfile.write(notes)

            if config.git_provider:

                for tag, url in git_provider.compare():
                    outfile.write("[{tag}]: {url}\n".format(tag=tag, url=url))

                outfile.write("\n")

            outfile.write(config.marshal() + "\n")

    #             outfile.write(TEMPLATE.render(ctx) + "\n")

    def add_entry(
        self, section_name: str, changelog_line: typing.Union[str, tuple]
    ) -> None:

        if isinstance(changelog_line, str):
            changelog_line = (changelog_line,)

        _changelog_line = "- " + " ".join(changelog_line)
        current = keepachangelog.to_dict(self.filename, show_unreleased=True)

        unreleased = current.get("Unreleased")
        if not unreleased:
            unreleased = {"Unreleased": {"version": "Unreleased", "release_date": None}}

            new = {}
            new.update(unreleased)
            new.update(current)

            current = new
            unreleased = current["Unreleased"]

        section = unreleased.setdefault(section_name, [])

        section.append(_changelog_line)

        self.write(current=current)

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
        changelog[last]["version"] = last
        changelog.update(current)

        self.write(current=changelog)

    def get_config(self, *, init=False):

        try:
            with open(self.filename) as changelog:
                for line in changelog:
                    if line.startswith(CONFIG_SIGNATURE):
                        return Configuration.factory(line)

        except FileNotFoundError:
            if init:
                return Configuration.empty()
