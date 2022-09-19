import sys
import tarfile
import subprocess
import os
import pathlib
import shutil
import scratchip_batteries

class BatteriesManager:
    def __init__(self, prj_path, cfg):
        self.batteries_cfg = scratchip_batteries.batteries
        self.default_cfg = self.parse_cfg(cfg)
        self.prj_path = prj_path

    def parse_cfg(self, cfg):
        if "battery" in cfg:
            cfg = cfg["battery"]
        else:
            cfg = scratchip_batteries.default

        return cfg

    def list_batteries(self):
        for bat in self.batteries_cfg:
            if bat == scratchip_batteries.default:
                print("%s [default]" % bat)
            else:
                print(bat)

    def extract_cache(self, src, dest):
        tar = tarfile.open(src, "r:gz")
        tar.extractall(dest)
        tar.close()

    def init(self):
        if self.default_cfg not in self.batteries_cfg:
            print("Battery ERROR!")
            print("%s not available in:" % self.default_cfg)
            self.list_batteries()
            sys.exit(-1)

        batteries = self.batteries_cfg[self.default_cfg]

        for dir_name, files in batteries.items():
            dir_path = os.path.join(self.prj_path, dir_name)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            for f in files:
                if "tar" in f:
                    self.extract_cache(f, dir_path)
                else:
                    shutil.copy(f, dir_path)
