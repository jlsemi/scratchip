# Scratchip

**scratchip** is a framework that can help to build your Chisel and Verilog/Systemverilog project easier.

## Build

If you want to build *scratchip* from scratch, please refer [how to build](doc/how-to-build.md).

## Install

Install **scratchip** with following shell command, if you would like to install it to system, use `sudo` and remove `--user`.

```shell
# require Python versions: 3.6+
$ pip3 --user install scratchip
```

## Usage

### Create Project (Use default configuration)

Create a project named `foo`, the default top module name is `Top`.

```shell
$ scratchip create foo
```

Create a project named foo, specify top module name to `Foo`.

```shell
$ scratchip create foo --top Foo
```

*scratchip* will generate the basic project directory structure below:

```shell
.
├── builds
│   └── scratchip
|       ├── .cache
│       ├── jars
│       │   └── chisel3.jar
│       └── mill
├── doc
├── hw
│   ├── chisel
│   │   ├── build.sc
│   │   ├── Makefile
│   │   └── src
│   │       └── Foo.scala
│   └── rtl
│── Makefile
└── .gitignore
```

At the same time, all tools include Chisel3/FIRRTL will copy to `builds/scratchip`, and the `builds` should never be commited to git repo. When you clone the project to a new project directory, you will need re-initialize the project with:

```shell
$ scratchip init
```

### Test Demo

```shell
$ make verilog
```

Then the `.fir` and `.v` generated by Chisel3/FIRRTL will be placed at `builds` directory.

```shell
.
├── builds
│   ├── ... 
│   ├── Foo.anno.json
│   ├── Foo.fir
│   └── Foo.v
└── ...
```
