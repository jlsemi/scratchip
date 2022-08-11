import sys
import yaml
import subprocess
import os

from collections import namedtuple

DepInfo = namedtuple('DepInfo', 'name url dest ver')

class DependenciesManager:
    def read_yaml(self, cfg_path):
        with open(cfg_path) as f:
            if sys.version_info.major == 3 and sys.version_info.minor >= 6:
                return yaml.load(f, Loader=yaml.FullLoader)
            else:
                return yaml.load(f)

    def parse_cfg(self, cfg):
        if "dependencies" not in cfg:
            print("Must define 'dependencies' key in CFG")
            sys.exit(-1)
        cfg = cfg["dependencies"]

        deps = []
        for name, info in cfg.items():
            if "ver" in info:
                dep_info = DepInfo(name, info["url"], info["dest"], info["ver"])
            else:
                dep_info = DepInfo(name, info["url"], info["dest"], "")
            deps.append(dep_info)

        return deps

    def __init__(self, cfg_path):
        self.deps = self.parse_cfg(self.read_yaml((cfg_path)))

    def install(self):
        for dep in self.deps:
            self.clone(dep)

    def clone(self, info):
        dest = os.path.join(info.dest, info.name)
        print(dest)
        p = subprocess.run(["git", "clone", info.url, dest])
        if info.ver != "":
            p = subprocess.run(["git", "checkout", info.ver], cwd = dest)
