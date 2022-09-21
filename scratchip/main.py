# See LICENSE for license details.

import pathlib
import argparse
import os
import sys
import pkg_resources
import tarfile
import shutil
import yaml
from pathlib import Path

from .dep_manager import DependenciesManager
from .bat_manager import BatteriesManager
from scratchip import __version__

# Check if this is run from a local installation
scratchipdir = os.path.abspath(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
)
if os.path.exists(os.path.join(scratchipdir, "scratchip")):
    sys.path[0:0] = [scratchipdir]


def read_lines(path):
    with open(path,'r') as f:
        return f.readlines()

def get_resource_name(name):
    return pkg_resources.resource_filename(__name__, name)

def get_resource_string(name):
    return pkg_resources.resource_string(__name__, name)


class ScratChip:
    prj_name = "None"
    prj_path = "None"
    top_name = "None"
    scratchip_path = '.scratchip'
    cfg = None

    def __init__(self, prj_name, cfg):
        self.prj_name = prj_name
        self.prj_path = os.path.abspath(self.prj_name)
        self.bat_path = os.path.join(self.prj_path, self.scratchip_path)
        with open(cfg) as file:
            if sys.version_info.major == 3 and sys.version_info.minor >= 6:
                self.cfg = yaml.load(file, Loader=yaml.FullLoader)
            else:
                print(sys.version_info)
                self.cfg = yaml.load(file)

    def create(self, top):
        self.top_name = top
        if self.prj_name != '.':
            os.mkdir(self.prj_name)

        self.create_dir(self.prj_path, self.cfg["hierarchy"])

        # shutil.copyfile(get_resource_name("assets/default.yaml"), os.path.join(self.prj_path, "config.yaml"))

    def init(self, is_create):
        prj_yml_dest = os.path.join(self.prj_path, 'project.yml')

        # create project's YAML template
        if not os.path.exists(prj_yml_dest):
            prj_yml = get_resource_name("assets/project.yml")
            shutil.copyfile(prj_yml, prj_yml_dest)

        bm = BatteriesManager(self.prj_path, self.read_yaml(prj_yml_dest))
        bm.init(is_create)

    def dump_default_cfg(self, cfg, dump_name):
       shutil.copyfile(cfg, dump_name)

    def create_dir(self, path, dir_tree):
        for (k, v) in dir_tree.items():
            sub_dir = os.path.join(path, k)
            if isinstance(v, dict):
                os.mkdir(sub_dir)
                self.create_dir(sub_dir, v)
            # elif 'chisel.mk' in v:
            #     self.gen_chisel_mk(v, sub_dir)
            #     self.gen_gitignore("assets/gitignore", sub_dir)
            elif 'project.mk' in v:
                self.gen_project_mk(v, sub_dir)
            # elif 'Demo.scala' in v:
            #     self.gen_demo_chisel(v, sub_dir, self.top_name)
            elif v == '':
                os.mkdir(sub_dir)
            else:
                f = get_resource_name(v)
                shutil.copyfile(f, sub_dir)

    # def gen_chisel_mk(self, template, dest):
    #     dest_path = os.path.dirname(os.path.join(self.prj_path, dest))
    #     rel_path = os.path.relpath(self.prj_path, dest_path)
    #     orig = get_resource_string(template).decode("utf-8")
    #     res = orig.format(
    #         mill_path = os.path.join(rel_path, self.scratchip_path + '/mill'),
    #         mill_lib_path = os.path.join(rel_path, self.scratchip_path + '/jars'),
    #         mill_cache_path = os.path.join(rel_path, self.scratchip_path + '/.cache'),
    #         prj_dir=rel_path
    #     )
    #     with open(dest, 'w') as f:
    #         f.write(res)


    def gen_project_mk(self, template, dest):
        dest_path = os.path.dirname(os.path.join(self.prj_path, dest))
        rel_path = os.path.relpath(self.prj_path, dest_path)
        orig = get_resource_string(template).decode("utf-8")
        res = orig.format(
            prj_dir=rel_path,
             mill_path = os.path.join(self.scratchip_path + '/mill'),
            mill_lib_path = os.path.join(self.scratchip_path + '/jars'),
            mill_cache_path = os.path.join(self.scratchip_path + '/cache'),
       )
        with open(dest, 'w') as f:
            f.write(res)

    # def gen_demo_chisel(self, template, dest, top_name):
    #     dest_path = os.path.dirname(os.path.join(self.prj_path, dest))
    #     rel_path = os.path.relpath(self.prj_path, dest_path)
    #     orig = get_resource_string(template).decode("utf-8")
    #     res = orig.format(
    #         top_name=top_name
    #     )
    #     with open(dest.replace("Demo", top_name), 'w') as f:
    #         f.write(res)


    def gen_gitignore(self, template, dest):
        dest_path = os.path.dirname(os.path.join(self.prj_path, dest))
        rel_path = os.path.relpath(dest_path, self.prj_path)
        orig = get_resource_string(template).decode("utf-8")
        res = orig.format(
            out_path=os.path.join(rel_path, 'out')
        )
        with open(os.path.join(self.prj_path, '.gitignore'), 'w') as f:
            f.write(res)

    def extract_cache(self, src, dest):
        tar = tarfile.open(src, "r:gz")
        tar.extractall(dest)
        tar.close()

    def read_yaml(self, cfg_path):
        with open(cfg_path) as file:
            if sys.version_info.major == 3 and sys.version_info.minor >= 6:
                return yaml.load(file, Loader=yaml.FullLoader)
            else:
                return yaml.load(file)

    def gen_filelist_str(self, path_list):
        inc_dir = []
        res = {
            "filelist" : [],
            "dirs"     : [],
            "files"    : [],
        }
        for path in path_list:
            if isinstance(path, dict):
                k, v = list(path.items())[0]
                tag = ''
                if v == "flat_dir":
                    flat_files = [str(p) for p in Path(os.path.abspath(k)).rglob("*.*v")]
                    if not flat_files:
                        print("Warn: %s is empty" % k)
                    res["filelist"].extend([x + "\n" for x in flat_files])
                    res["files"].extend([x + "\n" for x in flat_files])
                elif v == 'flat_filelist':
                    flat_files = read_lines(os.path.abspath(k))
                    res["filelist"].extend(flat_files)
                    res["files"].extend(flat_files)
                elif v == 'is_include_dir':
                    tag = '+incdir+'
                    inc_dir.append("%s%s\n" % (tag, os.path.abspath(k)))
                    res["dirs"].append("%s" % os.path.abspath(k))
                else:
                    if v == 'is_library_file':
                        tag = '-v '
                        res["files"].append("%s" % os.path.abspath(k))
                    elif v == 'is_filelist':
                        tag = '-f '
                        res["files"].append("%s" % os.path.abspath(k))
                    elif v == 'is_library_dir':
                        tag = '-y '
                        res["dirs"].append("%s" % os.path.abspath(k))
                    else:
                        print("Unsupport tag: %s" % v)
                        sys.exit(-1)
                    res["filelist"].append("%s%s\n" % (tag, os.path.abspath(k)))
            else:
                res["filelist"].append(os.path.abspath(path) + "\n")

        res["filelist"] = inc_dir + res["filelist"]
        duplicates = set([x for x in res["filelist"] if res["filelist"].count(x) > 1])
        if duplicates:
            print("WARN: %s" % " ".join(duplicates))
        return res

    def gen_filelist_define(self, defines):
        res = []
        for define in defines:
            if isinstance(define, dict):
                k, v = list(define.items())[0]
                res.append("+define+%s=%d\n" % (k, v))
            else:
                res.append("+define+%s\n" % define)

        return res

    def gen_filelist(self, cfg_path, dest_target):
        cfg = self.read_yaml(cfg_path)
        targets = {}
        yaml_targets = {}
        for target, v in cfg["filelist"].items():
            targets[target] = []
            yaml_targets[target] = {
                "dirs"  : [],
                "files" : [],
            }
            if "defines" in v:
                targets[target] += self.gen_filelist_define(v["defines"])
            if "files" in v:
                res = self.gen_filelist_str(v["files"])
                yaml_targets[target]["files"] += res["files"]
                yaml_targets[target]["dirs" ] += res["dirs" ]
                targets[target] += res["filelist"]
            if "includes" in v:
                for inc_path in v["includes"]:
                    inc_cfg = self.read_yaml(inc_path)
                    if "defines" in inc_cfg:
                        targets[target] += self.gen_filelist_define(inc_cfg["defines"])
                    if "files" in inc_cfg:
                        res =  self.gen_filelist_str(inc_cfg["files"])
                        yaml_targets[target]["files"] += res["files"]
                        yaml_targets[target]["dirs" ] += res["dirs" ]
                        targets[target] += res["filelist"]

        # Filesets Logic
        for target, v in cfg["filelist"].items():
            if "filesets" in v:
                filesets = []
                yaml_filesets = {}
                for other_target in v["filesets"]:
                    filesets += targets[other_target]
                    yaml_targets[target] = {**yaml_targets[other_target], **yaml_targets[target]}
                targets[target] = filesets + targets[target]

        # Remove specified line by keyword
        def remove_line(key_list, line):
            for k in key_list:
              if k in line:
                  return []
            return line
        for target, v in cfg["filelist"].items():
            if "exclude" in v:
                result = []
                for line in targets[target]:
                    result += remove_line(v["exclude"], line)
                targets[target] = result

        dest_dir = "builds/filelist"

        #if not os.path.exists(dest_dir):
            #os.mkdir(dest_dir)
        pathlib.Path(dest_dir).mkdir(parents=True, exist_ok=True)
        if dest_target == "all":
            for target, v in targets.items():
                with open("%s/%s.yaml" % (dest_dir, target), 'w') as f:
                    yaml.dump(yaml_targets[target], f)
                with open("%s/%s.f" % (dest_dir, target), 'w') as f:
                    f.writelines(v)
        elif dest_target in targets:
            with open("%s/%s.yaml" % (dest_dir, dest_target), 'w') as f:
                yaml.dump(yaml_targets[dest_target], f)
            with open("%s/%s.f" % (dest_dir, dest_target), 'w') as f:
                f.writelines(targets[dest_target])
        else:
            print("Not found target: %s" % dest_target)
            print("Available targets: %s" % " ".join(list(targets.keys())))
            sys.exit(-1)

