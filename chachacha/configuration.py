"""
Created on 26 feb 2020

@author: Alessandro Ogier <alessandro.ogier@gmail.com>
"""
try:
    from dataclasses import asdict, dataclass, fields
except ImportError:  # pragma: no cover
    from .vendor_dataclasses import asdict, dataclass, fields


CONFIG_SIGNATURE = "[//]: # (C3"


@dataclass
class Configuration:

    conf_map = {
        "D": "driver",
        "G": "git_provider",
        "R": "repo_name",
        "T": "tag_template",
    }

    version = 1
    driver: str
    git_provider: str
    repo_name: str
    tag_template: str

    def marshal(self):
        revmap = {v: k for k, v in self.conf_map.items()}
        conf = []
        for k, v in asdict(self).items():
            if v:
                conf.append(f"{revmap[k]}{v}")
        return f'{CONFIG_SIGNATURE}-{self.version}-{"-".join(sorted(conf))})'

    @staticmethod
    def empty():
        return Configuration(**{k.name: "" for k in fields(Configuration)})

    @staticmethod
    def factory(line):
        *_, conf = line.split()
        # future use
        # _, version, *args = conf.strip("()").split("-")
        _, _, *args = conf.strip("()").split("-")

        configuration = {
            "driver": "",
            "git_provider": "",
            "repo_name": "",
            "tag_template": "",
        }

        for arg in args:
            configuration[Configuration.conf_map[arg[0]]] = arg[1:]

        return Configuration(**configuration)
