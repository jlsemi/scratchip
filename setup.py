# coding:utf-8

from setuptools import setup

setup(
    name="scratchip",
    url='https://github.com/jlsemi',
    packages=["scratchip"],
    package_data={
        "scratchip": [
            "jars/chisel3.jar",
            "assets/default.yaml",
            "assets/build.sc",
            "assets/project.mk",
            "assets/chisel.mk",
            "assets/Demo.scala",
            "assets/mill",
            "assets/cache.tar.gz",
            "assets/gitignore",
        ],
    },
    use_scm_version={"relative_to": __file__, "write_to": "scratchip/version.py",},
    author="Leway Colin@JLSemi",
    author_email="colinlin@jlsemi.com",
    description=(
        "ScratChip is a framework that can help to build your Chisel and Verilog/Systemverilog project easier."
    ),
    license="Apache-2.0 License",
    keywords=[
        "verilog",
        "chisel",
        "rtl",
    ],
    entry_points={"console_scripts": ["scratchip = scratchip.main:main"]},
    setup_requires=["setuptools_scm",],
    install_requires=[
        "chisel3-jar",
        "mill-bin",
        "mill-cache",
        "pyyaml",
    ],
    # Supported Python versions: 3.6+
    python_requires=">=3.6",
)
