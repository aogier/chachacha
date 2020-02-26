"""
Created on 26 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""
import keepachangelog

from chachacha.configuration import Configuration


class Provider:

    compare_template = "https://github.com/{repo_name}/compare/{new}...{old}"
    tag_template = "https://github.com/{repo_name}/releases/tag/{tag}"

    def __init__(self, changelog, config):

        if not config.repo_name:
            raise Exception("missing repo name")

        self.changelog = changelog
        self.config = config

    def compare(self):

        last = "HEAD"
        for release in self.changelog:
            yield last if last != "HEAD" else "Unreleased", self.compare_template.format(
                repo_name=self.config.repo_name,
                new=self.config.tag_template.format(t=release),
                old=self.config.tag_template.format(t=last) if last != "HEAD" else last,
            )
            last = release
        yield last, self.tag_template.format(
            repo_name=self.config.repo_name, tag=self.config.tag_template.format(t=last)
        )
