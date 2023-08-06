import setuptools
from pathlib import Path 

setuptools.setup(
    name="wesamhamed",
    version=1.0,
    description=Path("README.md").read_text(),
    author="wesam hamed",
    packages=setuptools.find_packages(exclude=["test","data"]),
)