def parse_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser.set_defaults(prj_name='.')
    # Global actions
    parser.add_argument(
        "--version",
        help="Show the ScratChip version",
        action="version",
        version=__version__,
    )

    parser.add_argument(
        "--config",
        help="ScratChip Configure",
        nargs=1,
        default=get_resource_name("assets/default.yaml"),
        type=str,
    )

    # create subparser
    parser_create = subparsers.add_parser(
        "create", help="Create the project"
    )

    parser_create.add_argument(
        'prj_name', metavar='project name', type=str, nargs='?',
        default='.', help='Create Project with name')
    parser_create.add_argument(
        '--top', metavar='top module name', type=str, nargs='?',
        default='Top', help='Top Module Name')
    parser_create.set_defaults(func=create)

    # init subparser
    parser_init = subparsers.add_parser(
        "init", help="Initialize the project"
    )

    parser_init.add_argument(
        'prj_name', metavar='project name', type=str, nargs='?',
        default='.', help='Initialize Project specify by name')
    parser_init.set_defaults(func=init)

    # dump cfg subparser
    parser_dump_cfg = subparsers.add_parser(
        "dump_cfg", help="Dump configuare with YAML"
    )

    parser_dump_cfg.add_argument(
        'dump_name', type=str, nargs='?',
        default='config.yml', help='Dump Configure file name ')
    parser_dump_cfg.set_defaults(func=dump_cfg)

    # generate filelist
    parser_filelist = subparsers.add_parser("filelist", help="""
        is_library_file: -v, is_library_dir: -y is_include_dir: +incdir+
    """
    )
    parser_filelist.add_argument(
        'project_cfg', type=str, nargs='?',
        default='project.yml', help='Project configure file path')
    parser_filelist.add_argument(
        '--target', '-t', type=str, nargs='?',
        default='all', help='filelist target, default is all')

    parser_filelist.set_defaults(func=gen_filelist)

    # Install Dependencies
    parser_dep = subparsers.add_parser("install", help="""
        Install Dependencies
    """
    )
    parser_dep.add_argument(
        'project_cfg', type=str, nargs='?',
        default='project.yml', help='Project configure file path')

    parser_dep.set_defaults(func=gen_dependencies)

    # List Available Batteries
    parser_bat = subparsers.add_parser("list", help="""
        List Available Batteries
    """
    )
    parser_bat.add_argument(
        'project_cfg', type=str, nargs='?',
        default='project.yml', help='Project configure file path')

    parser_bat.set_defaults(func=list_batteries)


    args = parser.parse_args()

    if hasattr(args, "func"):
        return args
    if hasattr(args, "subparser"):
        args.subparser.print_help()
    else:
        parser.print_help()
        return None

