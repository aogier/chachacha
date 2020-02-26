"""
Created on 27 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""

PROVIDERS = {
    "GH": {
        "desc": "Github.com template",
        "compare": "https://github.com/{repo_name}/compare/{new}...{old}",
        "tag": "https://github.com/{repo_name}/releases/tag/{tag}",
    },
    "GL": {
        "desc": "Gitlab.com template",
        "compare": "https://gitlab.com/{repo_name}/-/compare/{new}...{old}",
        "tag": "https://gitlab.com/{repo_name}/-/tags/{tag}",
    },
}


class Provider:
    def __init__(self, changelog, config):

        self.changelog = changelog
        self.config = config

    def compare(self):

        last = "HEAD"
        self.changelog.pop("Unreleased", None)
        # xxx: emit warning?
        if not all((self.config.repo_name, self.config.tag_template)):
            return
        for release in self.changelog:
            yield last if last != "HEAD" else "Unreleased", PROVIDERS[
                self.config.git_provider
            ]["compare"].format(
                repo_name=self.config.repo_name,
                new=self.config.tag_template.format(t=release),
                old=self.config.tag_template.format(t=last) if last != "HEAD" else last,
            )
            last = release

        yield last, PROVIDERS[self.config.git_provider]["tag"].format(
            repo_name=self.config.repo_name, tag=self.config.tag_template.format(t=last)
        )
