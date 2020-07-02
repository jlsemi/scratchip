# Prepare

Change `CHISEL3_JAR` variable to your favorite version of Chisel3's URL in `Makefile`, and then:

```shell
$ make prepare
```

```shell
$ sudo pip3 install wheel
$ sudo pip3 install --upgrade setuptools
$ python3 setup.py bdist_wheel
```

# Install

```shell
$ pip3 install --user `ls dist/*.whl`
```

Add `bin` path to `PATH` in `~/.bashrc`

```shell
export PATH=~/.local/bin:$PATH
```
