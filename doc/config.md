# Customize your project

*scratchip* use yaml to describ the configuration.

The default YAML configuration：

```yaml
---
hierarchy:
  Makefile: assets/project.mk
  doc: ''
  hw:
    chisel:
      build.sc: assets/build.sc
      Makefile: assets/chisel.mk
      src:
        Demo.scala: assets/Demo.scala
    rtl: ''
```

Default configuration just describe project hierarchy. `key` is for directory or file name. If it is empty, `value` is empty string; if it is file, the `value` is the path to scratchip's `asserts` directory.

## Custom Configuration

Export default configuration, then customize.

### Export Default Configuration

```shell
$ scratchip dump_cfg path/to/file
```
### Create project with custom configuration

```shell
$ scratchip --config path/to/file create [project name]
```