def create(args):
    prj_name = args.prj_name
    top = args.top
    cfg = args.config
    if isinstance(args.config, list):
        cfg = args.config[0]
    sc = ScratChip(prj_name, cfg)
    sc.create(top)
    sc.init(True)

def init(args):
    prj_name = args.prj_name
    cfg = args.config

    if isinstance(args.config, list):
        cfg = args.config[0]
    sc = ScratChip(prj_name, cfg)
    sc.init(False)

def dump_cfg(args):
    cfg = get_resource_name("assets/default.yaml")
    dump_name = args.dump_name
    shutil.copyfile(cfg, dump_name)

def gen_filelist(args):
    cfg = get_resource_name("assets/default.yaml")
    prj_cfg = args.project_cfg
    target = args.target
    if isinstance(args.config, list):
        cfg = args.project_cfg[0]
    sc = ScratChip('.', cfg)
    sc.gen_filelist(prj_cfg, target)

def gen_dependencies(args):
    prj_cfg = args.project_cfg

    dm = DependenciesManager(prj_cfg)
    dm.install()

def list_batteries(args):
    prj_cfg = args.project_cfg

    bm = BatteriesManager()
    bm.list_batteries()


def main():
    args = parse_args()
    if not args:
        exit(0)

    # Run the function
    args.func(args)

if __name__ == "__main__":
    main()
