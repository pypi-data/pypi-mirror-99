import pathlib

from setuptools import find_packages
from setuptools import setup

from corelibs import config, lazy

ROOT_DIR = pathlib.Path(__file__).parent
README = (ROOT_DIR / "README.md").read_text(encoding="UTF-8")

lazy.delete_files("./corelibs/docs", extension="*")
lazy.copy("./docs/build/html", "./corelibs/docs")

setup(
    name="corelibs",
    version=config.PACKAGE_VERSION,
    description="꧁֍( Point Bleu Pâle )֎꧂",
    long_description=README,
    long_description_content_type='text/markdown',
    author="宀Kลⴅเ宀 ☬( Michel•TRUONG )☬",
    author_email="michel.truong@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["tests", "__pycache__"]),
    package_data={
        "corelibs": [
            ".corelibs/*/*",
            "bin/*/*/*",
            "yaml/*/*/*",
            "docs/*/*",
            "gui/*/*"
            "corelibs.*"
        ],
    },
    include_package_data=True,
    install_requires=[
        "mkl-service>=2.3.0",
        "cryptography",
        "coloredlogs>=14.0",
        "colorama>=0.4.3",
        "schema>=0.7.2",
        "ipython>=7.19.0",
        "blessed>=1.17.11",  # 1.17.11 not compatible with inquirer>=2.7.0 (must be 1.17.6)
        "enlighten>=1.6.2",
        "click>=7.1.2",
        "numpy==1.19.3",  # >=1.19.4 => numba will crash!
        "numba==0.51.2",  # 2 avoid bug as 0.51.2 is compatible with numpy 1.19.3
        "PyYAML>=5.3.1",
        "yamale>=3.0.4",
        "sqlparse>=0.4.1",
        "stackprinter>=0.2.5",
        "moment>=0.12.1",
        "pysimplegui>=4.33.0",
        "pyscaffold>=3.3",
        "dtale>=1.30.0",
        "pyspark>=3.0.1",
        # "dask>=2020.12.0",
        "dask[complete]",
        "pandasgui>=0.2.9",
        "openpyxl>=3.0.6",
        "phonenumbers>=8.12.19",
        "email-validator>=1.1.2",
    ],
    entry_points={
        "console_scripts": [
            "corelibs=corelibs.cli:main",
        ]
    },
)

lazy.delete_files("./build", extension="*")
